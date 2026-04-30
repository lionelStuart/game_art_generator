# Prompt Templates

## Style Contract Target Shape

```json
{
  "visual_style": "...",
  "color_palette": ["..."],
  "line_style": "...",
  "rendering": "...",
  "constraints": [
    "consistent proportions",
    "no realistic texture",
    "no text",
    "no watermark",
    "mobile game friendly"
  ]
}
```

## Character

Create a 2D game character asset for a casual mobile game.

Subject:
{{description}}

Style:
{{style_contract}}

Requirements:
- full body
- centered composition
- transparent background
- clean silhouette
- readable at small size
- game-ready asset
- no text
- no watermark

## Background

Create a 2D game background for a casual mobile game.

Scene:
{{description}}

Style:
{{style_contract}}

Requirements:
- wide background composition
- clear foreground / midground / background separation
- leave enough empty space for gameplay objects
- no text
- no watermark
- mobile screen friendly

## Prop

Create a 2D game prop asset.

Object:
{{description}}

Style:
{{style_contract}}

Requirements:
- isolated object
- transparent background
- clear silhouette
- suitable for mobile game inventory or gameplay use
- readable at 64x64 and 128x128
- no text
- no watermark

## UI

Create a 2D mobile game UI component set.

UI Description:
{{description}}

Style:
{{style_contract}}

Requirements:
- include normal / pressed / disabled states if needed
- clean edges
- readable buttons
- no fake text
- no watermark
- suitable for slicing into reusable UI components

## Icon

Create a 2D game icon.

Icon:
{{description}}

Style:
{{style_contract}}

Requirements:
- centered object
- simple shape
- strong contrast
- readable at 32x32, 64x64, 128x128
- transparent background
- no text
- no watermark

## Unified Negative Prompt

low quality, blurry, noisy, realistic photo, watermark, signature, text, logo, messy background, inconsistent style, extra limbs, broken anatomy, unreadable shape, over-detailed, distorted, cropped object, bad perspective
