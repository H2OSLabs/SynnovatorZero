# .pen File Format Reference

## Top-Level Structure

Every `.pen` file:
```json
{
  "version": "2.6",
  "children": [ /* one root frame */ ]
}
```

## Node Types

### frame
Container with layout. Most common node type.

```json
{
  "type": "frame",
  "id": "aB3xK",
  "name": "ComponentName",
  "reusable": true,
  "width": 1440,
  "height": 800,
  "fill": "#181818",
  "cornerRadius": 12,
  "stroke": { "thickness": 1, "fill": "#333333" },
  "layout": "vertical",
  "gap": 16,
  "padding": [16, 24],
  "justifyContent": "center",
  "alignItems": "center",
  "clip": true,
  "children": []
}
```

**Key properties:**
- `layout`: `"vertical"` or `"horizontal"` (omit for horizontal default)
- `gap`: spacing between children (number)
- `padding`: single number (all sides), `[vertical, horizontal]`, or `[top, right, bottom, left]`
- `justifyContent`: `"center"`, `"space_between"`, `"end"`
- `alignItems`: `"center"`
- `width`/`height`: number (px), `"fill_container"`, or `"fit_content(0)"`
- `slot`: `[]` — marks frame as a slot (placeholder for child content injection)
- `stroke.align`: `"inside"` for inset borders

### text
Text content node.

```json
{
  "type": "text",
  "id": "xK9mR",
  "name": "labelText",
  "fill": "#FFFFFF",
  "content": "Display text here",
  "fontFamily": "Inter",
  "fontSize": 14,
  "fontWeight": "500",
  "lineHeight": 1.5,
  "letterSpacing": 2,
  "textGrowth": "fixed-width",
  "width": 900
}
```

**fontWeight values:** `"normal"` (400), `"500"`, `"600"`, `"700"`, `"900"`

### icon_font
Icon from Lucide icon set.

```json
{
  "type": "icon_font",
  "id": "p2LmN",
  "name": "iconName",
  "width": 16,
  "height": 16,
  "iconFontName": "search",
  "iconFontFamily": "lucide",
  "fill": "#8E8E8E"
}
```

Common icons: `search`, `plus`, `x`, `chevron-down`, `chevron-left`, `chevron-right`, `check`, `info`, `circle-check`, `house`, `file`, `trash-2`, `pencil`, `eye`, `filter`, `download`, `upload`

### rectangle
Simple rectangle (used for dividers/separators).

```json
{
  "type": "rectangle",
  "id": "rN3bQ",
  "name": "divider",
  "fill": "#333333",
  "width": "fill_container",
  "height": 1
}
```

### ellipse
Circle/oval shape (used for avatars, radio buttons).

```json
{
  "type": "ellipse",
  "id": "eL4wP",
  "name": "circle",
  "fill": "#333333",
  "width": 40,
  "height": 40
}
```

## Design Tokens

### Colors

| Token | Hex | Usage |
|-------|-----|-------|
| `$lime-primary` | `#BBFD3B` | Primary accent, CTA buttons, active states |
| `$surface` | `#00000E` | Page background (near-black) |
| `$dark-bg` | `#333333` | Card backgrounds, secondary surfaces |
| `$near-black` | `#181818` | Main surface background |
| `$muted` | `#8E8E8E` | Placeholder text, secondary icons, helper text |
| `$light-gray` | `#DCDCDC` | Body text on dark bg |
| `$white` | `#FFFFFF` | Primary text, headings on dark bg |
| `$error` | `#FA541C` | Error states, destructive actions |
| `$success` | `#74FFBB` | Success feedback |
| `$warning` | `#FAAD14` | Warning states |
| `$cyan` | `#41FAF4` | Info alerts |
| `$blue` | `#4C78FF` | Links, secondary accent |
| `$pink` | `#FF74A7` | Highlight accent |
| `$orange` | `#FB7A38` | Tertiary accent |
| `$mint` | `#74FFBB` | Same as success |

Use `$token-name` syntax in fill values when referencing design tokens (e.g., `"fill": "$lime-primary"`). Use hex values for non-token colors.

### Background usage
- Page background: `#181818` (near-black surface)
- Card/container: `#222222`
- Table header / button default: `#333333`
- Input field: `#222222` with `#8E8E8E` stroke

### Typography

| Role | Font Family | Size | Weight | Color |
|------|------------|------|--------|-------|
| Page title (H1) | Space Grotesk | 36px | 700 | `$white` |
| Section title (H2) | Space Grotesk | 28px | 700 | `$white` |
| Subsection (H3) | Space Grotesk | 22px | 700 | `$white` |
| Body text | Inter | 16px | normal | `$light-gray` |
| UI label | Inter | 14px | 500 | `$white` |
| Body secondary | Inter | 14px | normal | `$light-gray` |
| Placeholder | Inter | 14px | normal | `$muted` |
| Helper / caption | Inter | 12px | normal | `$muted` |
| Code / numbers | Poppins | varies | 500 | varies |
| Chinese text | Noto Sans SC | varies | 400 | varies |
| Badge / system text | Poppins | 12px | 600 | varies |

### Spacing

| Token | Value |
|-------|-------|
| XS | 4px |
| SM | 8px |
| MD | 16px |
| LG | 24px |
| XL | 32px |
| XXL | 36px |

### Border Radius

| Token | Value | Usage |
|-------|-------|-------|
| SM | 4px | Checkbox, small elements |
| MD | 8px | Buttons, inputs, tabs |
| LG | 12px | Cards, dialogs, tables |
| XL | 21px | Dialog, sheet |
| Pill | 50px | Badges, switches, progress bars |

## Composite Component Patterns

### Table with data columns

```json
{
  "type": "frame",
  "name": "Table",
  "clip": true,
  "width": "fill_container",
  "fill": "#222222",
  "cornerRadius": 12,
  "stroke": { "thickness": 1, "fill": "#333333" },
  "layout": "vertical",
  "children": [
    {
      "type": "frame",
      "name": "tableHeader",
      "width": "fill_container",
      "fill": "#333333",
      "padding": [12, 16],
      "children": [
        {
          "type": "frame",
          "name": "headerCells",
          "width": "fill_container",
          "gap": 16,
          "children": [
            { "type": "text", "name": "colName", "fill": "#FFFFFF", "content": "Name", "fontFamily": "Inter", "fontSize": 14, "fontWeight": "500", "width": "fill_container" }
          ]
        }
      ]
    },
    {
      "type": "frame",
      "name": "tableBody",
      "width": "fill_container",
      "layout": "vertical",
      "children": [
        {
          "type": "frame",
          "name": "row1",
          "width": "fill_container",
          "stroke": { "thickness": { "bottom": 1 }, "fill": "#333333" },
          "padding": [12, 16],
          "children": [
            {
              "type": "frame",
              "name": "rowCells",
              "width": "fill_container",
              "gap": 16,
              "children": [
                { "type": "text", "name": "cellName", "fill": "#DCDCDC", "content": "Sample data", "fontFamily": "Inter", "fontSize": 14, "fontWeight": "normal", "width": "fill_container" }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

### Form field (Input/Group)

```json
{
  "type": "frame",
  "name": "fieldName",
  "width": "fill_container",
  "layout": "vertical",
  "gap": 8,
  "children": [
    { "type": "text", "name": "fieldLabel", "fill": "#FFFFFF", "content": "Field Label / 字段标签", "fontFamily": "Inter", "fontSize": 14, "fontWeight": "500" },
    {
      "type": "frame",
      "name": "fieldInput",
      "width": "fill_container",
      "fill": "#222222",
      "cornerRadius": 8,
      "stroke": { "thickness": 1, "fill": "#8E8E8E" },
      "padding": [12, 16],
      "alignItems": "center",
      "children": [
        { "type": "text", "name": "fieldPlaceholder", "fill": "#8E8E8E", "content": "Enter value...", "fontFamily": "Inter", "fontSize": 14, "fontWeight": "normal" }
      ]
    }
  ]
}
```

### Action button bar

```json
{
  "type": "frame",
  "name": "actionBar",
  "width": "fill_container",
  "gap": 12,
  "justifyContent": "end",
  "children": [
    {
      "type": "frame",
      "name": "cancelBtn",
      "cornerRadius": 8,
      "stroke": { "thickness": 1, "fill": "#8E8E8E" },
      "padding": [12, 24],
      "justifyContent": "center",
      "alignItems": "center",
      "children": [
        { "type": "text", "name": "cancelLabel", "fill": "#FFFFFF", "content": "Cancel / 取消", "fontFamily": "Inter", "fontSize": 14, "fontWeight": "500" }
      ]
    },
    {
      "type": "frame",
      "name": "submitBtn",
      "fill": "#BBFD3B",
      "cornerRadius": 8,
      "padding": [12, 24],
      "justifyContent": "center",
      "alignItems": "center",
      "children": [
        { "type": "text", "name": "submitLabel", "fill": "#00000E", "content": "Submit / 提交", "fontFamily": "Inter", "fontSize": 14, "fontWeight": "500" }
      ]
    }
  ]
}
```
