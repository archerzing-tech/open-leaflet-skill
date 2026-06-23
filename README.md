# open-leaflet-skill

基于自然语言描述生成交互式 Leaflet.js 地图 Web 组件的 Agent 技能。支持 2D 地图（GeoJSON、标记、特效）与 3D 建筑场景（OSM Buildings）。

## 使用方式

作为 [opencode](https://opencode.ai) Agent 技能，将 `SKILL.md` 和 `references/`、`data/`、`assets/` 置于 `~/.agents/skills/leaflet/` 目录下即可自动加载。直接对 Agent 说自然语言，例如：

> "把四川省高亮显示，用红色边框"  
> "显示上海陆家嘴的 3D 建筑地图"  
> "在成都标出宽窄巷子、锦里、熊猫基地三个景点"  
> "做一个中国各省人口分级统计图"

Agent 会自动生成可直接运行的独立 HTML 文件。

## 功能

- **2D 地图** — 定位、省份高亮、标记、弹窗、多边形、折线、图层控制
- **GeoJSON 数据** — 内置中国省级边界数据（`data/china_provinces.geojson`），支持 DataV.GeoAtlas / Overpass API 在线数据
- **3D 建筑场景** — 基于 OSMBuildings Classic 2.5D，建筑高度渐变着色 + 点击高亮 + 阴影开关
- **地图特效** — 遮罩（Mask）、发光（Glow）、脉动（Pulse）、蚂蚁线（Marching Ants）、颜色变换（Color Transform）
- **缓存优化** — localStorage GeoJSON 缓存（24h TTL）、keepBuffer 预加载
- **自适应嵌入** — ResizeObserver + iframe postMessage，支持嵌入任何页面

## 文件结构

```
leaflet/
├── SKILL.md                      # 技能主定义（Agent 加载入口）
├── README.md                     # 本文件
├── references/
│   ├── leaflet-quickstart.md     # Leaflet 快速入门
│   ├── geojson-guide.md          # GeoJSON 教程
│   ├── choropleth-guide.md       # 分级统计图教程
│   ├── api-reference.md          # Leaflet API 参考
│   ├── best-practices.md         # 性能优化与最佳实践
│   ├── data-sources.md           # 地理数据源（DataV, OSM, Overpass）
│   ├── effects-guide.md          # 地图特效指南
│   └── 3d-buildings-guide.md     # OSMBuildings 3D 建筑指南
├── data/
│   └── china_provinces.geojson   # 中国省级边界数据（34 省份）
└── assets/
    ├── leaf-demo.html            # 2D 演示：四川省高亮 + hover/click
    ├── leaf-effects.html         # 特效演示：遮罩/脉动/发光/蚂蚁线/色调
    └── leaf-3d-demo.html         # 3D 演示：上海/北京/成都/深圳 + 高度着色
```

## 使用示例

### 示例 1：省份高亮

```javascript
fetch('data/china_provinces.geojson')
  .then(r => r.json())
  .then(data => {
    var province = data.features.find(f => f.properties.name === '四川省');
    var layer = L.geoJSON(province, {
      style: { color: '#ff0000', weight: 3, fillColor: '#ff0000', fillOpacity: 0.3 }
    }).addTo(map);
    map.fitBounds(layer.getBounds());
  });
```

### 示例 2：多个标记点

```javascript
var points = [
  { name: '宽窄巷子', lat: 30.670, lng: 104.052 },
  { name: '锦里',     lat: 30.645, lng: 104.047 },
  { name: '熊猫基地', lat: 30.735, lng: 104.145 }
];
points.forEach(p => {
  L.marker([p.lat, p.lng]).addTo(map).bindPopup(p.name);
});
```

### 示例 3：3D 建筑场景

```javascript
var map = L.map('map', { center: [31.241, 121.500], zoom: 16,
  zoomControl: false, attributionControl: false });
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
  { maxZoom: 19, keepBuffer: 8 }).addTo(map);

var osmb = new OSMBuildings(map)
  .load('https://{s}.data.osmbuildings.org/0.2/59fcc2e8/tile/{z}/{x}/{y}.json');
osmb.style({ shadows: true });
osmb.each(function(f) {
  if (f.properties.height) {
    var t = Math.min(f.properties.height / 150, 1);
    f.properties.wallColor = 'rgb(' + Math.round(13 + 227 * t) + ','
      + Math.round(148 - 60 * t) + ',' + Math.round(136 - 106 * t) + ')';
  }
});
```

### 示例 4：鼠标悬停高亮

```javascript
function highlightFeature(e) {
  e.target.setStyle({ weight: 5, color: '#666', fillOpacity: 0.7 }).bringToFront();
}
function resetHighlight(e) { geojson.resetStyle(e.target); }
geojson = L.geoJSON(data, {
  style: { color: '#ff7800', weight: 2, fillOpacity: 0.3 },
  onEachFeature: function(feature, layer) {
    layer.on({ mouseover: highlightFeature, mouseout: resetHighlight });
  }
}).addTo(map);
```

## Demo

| 文件 | 功能 | 打开方式 |
|------|------|----------|
| `assets/leaf-demo.html` | 四川省高亮 + hover/click 交互 | 双击 / 本地 HTTP 服务 |
| `assets/leaf-effects.html` | 遮罩、脉动、发光、蚂蚁线、色调变换 | 同上 |
| `assets/leaf-3d-demo.html` | 4 城市 3D 建筑 + 高度着色 + 点击高亮 + 阴影 | 同上 |

## 数据源

- **中国行政区划**：阿里云 DataV.GeoAtlas `https://geo.datav.aliyun.com/areas_v3/bound/{adcode}_full.json`
- **全球数据**：OpenStreetMap Overpass API `https://overpass-api.de/api/interpreter`
- **3D 建筑**：OSMBuildings `https://{s}.data.osmbuildings.org/0.2/59fcc2e8/tile/{z}/{x}/{y}.json`
