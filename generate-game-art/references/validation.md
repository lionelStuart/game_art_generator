# Validation Rules

## Required checks

1. Dimensions match requested `spec.size` when provided.
2. File format matches `spec.output_format` or default `png`.
3. Transparency matches `spec.transparent_background`.
4. File naming follows:
   - `{{project_name}}/{{asset_type}}/{{asset_name}}_v{{version}}.{{format}}`
5. Style consistency check against style contract:
   - palette drift
   - line style mismatch
   - realism drift
6. Constraint checks:
   - no text / no watermark / no logos / no real people if requested.

## Status policy

- `success`: all assets pass all checks.
- `partial`: at least one asset valid, at least one issue exists.
- `failed`: zero valid assets or critical validation errors.

## Issue examples

- `unsupported asset_type for MVP: sprite_sheet`
- `asset[1] expected transparent background, got opaque`
- `asset[0] naming violation: expected ..._v001.png`
- `asset[2] style inconsistency: line_style expected 'bold'`
