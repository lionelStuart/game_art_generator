# Implementation Blueprint (MVP)

## Public API

```ts
function generate_game_art(input: GenerateGameArtInput): GenerateGameArtOutput
```

## Internal flow pseudo-code

```ts
normalize = parse_request(input)
style_contract = build_style_contract(normalize)
prompt = build_prompt(normalize.asset_type, normalize.spec.description, style_contract)
neg = unified_negative_prompt
raw_images = render_variations(prompt, neg, normalize.spec.variations, normalize.seed)
processed = postprocess_assets(raw_images, normalize)
sliced = normalize.spec.slicing_required ? slice_assets(processed, normalize) : processed
validation = validate_assets(sliced, normalize, style_contract)
metadata = export_metadata(normalize, prompt, neg)
return assemble_output(sliced, metadata, validation)
```

## Defaults

- `spec.variations`: default `1`, max recommended `4` in MVP.
- `spec.output_format`: default `png`.
- `spec.transparent_background`:
  - default `true` for `character|prop|icon|ui`
  - default `false` for `background`

## Determinism

- If `seed` exists in runtime/backend options, pass seed to renderer.
- Include `seed` in metadata.

## Suggested tests

1. Prompt template routing by `asset_type`.
2. Style contract inheritance across all variations.
3. Naming convention compliance.
4. Transparency expectation checks.
5. Failure mode for unsupported `asset_type`.
