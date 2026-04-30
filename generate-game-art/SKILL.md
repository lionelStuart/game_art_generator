---
name: generate-game-art
description: Generate production-ready game art assets with a single public tool `generate_game_art(input)`, including consistent style contracts, asset-type-specific prompts, image post-processing, validation, and export metadata. Use when users need character/background/prop/ui/icon assets for mobile games with reusable naming conventions, transparent background handling, multiple variations, and explicit validation issues.
---

# Generate Game Art Skill

Implement one public entrypoint only:

- `generate_game_art(input: GenerateGameArtInput): GenerateGameArtOutput`

Do not expose pipeline internals as public tools.

## Build MVP Scope First

Support only these `asset_type` values in v1:

- `character`
- `background`
- `prop`
- `ui`
- `icon`

Return `status: "failed"` with `validation.issues` for unsupported types.

## Follow Internal Pipeline

Run these steps in order:

1. Parse and normalize request.
2. Build style contract.
3. Build prompt by asset type.
4. Generate image variations.
5. Post-process image outputs.
6. Slice assets when requested.
7. Validate dimensions/format/transparency/naming/style consistency.
8. Export metadata and final output.

Use deterministic generation when a seed is provided.

## Read Reference Files Before Implementing

- Input/output schema and defaults: `references/schema.md`
- Prompt templates and negative prompt: `references/prompts.md`
- Validation rules and file naming: `references/validation.md`
- Implementation blueprint and pseudo-code: `references/implementation.md`

## Output Contract Requirements

Always return:

- `assets[]` with file path, dimensions, format, transparency flag, and tags
- `metadata` including `prompt_used` and `negative_prompt_used`
- `validation` with `passed` and `issues`

Never silently pass invalid outputs. Populate `validation.issues` and downgrade status to `partial` or `failed`.

## Naming Convention

Use this exact pattern:

- `{{project_name}}/{{asset_type}}/{{asset_name}}_v{{version}}.{{format}}`

Examples:

- `alien_kid/prop/water_balloon_v001.png`
- `alien_kid/ui/start_button_pressed_v001.png`
- `alien_kid/background/night_street_v001.png`

## Suggested Module Split

Implement helpers as internal modules/functions:

- `parse_request`
- `build_style_contract`
- `build_prompt`
- `render_variations`
- `postprocess_assets`
- `slice_assets`
- `validate_assets`
- `export_metadata`

Keep public interface flat and simple.
