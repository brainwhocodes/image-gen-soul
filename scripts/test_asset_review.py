"""Synthetic regression cases; no private art or model/network calls."""
import contextlib
import io
import tempfile
import unittest
from pathlib import Path

import numpy as np
from PIL import Image, ImageCms

from asset_review import create_review, main


class AssetReviewTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def save(self, image, filename='source.png'):
        source = self.root / filename
        image.save(source)
        return source

    def test_native_composites_gaps_and_partial_edges_preserve_source(self):
        image = Image.new('RGBA', (12, 10), (0, 255, 0, 0))
        image.paste((200, 60, 20, 255), (2, 2, 10, 8))
        image.putpixel((4, 4), (0, 255, 0, 0))
        image.putpixel((2, 2), (200, 60, 20, 128))
        source = self.save(image)
        before = source.read_bytes()
        output = self.root / 'qa'
        result = create_review(source, output, ['#eee6f4'], [(2, 2, 4, 3)], True)
        self.assertEqual(source.read_bytes(), before)
        self.assertTrue(result['nonempty_transparency'])
        self.assertEqual(result['visible_subject_bounds_px'], (2, 2, 10, 8))
        self.assertEqual(result['alpha_pixels']['partial'], 1)
        self.assertIsNone(result['visual_review_passed'])
        self.assertEqual(len(result['backgrounds']), 3)
        with Image.open(output / 'background-1.png') as light:
            self.assertEqual(light.size, image.size)
            self.assertEqual(light.getpixel((4, 4)), (255, 255, 255))
            self.assertEqual(light.getpixel((5, 5)), (200, 60, 20))
            self.assertEqual(light.getpixel((2, 2)), (227, 157, 137))
        with Image.open(output / 'background-2.png') as dark:
            self.assertEqual(dark.getpixel((4, 4)), (32, 32, 32))
        with Image.open(output / 'background-3-detail-1.png') as crop:
            self.assertEqual(crop.size, (4, 3))
            self.assertEqual(crop.getpixel((2, 2)), (238, 230, 244))

    def test_opaque_checkerboard_fails_required_alpha_even_in_rgba(self):
        pixels = np.zeros((16, 16, 4), dtype=np.uint8)
        gray = np.where(np.indices((16, 16)).sum(axis=0) % 2, 128, 200)
        pixels[:, :, :3] = gray[:, :, None]
        pixels[:, :, 3] = 255
        source = self.save(Image.fromarray(pixels))
        with contextlib.redirect_stdout(io.StringIO()):
            code = main([str(source), str(self.root / 'opaque'), '--require-alpha'])
        self.assertEqual(code, 1)

    def test_clear_corners_do_not_certify_internal_checkerboard(self):
        image = Image.new('RGBA', (10, 10), (0, 0, 0, 0))
        for x in range(2, 8):
            for y in range(2, 8):
                gray = 128 if (x + y) % 2 else 200
                image.putpixel((x, y), (gray, gray, gray, 255))
        result = create_review(self.save(image), self.root / 'residue', require_alpha=True)
        self.assertTrue(result['nonempty_transparency'])
        self.assertIsNone(result['visual_review_passed'])
        self.assertEqual(result['status'], 'manual_review_required')
        with Image.open(self.root / 'residue/background-1.png') as shown:
            self.assertEqual(shown.getpixel((3, 3)), (200, 200, 200))

    def test_empty_foreground_fails_required_alpha(self):
        source = self.save(Image.new('RGBA', (10, 10), (255, 0, 0, 0)))
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(main([str(source), str(self.root / 'empty'), '--require-alpha']), 1)

    def test_white_and_gray_foreground_details_are_not_color_keyed(self):
        image = Image.new('RGBA', (8, 8), (0, 0, 0, 0))
        image.paste((255, 255, 255, 255), (2, 2, 6, 6))
        image.putpixel((4, 4), (128, 128, 128, 255))
        output = self.root / 'neutral-details'
        create_review(self.save(image), output)
        with Image.open(output / 'background-2.png') as shown:
            self.assertEqual(shown.getpixel((3, 3)), (255, 255, 255))
            self.assertEqual(shown.getpixel((4, 4)), (128, 128, 128))

    def test_palette_transparency_is_measured_not_inferred_from_mode(self):
        image = Image.new('P', (4, 4), 0)
        image.putpalette([0, 255, 0, 200, 60, 20] + [0] * 762)
        image.info['transparency'] = 0
        image.putpixel((2, 2), 1)
        result = create_review(self.save(image), self.root / 'palette')
        self.assertEqual(result['alpha_pixels']['transparent'], 15)
        self.assertTrue(result['nonempty_transparency'])

    def test_refuses_overwrite_and_out_of_bounds_crops(self):
        source = self.save(Image.new('RGBA', (5, 5), (120, 80, 30, 255)))
        existing = self.root / 'existing'
        existing.mkdir()
        with self.assertRaises(FileExistsError):
            create_review(source, existing)
        missing = self.root / 'invalid'
        with self.assertRaises(ValueError):
            create_review(source, missing, crops=[(4, 4, 3, 3)])
        self.assertFalse(missing.exists())
        with self.assertRaises(ValueError):
            create_review(source, missing, crops=[(-1, 0, 3, 3)])

    def test_rejects_animation_instead_of_silently_reviewing_first_frame(self):
        source = self.root / 'animated.gif'
        first = Image.new('RGB', (10, 10), 'red')
        first.save(source, save_all=True, append_images=[Image.new('RGB', (10, 10), 'blue')])
        with self.assertRaises(ValueError):
            create_review(source, self.root / 'animation')

    def test_orientation_normalizes_alpha_bounds_and_detail_coordinates(self):
        image = Image.new('RGBA', (6, 4), (0, 0, 0, 0))
        image.putpixel((1, 2), (200, 60, 20, 255))
        source = self.root / 'oriented.png'
        exif = image.getexif()
        exif[274] = 6
        image.save(source, exif=exif)
        output = self.root / 'oriented'
        result = create_review(source, output, crops=[(1, 1, 1, 1)])
        self.assertEqual(result['stored_dimensions_px'], [6, 4])
        self.assertEqual(result['dimensions_px'], [4, 6])
        self.assertEqual(result['visible_subject_bounds_px'], (1, 1, 2, 2))
        with Image.open(output / 'background-1-detail-1.png') as detail:
            self.assertEqual(detail.getpixel((0, 0)), (200, 60, 20))
            self.assertNotIn(274, detail.getexif())

    def test_embedded_profile_converts_to_tagged_srgb_before_compositing(self):
        lab = Image.new('LAB', (6, 4), (150, 160, 110))
        profile = ImageCms.ImageCmsProfile(ImageCms.createProfile('LAB'))
        srgb = ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB'))
        source = self.root / 'profiled.tif'
        lab.save(source, icc_profile=profile.tobytes())
        expected = ImageCms.profileToProfile(lab, profile, srgb, outputMode='RGB')
        output = self.root / 'profiled'
        result = create_review(source, output)
        self.assertIn('Converted embedded ICC profile', result['color_management'])
        with Image.open(output / 'background-1.png') as shown:
            self.assertEqual(shown.getpixel((2, 2)), expected.getpixel((2, 2)))
            self.assertTrue(shown.info.get('icc_profile'))
            self.assertNotEqual(shown.getpixel((2, 2)), (150, 160, 110))

    def test_profiled_rgba_preserves_exact_alpha(self):
        image = Image.new('RGBA', (6, 4), (200, 60, 20, 128))
        image.putpixel((0, 0), (0, 0, 0, 0))
        profile = ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB'))
        source = self.root / 'profiled-alpha.png'
        image.save(source, icc_profile=profile.tobytes())
        output = self.root / 'profiled-alpha'
        result = create_review(source, output)
        self.assertEqual(result['alpha_pixels'], {'transparent': 1, 'partial': 23, 'opaque': 0})
        with Image.open(output / 'alpha.png') as alpha:
            self.assertTrue(np.array_equal(np.asarray(alpha), np.asarray(image.getchannel('A'))))
            self.assertIsNone(alpha.info.get('icc_profile'))

    def test_invalid_profile_is_rejected_without_creating_misleading_evidence(self):
        source = self.root / 'bad-profile.png'
        Image.new('RGB', (6, 4), 'red').save(source, icc_profile=b'not a profile')
        output = self.root / 'bad-profile'
        with self.assertRaises(ValueError):
            create_review(source, output)
        self.assertFalse(output.exists())


if __name__ == '__main__':
    unittest.main()
