# Schema

## GenerateGameArtInput

```ts
type GenerateGameArtInput = {
  project_name: string;
  asset_type: "character" | "background" | "prop" | "weapon" | "ui" | "icon" | "sprite_sheet" | "tilemap" | "logo";
  usage: "concept" | "final_asset" | "prototype" | "production";
  theme: string;
  style: {
    art_style: string;
    mood?: string;
    color_palette?: string[];
    perspective?: "top_down" | "side_view" | "isometric" | "front_view";
    line_style?: "clean" | "bold" | "pixel" | "hand_drawn" | "none";
    lighting?: string;
    reference_description?: string;
  };
  spec: {
    description: string;
    size?: { width: number; height: number };
    transparent_background?: boolean;
    variations?: number;
    animation_states?: string[];
    ui_states?: Array<"normal" | "hover" | "pressed" | "disabled">;
    slicing_required?: boolean;
    output_format?: "png" | "webp" | "jpg";
  };
  constraints?: {
    avoid_text?: boolean;
    avoid_logo?: boolean;
    avoid_real_person?: boolean;
    safe_for_children?: boolean;
    no_watermark?: boolean;
  };
};
```

## GenerateGameArtOutput

```ts
type GenerateGameArtOutput = {
  status: "success" | "partial" | "failed";
  assets: Array<{
    id: string;
    name: string;
    type: string;
    file_path: string;
    width: number;
    height: number;
    format: string;
    transparent_background: boolean;
    tags: string[];
  }>;
  metadata: {
    project_name: string;
    style_summary: string;
    prompt_used: string;
    negative_prompt_used: string;
    model_used?: string;
    seed?: number;
  };
  validation: {
    passed: boolean;
    issues: string[];
  };
  suggestions?: string[];
};
```

## MVP Guards

- Accept full schema for compatibility.
- In v1, hard-support only: `character`, `background`, `prop`, `ui`, `icon`.
- For unsupported types, return failure with clear issues.
