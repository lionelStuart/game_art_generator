import json
import tempfile
import unittest
from pathlib import Path

import sys
sys.path.append(str(Path(__file__).resolve().parents[1] / "scripts"))
from generate_game_art import generate_game_art


class GenerateGameArtTests(unittest.TestCase):
    def test_supported_asset_generates_variations(self):
        with tempfile.TemporaryDirectory() as td:
            result = generate_game_art(
                {
                    "project_name": "Alien Kid",
                    "asset_type": "icon",
                    "usage": "prototype",
                    "theme": "slime",
                    "style": {"art_style": "cartoon"},
                    "spec": {
                        "description": "water balloon",
                        "variations": 2,
                        "size": {"width": 128, "height": 128},
                        "output_format": "png",
                        "transparent_background": True,
                    },
                },
                output_root=td,
            )
            self.assertEqual(result["status"], "success")
            self.assertEqual(len(result["assets"]), 2)
            self.assertTrue(Path(td, result["assets"][0]["file_path"]).exists())

    def test_unsupported_asset_fails(self):
        result = generate_game_art(
            {
                "project_name": "Alien Kid",
                "asset_type": "sprite_sheet",
                "usage": "prototype",
                "theme": "slime",
                "style": {"art_style": "cartoon"},
                "spec": {"description": "hero"},
            }
        )
        self.assertEqual(result["status"], "failed")
        self.assertIn("unsupported asset_type for MVP", result["validation"]["issues"][0])


if __name__ == "__main__":
    unittest.main()
