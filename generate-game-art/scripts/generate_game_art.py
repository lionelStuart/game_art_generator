#!/usr/bin/env python3
from __future__ import annotations

import base64
import json
import re
import struct
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

SUPPORTED_ASSET_TYPES = {"character", "background", "prop", "ui", "icon"}
NEGATIVE_PROMPT = (
    "low quality, blurry, noisy, realistic photo, watermark, signature, text, logo, "
    "messy background, inconsistent style, extra limbs, broken anatomy, unreadable shape, "
    "over-detailed, distorted, cropped object, bad perspective"
)

# 1x1 transparent PNG fallback.
FALLBACK_PNG_BYTES = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR4nGNgYGD4DwABBAEAX+XDSwAAAABJRU5ErkJggg=="
)


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.strip().lower()).strip("_") or "asset"


def _style_contract(data: Dict[str, Any]) -> Dict[str, Any]:
    style = data.get("style", {})
    constraints = ["consistent proportions", "no realistic texture", "mobile game friendly"]
    c = data.get("constraints", {})
    if c.get("avoid_text", True):
        constraints.append("no text")
    if c.get("no_watermark", True):
        constraints.append("no watermark")
    if c.get("avoid_logo", True):
        constraints.append("no logo")
    if c.get("avoid_real_person", True):
        constraints.append("no real person")
    return {
        "visual_style": style.get("art_style", "casual mobile game 2D"),
        "color_palette": style.get("color_palette", []),
        "line_style": style.get("line_style", "clean"),
        "rendering": f"2D {style.get('mood', 'readable')} game asset",
        "constraints": constraints,
    }


def _build_prompt(asset_type: str, description: str, style_contract: Dict[str, Any]) -> str:
    templates = {
        "character": "Create a 2D game character asset for a casual mobile game.",
        "background": "Create a 2D game background for a casual mobile game.",
        "prop": "Create a 2D game prop asset.",
        "ui": "Create a 2D mobile game UI component set.",
        "icon": "Create a 2D game icon.",
    }
    head = templates.get(asset_type, f"Create a 2D game {asset_type} asset.")
    return (
        f"{head}\n\nDescription:\n{description}\n\nStyle:\n"
        f"{json.dumps(style_contract, ensure_ascii=False)}\n\n"
        "Requirements:\n- game-ready\n- no text\n- no watermark"
    )


def _extract_png_size(content: bytes) -> Optional[tuple[int, int]]:
    if len(content) < 24 or content[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    return struct.unpack(">II", content[16:24])


def _validate_asset(asset: Dict[str, Any], data: Dict[str, Any]) -> List[str]:
    issues: List[str] = []
    spec = data.get("spec", {})
    expected_size = spec.get("size")
    if expected_size and (asset["width"] != expected_size["width"] or asset["height"] != expected_size["height"]):
        issues.append("size mismatch")
    expected_format = spec.get("output_format", "png")
    if asset["format"] != expected_format:
        issues.append("format mismatch")
    expected_transparent = spec.get("transparent_background")
    if expected_transparent is not None and asset["transparent_background"] != expected_transparent:
        issues.append("transparent_background mismatch")
    pattern = rf"^{re.escape(data['project_name'])}/{re.escape(data['asset_type'])}/[a-z0-9_]+_v\d{{3}}\.{asset['format']}$"
    if not re.match(pattern, asset["file_path"]):
        issues.append("naming violation")
    if asset["byte_size"] <= 0:
        issues.append("empty file")
    return issues


def render_variations(
    prompt: str,
    negative_prompt: str,
    variations: int,
    *,
    image_generator: Optional[Callable[..., List[bytes]]] = None,
    use_codex_image_gen: bool = False,
) -> List[bytes]:
    """Render variations via backend callback.

    - If `image_generator` is provided, it must return image bytes.
    - If `use_codex_image_gen` is True, caller should provide a wrapper callback that
      invokes Codex built-in `image_gen` tool and returns bytes.
    - Fallback uses a transparent PNG so pipeline can still run offline.
    """
    if image_generator:
        return image_generator(prompt=prompt, negative_prompt=negative_prompt, n=variations)
    return [FALLBACK_PNG_BYTES for _ in range(variations)]


def generate_game_art(
    input_data: Dict[str, Any],
    output_root: str = "outputs",
    *,
    image_generator: Optional[Callable[..., List[bytes]]] = None,
    use_codex_image_gen: bool = False,
) -> Dict[str, Any]:
    project_name = _slug(input_data.get("project_name", "project"))
    asset_type = input_data.get("asset_type", "")
    spec = input_data.get("spec", {})

    if asset_type not in SUPPORTED_ASSET_TYPES:
        return {
            "status": "failed",
            "assets": [],
            "metadata": {
                "project_name": project_name,
                "style_summary": "",
                "prompt_used": "",
                "negative_prompt_used": NEGATIVE_PROMPT,
            },
            "validation": {"passed": False, "issues": [f"unsupported asset_type for MVP: {asset_type}"]},
            "suggestions": ["Use one of: character, background, prop, ui, icon"],
        }

    input_data = {**input_data, "project_name": project_name}
    style_contract = _style_contract(input_data)
    prompt = _build_prompt(asset_type, spec.get("description", ""), style_contract)

    variations = max(1, int(spec.get("variations", 1)))
    req_width = int(spec.get("size", {}).get("width", 1024))
    req_height = int(spec.get("size", {}).get("height", 1024))
    fmt = spec.get("output_format", "png")
    transparent = spec.get("transparent_background", asset_type != "background")

    root = Path(output_root)
    assets: List[Dict[str, Any]] = []
    all_issues: List[str] = []

    rendered_bytes = render_variations(
        prompt,
        NEGATIVE_PROMPT,
        variations,
        image_generator=image_generator,
        use_codex_image_gen=use_codex_image_gen,
    )

    for i, content in enumerate(rendered_bytes, start=1):
        name = _slug(spec.get("description", f"{asset_type}_{i}"))
        asset_name = f"{name}_{i:02d}" if variations > 1 else name
        rel_path = f"{project_name}/{asset_type}/{asset_name}_v001.{fmt}"
        abs_path = root / rel_path
        abs_path.parent.mkdir(parents=True, exist_ok=True)
        abs_path.write_bytes(content)

        parsed = _extract_png_size(content) if fmt == "png" else None
        width, height = parsed if parsed else (req_width, req_height)

        asset = {
            "id": f"{asset_type}_{i:03d}",
            "name": asset_name,
            "type": asset_type,
            "file_path": rel_path,
            "width": width,
            "height": height,
            "format": fmt,
            "transparent_background": transparent,
            "tags": [asset_type, input_data.get("theme", "")],
            "byte_size": len(content),
        }
        issues = _validate_asset(asset, input_data)
        all_issues.extend([f"asset[{i-1}] {it}" for it in issues])
        assets.append(asset)

    passed = len(all_issues) == 0
    status = "success" if passed else ("partial" if assets else "failed")
    return {
        "status": status,
        "assets": assets,
        "metadata": {
            "project_name": project_name,
            "style_summary": json.dumps(style_contract, ensure_ascii=False),
            "prompt_used": prompt,
            "negative_prompt_used": NEGATIVE_PROMPT,
            "seed": input_data.get("seed"),
            "model_used": "codex_image_gen" if use_codex_image_gen else "fallback_png",
        },
        "validation": {"passed": passed, "issues": all_issues},
        "suggestions": [] if passed else ["Adjust backend output, size/format/transparency, or naming inputs"],
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate game art metadata and files")
    parser.add_argument("--input", required=True, help="Path to input JSON")
    parser.add_argument("--output-root", default="outputs", help="Root directory for generated assets")
    parser.add_argument("--use-codex-image-gen", action="store_true", help="Mark model_used as codex_image_gen")
    args = parser.parse_args()

    payload = json.loads(Path(args.input).read_text(encoding="utf-8"))
    result = generate_game_art(payload, output_root=args.output_root, use_codex_image_gen=args.use_codex_image_gen)
    print(json.dumps(result, ensure_ascii=False, indent=2))
