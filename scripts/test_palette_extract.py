"""Behavior checks using synthetic pixels, with no bundled reference artwork."""
import unittest
from PIL import Image
from palette_extract import palette

class PaletteTests(unittest.TestCase):
    def test_opaque_single_color_has_all_the_weight(self):
        measured = palette(Image.new('RGB', (40, 20), (192, 64, 32)))
        self.assertAlmostEqual(sum(c['percent'] for c in measured['colors']), 100, places=1)
        self.assertEqual(measured['colors'][0]['hex'], '#c04020')
        self.assertAlmostEqual(sum(measured['luminance']), 100, places=1)

    def test_transparent_pixels_do_not_change_the_palette(self):
        image = Image.new('RGBA', (32, 16), (0, 255, 0, 0))
        image.paste((192, 64, 32, 255), (0, 0, 16, 16))
        measured = palette(image)
        self.assertEqual(measured['colors'][0]['hex'], '#c04020')
        self.assertAlmostEqual(measured['colors'][0]['percent'], 100, places=1)

    def test_fully_transparent_has_no_color_claim(self):
        measured = palette(Image.new('RGBA', (20, 20), (192, 64, 32, 0)))
        self.assertEqual(measured['colors'], [])

if __name__ == '__main__':
    unittest.main()
