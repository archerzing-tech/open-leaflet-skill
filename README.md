# open-leaflet-skill

Agent skill for generating interactive Leaflet.js map HTML components from natural language descriptions. Supports 2D maps, 3D buildings (OSMBuildings), map card popups/tooltips, visual effects, and choropleth visualization with built-in China province GeoJSON data.

> **For the skill definition (agent consumption), see [`open-leaflet-skill/SKILL.md`](./open-leaflet-skill/SKILL.md).**  
> This README is for humans browsing the repository.

---

## Installation

### Prerequisites

- An AI agent that supports the [Agent Skills](https://agentskills.io) format (e.g., Claude Code, opencode, hermes, Cursor, Windsurf, or similar)
- Git

### Quick Install

Clone this repository into your agent's skills directory:

```bash
# Default skills directory for most agents
git clone https://github.com/archerzing-tech/open-leaflet-skill ~/.agents/skills/leaflet/
```

### Manual Install

If you prefer to place the skill elsewhere or don't use the default skills directory:

```bash
# Clone anywhere
git clone https://github.com/archerzing-tech/open-leaflet-skill

# Then configure your agent to point to the skill path.
# Most agents support a SKILL_PATH or similar config.
```

> ⚠️ **Important**: The skill root is the `open-leaflet-skill/` subdirectory inside this repo. When configuring your agent, make sure it points to `open-leaflet-skill/SKILL.md`.

### Verify Installation

After installation, verify the skill is available by checking:

```bash
ls ~/.agents/skills/leaflet/open-leaflet-skill/SKILL.md
```

Then ask your agent to "list available skills" — it should show **leaflet** (or **open-leaflet-skill**) in the list.

### Supported Agents

| Agent | Compatibility |
|-------|--------------|
| Claude Code | ✅ Full support — auto-loads `SKILL.md` from skill root |
| opencode | ✅ Full support |
| hermes | ✅ Full support |
| Cursor | ✅ Compatible (point to `open-leaflet-skill/SKILL.md`) |
| Windsurf | ✅ Compatible |

---

## Usage Examples

Send these prompts to your agent after the skill is installed:

> "把四川省高亮显示，用红色边框，点击弹出省会成都的数据指标卡片"  
> "显示上海陆家嘴的 3D 建筑场景"  
> "在成都标出宽窄巷子、锦里、熊猫基地三个景点，带图文卡片"  
> "做一个全国人口分级统计图，按省份用颜色深浅表示人口密度"

---

## Examples

### Province Highlight with Metric Card

![sichuan-highlight](pics/screenshot-sichuan.png)

Full file: [`open-leaflet-skill/assets/examples/sichuan-highlight.html`](./open-leaflet-skill/assets/examples/sichuan-highlight.html)

---

### Chengdu POIs with Image Cards

![chengdu-pois](pics/screenshot-chengdu.png)

Full file: [`open-leaflet-skill/assets/examples/chengdu-pois.html`](./open-leaflet-skill/assets/examples/chengdu-pois.html)

---

### Population Choropleth

![choropleth](pics/screenshot-choropleth.png)

Full file: [`open-leaflet-skill/assets/examples/choropleth-population.html`](./open-leaflet-skill/assets/examples/choropleth-population.html)

---

## Demos

| File | Description |
|------|-------------|
| `open-leaflet-skill/assets/leaf-demo.html` | Province highlight + hover/click interaction |
| `open-leaflet-skill/assets/leaf-effects.html` | Effects: mask, glow, pulse, marching ants, color transform |
| `open-leaflet-skill/assets/leaf-3d-demo.html` | 3D buildings (Shanghai/Beijing/Chengdu/Shenzhen) + height coloring |
| `open-leaflet-skill/assets/leaf-card-demo.html` | 6 POI cards + province metric card in 3 modes (popup/tooltip/float) |

---

## Directory Structure

```
open-leaflet-skill/                       # Project root
├── README.md                             # Project intro (this file)
├── pics/                                 # Screenshots for README
│   ├── screenshot-sichuan.png
│   ├── screenshot-chengdu.png
│   └── screenshot-choropleth.png
└── open-leaflet-skill/                   # Agent skill root (agentskills.io spec)
    ├── SKILL.md                          # Required: metadata + instructions
    ├── scripts/                          # Optional: executable code
    ├── references/                       # Optional: reference guides
    │   ├── leaflet-quickstart.md
    │   ├── geojson-guide.md
    │   ├── choropleth-guide.md
    │   ├── api-reference.md
    │   ├── best-practices.md
    │   ├── data-sources.md
    │   ├── effects-guide.md
    │   ├── 3d-buildings-guide.md
    │   ├── tooltip-card-guide.md
    │   └── real-world-examples.md
    └── assets/                           # Optional: static resources
        ├── leaf-demo.html
        ├── leaf-effects.html
        ├── leaf-3d-demo.html
        ├── leaf-card-demo.html
        ├── examples/
        │   ├── sichuan-highlight.html
        │   ├── chengdu-pois.html
        │   └── choropleth-population.html
        ├── data/                         # GeoJSON data
        │   ├── china_provinces.geojson
        │   ├── taiwan.geojson
        │   ├── hongkong.geojson
        │   └── macau.geojson
        └── lib/                          # Leaflet 1.9.4 (local, no CDN)
            ├── leaflet.css
            └── leaflet.js
```

## Data Sources

- **China administrative boundaries**: DataV.GeoAtlas `https://geo.datav.aliyun.com/areas_v3/bound/{adcode}_full.json`
- **Global data**: OpenStreetMap Overpass API `https://overpass-api.de/api/interpreter`
- **3D buildings**: OSMBuildings `https://{s}.data.osmbuildings.org/0.2/59fcc2e8/tile/{z}/{x}/{y}.json`
- **Placeholder images**: picsum.photos

## License

MIT
