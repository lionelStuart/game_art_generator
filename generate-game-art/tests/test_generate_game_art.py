import tempfile
import unittest
from pathlib import Path

import sys
sys.path.append(str(Path(__file__).resolve().parents[1] / "scripts"))
from generate_game_art import FALLBACK_PNG_BYTES, generate_game_art


def fake_image_generator(**kwargs):
    return [FALLBACK_PNG_BYTES for _ in range(kwargs["n"])]


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
                        "output_format": "png",
                        "transparent_background": True,
                    },
                },
                output_root=td,
                image_generator=fake_image_generator,
                use_codex_image_gen=True,
            )
            self.assertEqual(result["status"], "success")
            self.assertEqual(result["metadata"]["model_used"], "codex_image_gen")
            self.assertEqual(len(result["assets"]), 2)
            file_path = Path(td, result["assets"][0]["file_path"])
            self.assertTrue(file_path.exists())
            self.assertGreater(file_path.stat().st_size, 0)

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
