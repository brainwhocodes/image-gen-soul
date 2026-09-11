"""Local synthetic tests. Creates temporary fixtures only; no reference images ship."""
from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

import numpy as np
from PIL import Image

import color_pipeline as cp


class ColorPipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.rng = np.random.default_rng(817)
        self.pixels = self.rng.integers(12, 244, size=(40, 56, 3), dtype=np.uint8)
        self.source = self.root / "source.png"
        Image.fromarray(self.pixels).save(self.source)
        self.reference = self.root / "reference.png"
        transformed = np.clip(self.pixels.astype(float) * .95 + 9, 0, 255).astype(np.uint8)
        Image.fromarray(transformed).save(self.reference)

    def tearDown(self):
        self.temp.cleanup()

    def run_cli(self, args):
        parsed = cp.build_parser().parse_args([str(a) for a in args])
        with contextlib.redirect_stdout(io.StringIO()):
            parsed.func(parsed)

    def manual_recipe(self, settings=None):
        path = self.root / "manual.json"
        path.write_text(json.dumps({"schema_version": 1, "source": {"sha256": cp.digest(self.source)},
                                    "settings": settings or cp.identity_settings()}))
        return path

    def test_color_round_trip(self):
        rgb = self.rng.random((17, 19, 3))
        back = cp.linear_to_srgb(cp.oklab_to_linear(cp.linear_to_oklab(cp.srgb_to_linear(rgb))))
        np.testing.assert_allclose(rgb, back, atol=2e-7)

    def test_zero_strength_is_exact(self):
        settings = cp.identity_settings()
        settings.update(strength=0, exposure_ev=1, chroma_scale=1.8)
        rgb = self.pixels / 255.
        np.testing.assert_array_equal(cp.grade_array(rgb, settings), rgb)

    def test_identity_recipe_keeps_8bit_pixels(self):
        rgb = self.pixels / 255.
        graded = cp.grade_array(rgb, cp.identity_settings())
        np.testing.assert_array_equal(np.rint(graded * 255).astype(np.uint8), self.pixels)

    def test_zero_mask_is_exact(self):
        settings = cp.identity_settings()
        settings.update(exposure_ev=.5)
        rgb = self.pixels / 255.
        np.testing.assert_array_equal(cp.grade_array(rgb, settings, np.zeros(rgb.shape[:2])), rgb)

    def test_partial_mask_preserves_black_region(self):
        settings = cp.identity_settings()
        settings.update(strength=.8, exposure_ev=.5)
        rgb = self.pixels / 255.
        mask = np.ones(rgb.shape[:2]); mask[:, :20] = 0
        graded = cp.grade_array(rgb, settings, mask)
        np.testing.assert_array_equal(graded[:, :20], rgb[:, :20])
        self.assertGreater(float(np.mean(np.abs(graded[:, 20:] - rgb[:, 20:]))), .001)

    def test_gamut_map_finite_and_bounded(self):
        lab = self.rng.uniform(-1, 1, size=(31, 43, 3))
        lab[..., 0] = self.rng.uniform(-.3, 1.4, size=(31, 43))
        rgb = cp.gamut_map(lab)
        self.assertTrue(np.all(np.isfinite(rgb)))
        self.assertTrue(np.all((rgb >= 0) & (rgb <= 1)))

    def test_neutrals_not_tinted_by_chroma(self):
        gray = np.linspace(.1, .9, 100).reshape(10, 10)
        rgb = np.repeat(gray[..., None], 3, axis=2)
        settings = cp.identity_settings(); settings.update(strength=1, chroma_scale=1.9)
        graded = cp.grade_array(rgb, settings)
        np.testing.assert_allclose(graded[..., 0], graded[..., 1], atol=1e-6)
        np.testing.assert_allclose(graded[..., 1], graded[..., 2], atol=1e-6)

    def test_fit_and_apply_cli(self):
        recipe = self.root / "grade.json"
        output = self.root / "graded.png"
        report = self.root / "qa.json"
        self.run_cli(["fit", self.source, "--reference", self.reference, "--recipe", recipe])
        self.run_cli(["apply", self.source, output, "--recipe", recipe, "--report", report])
        record = json.loads(report.read_text())
        self.assertTrue(record["same_displayed_dimensions"])
        self.assertTrue(record["alpha_preserved"])
        self.assertEqual(record["visual_review"], "not performed by this script")
        with Image.open(output) as saved:
            self.assertIsNotNone(saved.info.get("icc_profile"))

    def test_inspect_records_measurements(self):
        report = self.root / "inspect.json"
        self.run_cli(["inspect", self.source, self.reference, "--report", report])
        data = json.loads(report.read_text())
        self.assertEqual(len(data["images"]), 2)
        self.assertEqual(data["images"][0]["displayed_size"], [56, 40])

    def test_reference_weights(self):
        recipe = self.root / "grade.json"
        self.run_cli(["fit", self.source, "--reference", self.source,
                      "--reference", self.reference, "--weights", "3,1", "--recipe", recipe])
        data = json.loads(recipe.read_text())
        self.assertEqual([r["weight"] for r in data["references"]], [.75, .25])

    def test_invalid_weights_rejected(self):
        with self.assertRaises(ValueError):
            self.run_cli(["fit", self.source, "--reference", self.reference,
                          "--weights", "-1", "--recipe", self.root / "grade.json"])

    def test_source_hash_mismatch_rejected(self):
        recipe = self.manual_recipe()
        with self.assertRaisesRegex(ValueError, "different source"):
            self.run_cli(["apply", self.reference, self.root / "out.png", "--recipe", recipe])

    def test_source_hash_override_reported(self):
        recipe = self.manual_recipe()
        report = self.root / "qa.json"
        self.run_cli(["apply", self.reference, self.root / "out.png", "--recipe", recipe,
                      "--allow-new-source", "--report", report])
        self.assertTrue(any("reused" in w for w in json.loads(report.read_text())["warnings"]))

    def test_original_overwrite_rejected(self):
        recipe = self.manual_recipe()
        with self.assertRaisesRegex(ValueError, "overwrite"):
            self.run_cli(["apply", self.source, self.source, "--recipe", recipe, "--overwrite"])

    def test_hardlink_overwrite_rejected(self):
        alias = self.root / "alias.png"
        alias.hardlink_to(self.source)
        with self.assertRaisesRegex(ValueError, "aliases"):
            cp.guard_outputs([alias], [self.source], True)

    def test_alpha_and_hidden_rgb_preserved(self):
        rgba = np.dstack([self.pixels, self.rng.integers(0, 256, size=(40, 56), dtype=np.uint8)])
        rgba[:4, :, 3] = 0
        path = self.root / "alpha.png"
        Image.fromarray(rgba).save(path)
        settings = cp.identity_settings(); settings.update(strength=.6, exposure_ev=.3)
        recipe = self.root / "alpha-recipe.json"
        recipe.write_text(json.dumps({"schema_version": 1, "settings": settings}))
        output = self.root / "alpha-out.png"
        self.run_cli(["apply", path, output, "--recipe", recipe])
        with Image.open(output) as saved:
            result = np.asarray(saved)
        np.testing.assert_array_equal(result[..., 3], rgba[..., 3])
        np.testing.assert_array_equal(result[:4], rgba[:4])

    def test_transparent_rgb_excluded_from_statistics(self):
        rgba = np.dstack([self.pixels, np.full((40, 56), 255, dtype=np.uint8)])
        rgba[:20, :, 3] = 0
        path = self.root / "alpha.png"; Image.fromarray(rgba).save(path)
        rgb, alpha, _ = cp.load_srgb(path)
        values, weights = cp.samples(rgb, alpha)
        self.assertEqual(len(values), 20 * 56)

    def test_nonopaque_jpeg_rejected(self):
        path = self.root / "alpha.png"
        image = Image.fromarray(self.pixels); image.putalpha(128); image.save(path)
        with self.assertRaisesRegex(ValueError, "transparency"):
            self.run_cli(["apply", path, self.root / "out.jpg", "--recipe", self.manual_recipe(), "--allow-new-source"])

    def test_protection_mask_on_saved_png(self):
        mask_path = self.root / "protect.png"
        mask = np.zeros((40, 56), dtype=np.uint8); mask[:, :20] = 255
        Image.fromarray(mask).save(mask_path)
        settings = cp.identity_settings(); settings.update(strength=.9, exposure_ev=.5)
        output = self.root / "protected.png"
        self.run_cli(["apply", self.source, output, "--recipe", self.manual_recipe(settings), "--protect-mask", mask_path])
        with Image.open(output) as saved:
            result = np.asarray(saved)
        np.testing.assert_array_equal(result[:, :20], self.pixels[:, :20])

    def test_mask_dimension_mismatch_rejected(self):
        p = self.root / "mask.png"; Image.new("L", (4, 4), 255).save(p)
        with self.assertRaisesRegex(ValueError, "expected"):
            cp.load_mask(p, (56, 40))

    def test_empty_analysis_mask_rejected(self):
        rgb, alpha, _ = cp.load_srgb(self.source)
        with self.assertRaisesRegex(ValueError, "Fewer"):
            cp.samples(rgb, alpha, Image.new("L", rgb.size, 0))

    def test_invalid_curve_rejected(self):
        with self.assertRaises(ValueError):
            cp.validate_settings({"lightness_curve": {"x": [0, .5, .4, 1], "y": [0, .5, .6, 1]}})

    def test_unknown_setting_rejected(self):
        with self.assertRaisesRegex(ValueError, "Unknown"):
            cp.validate_settings({"saturtion": 1.2})

    def test_nonfinite_setting_rejected(self):
        with self.assertRaises(ValueError):
            cp.validate_settings({"exposure_ev": float("nan")})

    def test_hue_band_requires_explicit_center(self):
        with self.assertRaisesRegex(ValueError, "center_deg"):
            cp.validate_settings({"hue_adjustments": [{"rotation_deg": 2}]})

    def test_flat_tone_fit_skipped(self):
        values = np.full((100, 3), .4)
        stats = cp.statistics(values, np.ones(100))
        settings, warnings = cp.fit_settings(stats, stats, .3, False)
        self.assertEqual(settings["lightness_curve"], {"x": [0., 1.], "y": [0., 1.]})
        self.assertTrue(any("Flat" in w for w in warnings))

    def test_16bit_png_rejected(self):
        path = self.root / "depth.png"
        Image.fromarray(np.arange(100, dtype=np.uint16).reshape(10, 10)).save(path)
        with self.assertRaisesRegex(ValueError, "8-bit"):
            cp.load_srgb(path)

    def test_untagged_cmyk_rejected(self):
        path = self.root / "cmyk.tif"
        Image.fromarray(self.pixels).convert("CMYK").save(path)
        with self.assertRaisesRegex(ValueError, "Untagged"):
            cp.load_srgb(path)

    def test_exif_orientation(self):
        path = self.root / "orientation.jpg"
        image = Image.fromarray(self.pixels)
        exif = image.getexif(); exif[274] = 6
        image.save(path, exif=exif)
        rgb, _, meta = cp.load_srgb(path)
        self.assertEqual(rgb.size, (40, 56))
        self.assertEqual(meta["stored_size"], [56, 40])

    def test_comparison_sheet(self):
        output = self.root / "compare.png"
        self.run_cli(["compare", self.source, self.reference, output, "--reference", self.source])
        with Image.open(output) as image:
            self.assertEqual(image.size, (1260, 556))


if __name__ == "__main__":
    unittest.main(verbosity=2)
