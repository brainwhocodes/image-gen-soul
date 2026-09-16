"""Make cutout review evidence, never a visual-cleanliness certification.

No background removal, model download, network or source modification. Output
must be a new directory. Native-size composites/crops expose detail that small
contact sheets miss; alpha measurements alone cannot detect a baked checkerboard.
"""
import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageCms, ImageColor, ImageDraw

from color_pipeline import load_srgb


def parse_crop(value):
    try:
        crop = tuple(int(part) for part in value.split(','))
        if len(crop) != 4 or min(crop[:2]) < 0 or min(crop[2:]) <= 0:
            raise ValueError
        return crop
    except ValueError as exc:
        raise argparse.ArgumentTypeError('crop must be nonnegative x,y and positive w,h') from exc


def parse_background(value):
    try:
        color = ImageColor.getcolor(value, 'RGB')
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f'invalid solid background: {value}') from exc
    return '#%02x%02x%02x' % color


def create_review(source, destination, backgrounds=(), crops=(), require_alpha=False):
    source, destination = Path(source).resolve(), Path(destination).resolve()
    # Share the package's orientation/profile normalization and HDR/animation
    # rejection rather than quietly changing the image's displayed appearance.
    rgb, source_alpha, metadata = load_srgb(source)
    image = rgb.convert('RGBA')
    if source_alpha is not None:
        image.putalpha(source_alpha)
    srgb_profile = ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB')).tobytes()
    width, height = image.size
    colors = list(dict.fromkeys(['#ffffff', '#202020', *map(parse_background, backgrounds)]))
    for crop in crops:
        if (len(crop) != 4 or min(crop[:2]) < 0 or min(crop[2:]) <= 0
                or crop[0] + crop[2] > width or crop[1] + crop[3] > height):
            raise ValueError(f'Crop {crop} lies outside the {width}x{height} source')

    alpha = np.asarray(image.getchannel('A'))
    transparent = int(np.count_nonzero(alpha == 0))
    partial = int(np.count_nonzero((alpha > 0) & (alpha < 255)))
    opaque = int(np.count_nonzero(alpha == 255))
    visible = partial + opaque
    warnings = []
    if not transparent and not partial:
        warnings.append('No transparent pixels: an opaque matte/checkerboard is not a cutout.')
    if not visible:
        warnings.append('No visible foreground: an empty image is not a valid cutout.')
    report = {
        'source_name': source.name,
        'source_sha256': metadata['sha256'],
        'stored_dimensions_px': metadata['stored_size'],
        'dimensions_px': [width, height],
        'coordinate_space': 'displayed pixels after EXIF orientation normalization',
        'color_management': metadata['color_management'],
        'alpha_extrema': [int(alpha.min()), int(alpha.max())],
        'alpha_pixels': {'transparent': transparent, 'partial': partial, 'opaque': opaque},
        'visible_subject_bounds_px': image.getchannel('A').getbbox(),
        'canvas_edge_has_foreground': bool(np.any(alpha[0]) or np.any(alpha[-1])
                                           or np.any(alpha[:, 0]) or np.any(alpha[:, -1])),
        'nonempty_transparency': bool(visible and (transparent or partial)),
        'require_alpha': require_alpha,
        'visual_review_passed': None,
        'status': 'manual_review_required',
        'warnings': warnings,
        'review_instructions': [
            'Inspect native-size composites, not only the contact sheet.',
            'Check silhouette AND interior gaps for checkerboard, matte remnants and fringes.',
            'Compare face, hands, fabric and props to the original for erased details.',
            'Inspect on actual destination colors and at the rendered placement size.',
            'This report does not certify clean edges, color accuracy, pose or layout fidelity.',
        ],
        'backgrounds': [],
        'detail_crops': [],
    }

    # Refuse to overwrite any prior evidence (or a directory containing the source).
    destination.mkdir(parents=True, exist_ok=False)
    # Alpha is numeric coverage, not RGB color; do not inherit an RGB ICC tag.
    image.getchannel('A').save(destination / 'alpha.png', icc_profile=None)
    cell_width, cell_height = 320, 360
    columns = min(3, len(colors))
    rows = (len(colors) + columns - 1) // columns
    sheet = Image.new('RGB', (columns * cell_width, rows * cell_height), '#e6e6e6')
    for index, color in enumerate(colors):
        composite = Image.new('RGBA', image.size, color)
        composite.alpha_composite(image)
        composite = composite.convert('RGB')
        filename = f'background-{index + 1}.png'
        composite.save(destination / filename, icc_profile=srgb_profile)
        report['backgrounds'].append({'color': color, 'native_size_composite': filename})
        for number, (x, y, w, h) in enumerate(crops, 1):
            crop_file = f'background-{index + 1}-detail-{number}.png'
            composite.crop((x, y, x + w, y + h)).save(destination / crop_file, icc_profile=srgb_profile)
            report['detail_crops'].append({'path': crop_file, 'source_xywh': [x, y, w, h],
                                           'scale': 1, 'background': color})
        thumb = composite.copy()
        thumb.thumbnail((cell_width - 16, cell_height - 40), Image.Resampling.LANCZOS)
        left, top = index % columns * cell_width, index // columns * cell_height
        ImageDraw.Draw(sheet).text((left + 8, top + 8), color, fill='#111111')
        sheet.paste(thumb, (left + (cell_width - thumb.width) // 2, top + 32))
    sheet.save(destination / 'contact-sheet.png', icc_profile=srgb_profile)
    (destination / 'review.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    return report


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('destination', type=Path, help='new job-local evidence directory')
    parser.add_argument('--background', action='append', default=[], type=parse_background,
                        help='additional solid destination color; light/dark always included')
    parser.add_argument('--crop', action='append', default=[], type=parse_crop,
                        help='native-resolution detail in displayed, EXIF-normalized pixels: x,y,w,h')
    parser.add_argument('--require-alpha', action='store_true', help='fail empty or fully opaque art')
    args = parser.parse_args(argv)
    try:
        report = create_review(args.source, args.destination, args.background, args.crop,
                               args.require_alpha)
    except (ValueError, OSError) as exc:
        parser.error(str(exc))
    print(f'Review artifacts: {args.destination / "review.json"}')
    print('Visual review required; alpha statistics are not approval.')
    return 1 if args.require_alpha and not report['nonempty_transparency'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
