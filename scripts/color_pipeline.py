#!/usr/bin/env python3
"""Reference-driven, conservative sRGB grading. No built-in aesthetic presets.

Commands: inspect, fit, apply, compare. Run a command with --help for details.
Requires Python 3.10+, Pillow, NumPy. All work is local; no generation/API calls.
Oklab conversion matrices: https://bottosson.github.io/posts/oklab/
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import io
import json
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image, ImageCms, ImageDraw, ImageOps

VERSION = "1.0.0"
FORMATS = {".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff"}
QUANTILES = np.array([0.05, 0.25, 0.50, 0.75, 0.95])
M1 = np.array([[.4122214708, .5363325363, .0514459929],
               [.2119034982, .6806995451, .1073969566],
               [.0883024619, .2817188376, .6299787005]], dtype=np.float64)
M2 = np.array([[.2104542553, .7936177850, -.0040720468],
               [1.9779984951, -2.4285922050, .4505937099],
               [.0259040371, .7827717662, -.8086757660]], dtype=np.float64)
I1, I2 = np.linalg.inv(M1), np.linalg.inv(M2)


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def srgb_to_linear(rgb: np.ndarray) -> np.ndarray:
    return np.where(rgb <= .04045, rgb / 12.92,
                    np.maximum((rgb + .055) / 1.055, 0) ** 2.4)


def linear_to_srgb(rgb: np.ndarray) -> np.ndarray:
    rgb = np.maximum(rgb, 0)
    return np.where(rgb <= .0031308, 12.92 * rgb,
                    1.055 * rgb ** (1 / 2.4) - .055)


def linear_to_oklab(rgb: np.ndarray) -> np.ndarray:
    return np.cbrt(rgb @ M1.T) @ M2.T


def oklab_to_linear(lab: np.ndarray) -> np.ndarray:
    return ((lab @ I2.T) ** 3) @ I1.T


def smoothstep(low: float, high: float, x: np.ndarray) -> np.ndarray:
    t = np.clip((x - low) / (high - low), 0, 1)
    return t * t * (3 - 2 * t)


def gamut_map(lab: np.ndarray) -> np.ndarray:
    """Reduce out-of-gamut Oklab chroma at fixed lightness/hue; not a LUT."""
    safe = lab.copy()
    safe[..., 0] = np.clip(safe[..., 0], 0, 1)
    rgb = oklab_to_linear(safe)
    bad = np.any((rgb < -1e-7) | (rgb > 1 + 1e-7), axis=-1)
    if np.any(bad):
        points = safe[bad].copy()
        lo = np.zeros(len(points))
        hi = np.ones(len(points))
        for _ in range(12):
            mid = (lo + hi) * .5
            trial = points.copy()
            trial[:, 1:] *= mid[:, None]
            candidate = oklab_to_linear(trial)
            good = np.all((candidate >= -1e-7) & (candidate <= 1 + 1e-7), axis=1)
            lo = np.where(good, mid, lo)
            hi = np.where(good, hi, mid)
        points[:, 1:] *= lo[:, None]
        rgb[bad] = oklab_to_linear(points)
    return np.clip(rgb, 0, 1)


def load_srgb(path: Path) -> tuple[Image.Image, Image.Image | None, dict[str, Any]]:
    """Normalize displayed orientation and color. Return 8-bit RGB and exact alpha."""
    if not path.is_file():
        raise ValueError(f"Image not found: {path}")
    with Image.open(path) as opened:
        if getattr(opened, "n_frames", 1) != 1:
            raise ValueError(f"Animated/multipage input is not supported: {path}")
        # Reject high-bit-depth TIFF/PNG rather than silently claiming HDR support.
        bits = getattr(opened, "tag_v2", {}).get(258, ())
        if isinstance(bits, int):
            bits = (bits,)
        png_depth = None
        if opened.format == "PNG":
            with path.open("rb") as f:
                header = f.read(25)
            if len(header) == 25:
                png_depth = header[24]
        if (opened.mode in {"I", "F"} or opened.mode.startswith("I;16")
                or any(int(b) > 8 for b in bits) or (png_depth and png_depth > 8)):
            raise ValueError("Use an 8-bit display-referred sRGB export; this helper is not RAW/HDR/16-bit mastering.")
        raw_size = opened.size
        source_mode = opened.mode
        image = ImageOps.exif_transpose(opened)
        image.load()
        has_alpha = "A" in image.getbands() or "transparency" in image.info
        alpha = image.convert("RGBA").getchannel("A") if has_alpha else None
        icc = image.info.get("icc_profile")
        if icc:
            color = image if image.mode in {"RGB", "CMYK", "LAB", "L"} else image.convert("RGB")
            try:
                rgb = ImageCms.profileToProfile(
                    color, ImageCms.ImageCmsProfile(io.BytesIO(icc)),
                    ImageCms.createProfile("sRGB"), outputMode="RGB")
            except Exception as exc:
                raise ValueError(f"Cannot convert embedded color profile in {path}: {exc}") from exc
            color_note = "Converted embedded ICC profile to sRGB."
        else:
            if image.mode in {"CMYK", "LAB"}:
                raise ValueError("Untagged CMYK/LAB cannot be interpreted safely; export to tagged sRGB.")
            rgb = image.convert("RGB")
            color_note = "No embedded ICC profile; RGB/grayscale input assumed sRGB."
        meta = {"path": str(path.resolve()), "sha256": digest(path),
                "original_mode": source_mode, "stored_size": list(raw_size),
                "displayed_size": list(rgb.size), "has_alpha": has_alpha,
                "color_management": color_note}
        return rgb.copy(), alpha.copy() if alpha else None, meta


def load_mask(path: Path | None, size: tuple[int, int]) -> Image.Image | None:
    if path is None:
        return None
    if not path.is_file():
        raise ValueError(f"Mask not found: {path}")
    with Image.open(path) as opened:
        if getattr(opened, "n_frames", 1) != 1:
            raise ValueError("Masks must be single-frame images.")
        image = ImageOps.exif_transpose(opened)
        if image.size != size:
            raise ValueError(f"Mask {path} has size {image.size}; expected displayed/oriented size {size}.")
        if image.mode in {"I", "F"} or image.mode.startswith("I;16"):
            raise ValueError("Export masks as 8-bit opaque grayscale, not floating-point/16-bit data.")
        if (("A" in image.getbands() or "transparency" in image.info)
                and image.convert("RGBA").getchannel("A").getextrema() != (255, 255)):
            raise ValueError("Export masks as opaque grayscale: white selects/protects, black excludes.")
        return image.convert("L").copy()


def samples(rgb: Image.Image, alpha: Image.Image | None,
            mask: Image.Image | None = None) -> tuple[np.ndarray, np.ndarray]:
    """Deterministic grid, at most 512 x 512 samples; never mix hidden RGB into samples."""
    w, h = rgb.size
    ys = np.linspace(0, h - 1, min(h, 512)).round().astype(int)
    xs = np.linspace(0, w - 1, min(w, 512)).round().astype(int)
    values = np.asarray(rgb)[ys[:, None], xs[None, :]].reshape(-1, 3) / 255.0
    weights = np.ones(len(values), dtype=np.float64)
    if alpha is not None:
        weights *= np.asarray(alpha)[ys[:, None], xs[None, :]].reshape(-1) / 255.0
    if mask is not None:
        weights *= np.asarray(mask)[ys[:, None], xs[None, :]].reshape(-1) / 255.0
    keep = weights > 1e-8
    if np.count_nonzero(keep) < 4:
        raise ValueError("Fewer than four visible/selected analysis samples. Use a larger selection or crop.")
    return values[keep], weights[keep]


def weighted_quantiles(values: np.ndarray, weights: np.ndarray,
                       q: np.ndarray = QUANTILES) -> np.ndarray:
    order = np.argsort(values, kind="stable")
    v, w = values[order], weights[order]
    cumulative = (np.cumsum(w) - .5 * w) / w.sum()
    return np.interp(q, cumulative, v)


def statistics(values: np.ndarray, weights: np.ndarray) -> dict[str, Any]:
    lab = linear_to_oklab(srgb_to_linear(values))
    lightness = lab[:, 0]
    chroma = np.hypot(lab[:, 1], lab[:, 2])
    colored = (chroma > .025) & (lightness > .05) & (lightness < .98)
    neutral = (chroma < .03) & (lightness > .20) & (lightness < .95)
    colored_fraction = float(weights[colored].sum() / weights.sum())
    neutral_fraction = float(weights[neutral].sum() / weights.sum())
    median_c = (float(weighted_quantiles(chroma[colored], weights[colored], np.array([.5]))[0])
                if np.count_nonzero(colored) >= 4 else None)
    neutral_ab = (np.average(lab[neutral, 1:], axis=0, weights=weights[neutral]).tolist()
                  if np.count_nonzero(neutral) >= 4 else None)
    return {"sample_count": len(values), "quantile_positions": QUANTILES.tolist(),
            "oklab_lightness_quantiles": weighted_quantiles(lightness, weights).tolist(),
            "oklab_chroma_quantiles": weighted_quantiles(chroma, weights).tolist(),
            "colored_sample_fraction": colored_fraction, "colored_median_chroma": median_c,
            "low_chroma_sample_fraction": neutral_fraction, "low_chroma_mean_ab": neutral_ab,
            "near_black_channel_fraction": float(np.average(np.any(values <= 1 / 255, axis=1), weights=weights)),
            "near_white_channel_fraction": float(np.average(np.any(values >= 254 / 255, axis=1), weights=weights)),
            "boundary_note": "Channel-boundary fractions are warnings, not proof of lost highlight/shadow detail."}


def identity_settings() -> dict[str, Any]:
    return {"strength": .30, "exposure_ev": 0.0, "lightness_offset": 0.0,
            "lightness_curve": {"x": [0.0, 1.0], "y": [0.0, 1.0]},
            "chroma_scale": 1.0, "neutral_shift_ab": [0.0, 0.0],
            "neutral_protection": 1.0, "highlight_protection": .65,
            "hue_adjustments": []}


def validate_settings(raw: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(raw, dict):
        raise ValueError("Recipe settings must be an object.")
    settings = identity_settings()
    unknown = set(raw) - set(settings)
    if unknown:
        raise ValueError(f"Unknown recipe settings: {sorted(unknown)}")
    settings.update(copy.deepcopy(raw))
    ranges = {"strength": (0, 1), "exposure_ev": (-2, 2), "lightness_offset": (-.2, .2),
              "chroma_scale": (0, 2), "neutral_protection": (0, 1), "highlight_protection": (0, 1)}
    for key, (low, high) in ranges.items():
        val = settings[key]
        if isinstance(val, bool) or not isinstance(val, (int, float)) or not math.isfinite(val) or not low <= val <= high:
            raise ValueError(f"{key} must be a finite number between {low} and {high}.")
    curve = settings["lightness_curve"]
    if not isinstance(curve, dict) or set(curve) != {"x", "y"}:
        raise ValueError("lightness_curve needs x and y arrays only.")
    x, y = np.array(curve["x"], dtype=float), np.array(curve["y"], dtype=float)
    if (x.ndim != 1 or y.ndim != 1 or len(x) != len(y) or not 2 <= len(x) <= 64
            or not np.all(np.isfinite(x)) or not np.all(np.isfinite(y))
            or x[0] != 0 or x[-1] != 1 or np.any(np.diff(x) <= 0)
            or np.any(np.diff(y) < 0) or np.any(y < 0) or np.any(y > 1)):
        raise ValueError("Curve x must increase strictly from 0 to 1; y must be monotonic in [0,1].")
    shift = np.asarray(settings["neutral_shift_ab"], dtype=float)
    if shift.shape != (2,) or not np.all(np.isfinite(shift)) or np.any(np.abs(shift) > .05):
        raise ValueError("neutral_shift_ab needs two finite Oklab values, each within +/-0.05.")
    bands = settings["hue_adjustments"]
    if not isinstance(bands, list) or len(bands) > 24:
        raise ValueError("hue_adjustments must be a list of at most 24 bands.")
    defaults = {"center_deg": 0., "width_deg": 30., "rotation_deg": 0.,
                "chroma_scale": 1., "lightness_offset": 0.}
    for i, band in enumerate(bands):
        if not isinstance(band, dict) or set(band) - set(defaults):
            raise ValueError("Unknown hue-adjustment fields.")
        if "center_deg" not in band:
            raise ValueError("Each hue band needs an explicitly measured/chosen center_deg.")
        b = {**defaults, **band}
        for key, low, high in [("center_deg", 0, 360), ("width_deg", 1, 180),
                              ("rotation_deg", -30, 30), ("chroma_scale", 0, 2),
                              ("lightness_offset", -.15, .15)]:
            val = b[key]
            if isinstance(val, bool) or not isinstance(val, (int, float)) or not math.isfinite(val) or not low <= val <= high:
                raise ValueError(f"Invalid hue band {i} field {key}.")
        bands[i] = b
    return settings


def fit_settings(source_stats: dict[str, Any], reference_stats: dict[str, Any],
                 strength: float, neutral_cast: bool) -> tuple[dict[str, Any], list[str]]:
    settings = identity_settings()
    settings["strength"] = strength
    warnings = ["Statistical fit is a starting point, not semantic/object-aware color matching. Review the actual image."]
    sq = np.array(source_stats["oklab_lightness_quantiles"])
    rq = np.array(reference_stats["oklab_lightness_quantiles"])
    if sq[-1] - sq[0] < .02 or rq[-1] - rq[0] < .02:
        warnings.append("Flat source/reference lightness: automatic tone fit skipped.")
    else:
        # Match only part of each measured discrepancy. Bound deviations and slopes.
        anchors = np.linspace(0, 1, 11)
        ux, inv = np.unique(sq, return_inverse=True)
        delta = np.bincount(inv, weights=rq - sq) / np.bincount(inv)
        adjustment = np.interp(anchors, ux, np.clip(delta, -.06, .06))
        adjustment *= np.sin(np.pi * anchors) ** .65
        target = np.clip(anchors + adjustment, 0, 1)
        target[0], target[-1] = 0., 1.
        for i in range(1, len(target)):
            dx = anchors[i] - anchors[i - 1]
            target[i] = np.clip(target[i], target[i - 1] + .5 * dx, target[i - 1] + 1.5 * dx)
        for i in range(len(target) - 2, -1, -1):
            dx = anchors[i + 1] - anchors[i]
            target[i] = np.clip(target[i], target[i + 1] - 1.5 * dx, target[i + 1] - .5 * dx)
        target[0], target[-1] = 0., 1.
        settings["lightness_curve"] = {"x": anchors.tolist(), "y": target.tolist()}
    sc, rc = source_stats["colored_median_chroma"], reference_stats["colored_median_chroma"]
    if (sc and rc and source_stats["colored_sample_fraction"] >= .03
            and reference_stats["colored_sample_fraction"] >= .03):
        settings["chroma_scale"] = float(np.clip(rc / sc, .88, 1.12))
    else:
        warnings.append("Insufficient comparable colored samples: automatic chroma fit skipped.")
    if neutral_cast:
        sa, ra = source_stats["low_chroma_mean_ab"], reference_stats["low_chroma_mean_ab"]
        if (sa is not None and ra is not None and source_stats["low_chroma_sample_fraction"] >= .03
                and reference_stats["low_chroma_sample_fraction"] >= .03):
            settings["neutral_shift_ab"] = np.clip(np.array(ra) - np.array(sa), -.008, .008).tolist()
            warnings.append("Optional low-chroma cast matching enabled. Low chroma is not semantic white balance; inspect it.")
        else:
            warnings.append("Not enough comparable low-chroma samples: cast matching skipped.")
    return validate_settings(settings), warnings


def grade_array(rgb: np.ndarray, settings: dict[str, Any],
                mask: np.ndarray | None = None) -> np.ndarray:
    """Apply all corrections in one pass; zero strength/mask is a true no-op."""
    s = settings
    strength = float(s["strength"])
    if strength == 0 or (mask is not None and not np.any(mask > 0)):
        return rgb.copy()
    original_linear = srgb_to_linear(rgb)
    original_lab = linear_to_oklab(original_linear)
    lab = linear_to_oklab(original_linear * (2.0 ** s["exposure_ev"]))
    curve = s["lightness_curve"]
    lab[..., 0] = np.interp(lab[..., 0], curve["x"], curve["y"]) + s["lightness_offset"]
    chroma = np.hypot(lab[..., 1], lab[..., 2])
    gate = 1 - s["neutral_protection"] * (1 - smoothstep(.015, .05, chroma))
    lab[..., 1:] *= (1 + (s["chroma_scale"] - 1) * gate)[..., None]
    # Each explicitly supplied hue band is evaluated against the pre-band colors.
    base = lab.copy()
    hue = np.degrees(np.arctan2(base[..., 2], base[..., 1])) % 360
    for band in s["hue_adjustments"]:
        distance = np.abs((hue - band["center_deg"] + 180) % 360 - 180)
        weight = (1 - smoothstep(0, band["width_deg"], distance)) * gate
        angle = np.radians(band["rotation_deg"])
        a, b = base[..., 1], base[..., 2]
        na = (a * np.cos(angle) - b * np.sin(angle)) * band["chroma_scale"]
        nb = (a * np.sin(angle) + b * np.cos(angle)) * band["chroma_scale"]
        lab[..., 1] += (na - a) * weight
        lab[..., 2] += (nb - b) * weight
        lab[..., 0] += band["lightness_offset"] * weight
    neutral = ((1 - smoothstep(.015, .05, chroma))
               * smoothstep(.08, .25, original_lab[..., 0])
               * (1 - smoothstep(.85, 1., original_lab[..., 0])))
    lab[..., 1:] += neutral[..., None] * np.array(s["neutral_shift_ab"])
    protect = 1 - s["highlight_protection"] * smoothstep(.85, 1., original_lab[..., 0])
    lab = original_lab + (lab - original_lab) * protect[..., None]
    candidate = gamut_map(lab)
    weight = strength if mask is None else strength * np.clip(mask, 0, 1)[..., None]
    result = np.clip(linear_to_srgb(original_linear * (1 - weight) + candidate * weight), 0, 1)
    if mask is not None:
        result[mask <= 0] = rgb[mask <= 0]
    return result


def guard_outputs(outputs: list[Path | None], inputs: list[Path | None], overwrite: bool) -> None:
    outs = [p for p in outputs if p is not None]
    protected = {p.resolve() for p in inputs if p is not None}
    resolved = [p.resolve() for p in outs]
    if len(set(resolved)) != len(resolved):
        raise ValueError("Output paths must be distinct.")
    for p in outs:
        if p.resolve() in protected:
            raise ValueError(f"Refusing to overwrite an input/reference/recipe/mask: {p}")
        if p.exists() and not overwrite:
            raise ValueError(f"Output exists: {p}. Use a new name or --overwrite.")
        if p.exists() and not p.is_file():
            raise ValueError(f"Output is not a regular file: {p}")
        # Guard hard-link aliases as well as ordinary paths/symlinks.
        if p.exists():
            for src in inputs:
                if src is not None and src.exists() and p.samefile(src):
                    raise ValueError(f"Output aliases a protected input: {p}")


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, allow_nan=False) + "\n", encoding="utf-8")


def save_image(rgb: Image.Image, alpha: Image.Image | None, path: Path) -> None:
    if path.suffix.lower() not in FORMATS:
        raise ValueError(f"Unsupported output format: {path.suffix}")
    output = rgb.copy()
    jpeg = path.suffix.lower() in {".jpg", ".jpeg"}
    if alpha is not None:
        if jpeg and alpha.getextrema() != (255, 255):
            raise ValueError("JPEG cannot preserve transparency. Use PNG/WebP/TIFF or explicitly flatten first.")
        if not jpeg:
            output.putalpha(alpha)
    options: dict[str, Any] = {"icc_profile": ImageCms.ImageCmsProfile(ImageCms.createProfile("sRGB")).tobytes()}
    if jpeg:
        options.update(quality=96, subsampling=0)
    elif path.suffix.lower() == ".webp":
        options.update(lossless=True, exact=True)
    path.parent.mkdir(parents=True, exist_ok=True)
    output.save(path, **options)


def command_inspect(args: argparse.Namespace) -> None:
    guard_outputs([args.report], args.inputs, args.overwrite)
    records = []
    for p in args.inputs:
        rgb, alpha, meta = load_srgb(p)
        values, weights = samples(rgb, alpha)
        records.append({**meta, "statistics": statistics(values, weights)})
    data = {"tool_version": VERSION, "images": records,
            "note": "Measured job-local data only. No semantic interpretation or persistent aesthetic profile."}
    if args.report:
        write_json(args.report, data)
        print(f"Saved measurements: {args.report}")
    else:
        print(json.dumps(data, indent=2))


def command_fit(args: argparse.Namespace) -> None:
    refs: list[Path] = args.reference
    weights = np.array([float(v) for v in args.weights.split(",")] if args.weights else [1.] * len(refs))
    if len(weights) != len(refs) or not np.all(np.isfinite(weights)) or np.any(weights <= 0):
        raise ValueError("--weights must contain one positive finite number per --reference, in the same order.")
    weights /= weights.sum()
    ref_masks = [None if p == "-" else Path(p) for p in (args.reference_mask or [])]
    if ref_masks and len(ref_masks) != len(refs):
        raise ValueError("Supply one --reference-mask per reference; use '-' for no mask.")
    ref_masks = ref_masks or [None] * len(refs)
    guard_outputs([args.recipe], [args.input, args.source_mask, *refs, *ref_masks], args.overwrite)
    rgb, alpha, meta = load_srgb(args.input)
    source_mask = load_mask(args.source_mask, rgb.size)
    source_values, source_weights = samples(rgb, alpha, source_mask)
    source_stats = statistics(source_values, source_weights)
    all_values, all_weights, records = [], [], []
    per_ref_stats = []
    for ref, relative_weight, mask_path in zip(refs, weights, ref_masks):
        rr, aa, mm = load_srgb(ref)
        mask = load_mask(mask_path, rr.size)
        values, ws = samples(rr, aa, mask)
        stats = statistics(values, ws)
        all_values.append(values)
        all_weights.append(ws / ws.sum() * relative_weight)
        per_ref_stats.append(stats)
        records.append({**mm, "weight": float(relative_weight),
                        "analysis_mask": str(mask_path.resolve()) if mask_path else None,
                        "analysis_mask_sha256": digest(mask_path) if mask_path else None})
    combined = statistics(np.concatenate(all_values), np.concatenate(all_weights))
    settings, warnings = fit_settings(source_stats, combined, args.strength, args.match_neutral_cast)
    medians = [s["oklab_lightness_quantiles"][2] for s in per_ref_stats]
    if max(medians) - min(medians) > .20:
        warnings.append("References differ substantially in median lightness; prefer one anchor or comparable masked regions.")
    recipe = {"schema_version": 1, "tool_version": VERSION,
              "method": "bounded reference-relative tone/chroma; optional low-chroma cast",
              "source": meta, "references": records,
              "analysis": {"source_mask": str(args.source_mask.resolve()) if args.source_mask else None,
                           "source_mask_sha256": digest(args.source_mask) if args.source_mask else None,
                           "source_statistics": source_stats, "combined_reference_statistics": combined,
                           "individual_reference_statistics": per_ref_stats},
              "settings": settings, "warnings": warnings}
    write_json(args.recipe, recipe)
    print(f"Saved job-specific recipe: {args.recipe}")
    for warning in warnings:
        print(f"Review: {warning}")


def command_apply(args: argparse.Namespace) -> None:
    if not args.recipe.is_file():
        raise ValueError(f"Recipe not found: {args.recipe}")
    recipe = json.loads(args.recipe.read_text(encoding="utf-8"))
    if not isinstance(recipe, dict) or recipe.get("schema_version") != 1:
        raise ValueError("Expected a recipe object with schema_version 1.")
    if recipe.get("source") is not None and not isinstance(recipe["source"], dict):
        raise ValueError("Recipe source must be an object or null.")
    if not isinstance(recipe.get("references", []), list) or any(
            not isinstance(r, dict) for r in recipe.get("references", [])):
        raise ValueError("Recipe references must be a list of objects.")
    if not isinstance(recipe.get("analysis", {}), dict):
        raise ValueError("Recipe analysis must be an object when present.")
    settings = validate_settings(recipe.get("settings", {}))
    overrides = {"strength": args.strength, "exposure_ev": args.exposure, "chroma_scale": args.chroma_scale}
    settings.update({key: value for key, value in overrides.items() if value is not None})
    settings = validate_settings(settings)
    ref_paths = [Path(r["path"]) for r in recipe.get("references", []) if r.get("path")]
    aux_paths = [Path(r["analysis_mask"]) for r in recipe.get("references", []) if r.get("analysis_mask")]
    source_record = recipe.get("source") or {}
    if source_record.get("path"):
        aux_paths.append(Path(source_record["path"]))
    if recipe.get("analysis", {}).get("source_mask"):
        aux_paths.append(Path(recipe["analysis"]["source_mask"]))
    guard_outputs([args.output, args.report], [args.input, args.recipe, args.mask, args.protect_mask,
                                              *ref_paths, *aux_paths], args.overwrite)
    if args.output.suffix.lower() not in FORMATS:
        raise ValueError("Output must be PNG, JPEG, WebP, or 8-bit TIFF.")
    rgb, alpha, meta = load_srgb(args.input)
    expected = source_record.get("sha256")
    warnings = []
    if expected and expected != meta["sha256"]:
        if not args.allow_new_source:
            raise ValueError("Recipe was fitted to a different source. Refit, or explicitly use --allow-new-source and inspect carefully.")
        warnings.append("Recipe intentionally reused on a different source; correspondence is not guaranteed.")
    if not expected:
        warnings.append("Manual recipe has no source hash; verify it belongs to this job.")
    if alpha is not None and alpha.getextrema() != (255, 255) and args.output.suffix.lower() in {".jpg", ".jpeg"}:
        raise ValueError("JPEG cannot preserve transparency; use PNG/WebP/TIFF.")
    apply_mask = load_mask(args.mask, rgb.size)
    protect_mask = load_mask(args.protect_mask, rgb.size)
    before_values, before_weights = samples(rgb, alpha)
    before_stats = statistics(before_values, before_weights)
    output = Image.new("RGB", rgb.size)
    for top in range(0, rgb.height, 192):
        box = (0, top, rgb.width, min(top + 192, rgb.height))
        tile = np.asarray(rgb.crop(box), dtype=np.float64) / 255.0
        mask = np.ones(tile.shape[:2])
        if apply_mask is not None:
            mask *= np.asarray(apply_mask.crop(box)) / 255.0
        if protect_mask is not None:
            mask *= 1 - np.asarray(protect_mask.crop(box)) / 255.0
        if alpha is not None:
            # Preserve invisible RGB. Keep straight-alpha edge colors unattenuated.
            mask *= np.asarray(alpha.crop(box)) > 0
        result = grade_array(tile, settings, mask)
        output.paste(Image.fromarray(np.rint(result * 255).astype(np.uint8)), (0, top))
    save_image(output, alpha, args.output)
    # Verify the actual saved artifact, including any lossy encoding effects.
    saved_rgb, saved_alpha, saved_meta = load_srgb(args.output)
    av, aw = samples(saved_rgb, saved_alpha)
    after_stats = statistics(av, aw)
    for key in ("near_black_channel_fraction", "near_white_channel_fraction"):
        if after_stats[key] > before_stats[key] + .01:
            warnings.append(f"Increased {key}; inspect details before accepting the grade.")
    alpha_same = (alpha is None and saved_alpha is None) or (
        alpha is not None and saved_alpha is not None and np.array_equal(np.asarray(alpha), np.asarray(saved_alpha)))
    if alpha is not None and alpha.getextrema() == (255, 255) and saved_alpha is None:
        alpha_same = True  # Opaque alpha intentionally omitted for JPEG.
    if args.output.suffix.lower() in {".jpg", ".jpeg"}:
        warnings.append("JPEG is lossy; fully protected RGB pixels are exact before encoding, not necessarily after JPEG encoding.")
    report = {"tool_version": VERSION, "input": meta, "output": saved_meta,
              "recipe_path": str(args.recipe.resolve()), "recipe_sha256": digest(args.recipe),
              "applied_settings": settings,
              "mask": str(args.mask.resolve()) if args.mask else None,
              "mask_sha256": digest(args.mask) if args.mask else None,
              "protect_mask": str(args.protect_mask.resolve()) if args.protect_mask else None,
              "protect_mask_sha256": digest(args.protect_mask) if args.protect_mask else None,
              "before": before_stats, "after": after_stats,
              "same_displayed_dimensions": rgb.size == saved_rgb.size,
              "alpha_preserved": bool(alpha_same), "warnings": warnings,
              "visual_review": "not performed by this script"}
    if args.report:
        write_json(args.report, report)
    print(f"Saved: {args.output} | {output.width} x {output.height} | strength={settings['strength']:.3f}")
    for warning in warnings:
        print(f"Review: {warning}")


def command_compare(args: argparse.Namespace) -> None:
    inputs = [args.before, args.after, *(args.reference or [])]
    guard_outputs([args.output], inputs, args.overwrite)
    if args.output.suffix.lower() != ".png":
        raise ValueError("Comparison previews must be PNG.")
    width, height, label_height = 420, 520, 36
    sheet = Image.new("RGB", (width * len(inputs), height + label_height), (232, 232, 232))
    draw = ImageDraw.Draw(sheet)
    for i, path in enumerate(inputs):
        rgb, alpha, _ = load_srgb(path)
        if alpha is not None:
            rgb.putalpha(alpha)
        thumb = ImageOps.contain(rgb, (width - 20, height - 20), Image.Resampling.LANCZOS)
        x = i * width + (width - thumb.width) // 2
        y = label_height + (height - thumb.height) // 2
        if "A" in thumb.getbands():
            sheet.paste(thumb.convert("RGB"), (x, y), thumb.getchannel("A"))
        else:
            sheet.paste(thumb, (x, y))
        label = "Original" if i == 0 else "Corrected" if i == 1 else f"Reference {i - 1}"
        draw.text((i * width + 12, 12), label, fill=(25, 25, 25))
    save_image(sheet, None, args.output)
    print(f"Saved comparison: {args.output}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--version", action="version", version=VERSION)
    commands = parser.add_subparsers(dest="command", required=True)
    inspect = commands.add_parser("inspect", help="Measure current images without changing them.")
    inspect.add_argument("inputs", type=Path, nargs="+")
    inspect.add_argument("--report", type=Path)
    inspect.add_argument("--overwrite", action="store_true")
    inspect.set_defaults(func=command_inspect)
    fit = commands.add_parser("fit", help="Build a bounded job-specific recipe from selected reference pixels.")
    fit.add_argument("input", type=Path)
    fit.add_argument("--reference", type=Path, action="append", required=True)
    fit.add_argument("--weights", help="Comma-separated positive reference weights, in reference order.")
    fit.add_argument("--source-mask", type=Path, help="Analysis-only selection; does NOT restrict where apply operates.")
    fit.add_argument("--reference-mask", action="append", help="Analysis mask per reference; use '-' for no mask.")
    fit.add_argument("--strength", type=float, default=.30)
    fit.add_argument("--match-neutral-cast", action="store_true", help="Opt-in low-chroma cast comparison; not semantic white balance.")
    fit.add_argument("--recipe", type=Path, required=True)
    fit.add_argument("--overwrite", action="store_true")
    fit.set_defaults(func=command_fit)
    apply = commands.add_parser("apply", help="Run Python-only color/tone correction; never changes layout or generates content.")
    apply.add_argument("input", type=Path)
    apply.add_argument("output", type=Path)
    apply.add_argument("--recipe", type=Path, required=True)
    apply.add_argument("--strength", type=float)
    apply.add_argument("--exposure", type=float, help="Override exposure in EV; blended by strength and masks.")
    apply.add_argument("--chroma-scale", type=float)
    apply.add_argument("--mask", type=Path, help="White applies corrections; black leaves normalized sRGB pixels unchanged.")
    apply.add_argument("--protect-mask", type=Path, help="White protects pixels; black permits corrections.")
    apply.add_argument("--report", type=Path)
    apply.add_argument("--allow-new-source", action="store_true")
    apply.add_argument("--overwrite", action="store_true")
    apply.set_defaults(func=command_apply)
    compare = commands.add_parser("compare", help="Make a labeled before/after/reference inspection sheet.")
    compare.add_argument("before", type=Path)
    compare.add_argument("after", type=Path)
    compare.add_argument("output", type=Path)
    compare.add_argument("--reference", type=Path, action="append")
    compare.add_argument("--overwrite", action="store_true")
    compare.set_defaults(func=command_compare)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        args.func(args)
    except (ValueError, OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
