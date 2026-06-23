# open-leaflet-skill

基于自然语言描述生成交互式 Leaflet.js 地图 Web 组件的 Agent 技能。支持 2D 地图（GeoJSON、标记、特效）与 3D 建筑场景（OSM Buildings）。

## 适用 Agent

本技能兼容以下 Agent 工具：

- **[opencode](https://opencode.ai)** — 将本仓库 clone 或 symlink 到 `~/.agents/skills/leaflet/`，Agent 自动加载
- **[hermes](https://hermes.ai)** — 在 hermes 配置中指向本技能目录即可
- **[claude-code](https://claude.ai/code)** — 通过 `.claude/CLAUDE.md` 中引用本技能目录

## 使用方式

直接对 Agent 说自然语言描述，Agent 会自动理解需求并生成可直接运行的独立 HTML 文件：

> "把四川省高亮显示，用红色边框"  
> "显示上海陆家嘴的 3D 建筑地图"  
> "在成都标出宽窄巷子、锦里、熊猫基地三个景点"  
> "做一个全国人口分级统计图，按省份用颜色深浅表示"

Agent 会参考本技能的 `SKILL.md`、`references/` 中的指南、`data/` 中的 GeoJSON 数据以及 `assets/` 中的示例模板，生成符合规范的自包含 HTML 文件。

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
│   ├── 3d-buildings-guide.md     # OSMBuildings 3D 建筑指南
│   ├── tooltip-card-guide.md    # 地图卡片 / Tooltip 指南
│   └── real-world-examples.md   # 真实 Leaflet 案例参考（实时追踪、热力图、聚类等）
├── data/
│   ├── china_provinces.geojson   # 中国省级边界数据（34 省份 + 港澳台）
│   ├── taiwan.geojson            # 台湾省边界（独立文件）
│   ├── hongkong.geojson          # 香港特别行政区边界（含 18 区）
│   └── macau.geojson             # 澳门特别行政区边界（含 8 堂区）
└── assets/
    ├── leaf-demo.html            # 2D 演示：四川省高亮 + hover/click
    ├── leaf-effects.html         # 特效演示：遮罩/脉动/发光/蚂蚁线/色调
    ├── leaf-3d-demo.html         # 3D 演示：上海/北京/成都/深圳 + 高度着色
    └── leaf-card-demo.html       # 地图卡片演示：6 POI + 指标卡 + 3 种模式切换
```

## 自然语言示例

以下展示用户输入的自然语言描述，以及 Agent 生成的对应代码核心逻辑。

### 示例 1：省份高亮

**用户说：** _"把四川省高亮显示，用红色边框"_

**Agent 生成的 HTML 核心代码：**

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

**运行结果：** 地图自动缩放到四川省范围，红色边框 + 半透明红色填充，双击 `leaf-demo.html` 可查看。

### 示例 2：景点标记

**用户说：** _"在成都标出宽窄巷子、锦里、熊猫基地三个景点，点击弹窗显示名称"_

**Agent 生成的 HTML 核心代码：**

```javascript
var markers = [
  { name: '宽窄巷子', lat: 30.670, lng: 104.052 },
  { name: '锦里',     lat: 30.645, lng: 104.047 },
  { name: '熊猫基地', lat: 30.735, lng: 104.145 }
];
var markerLayers = [];
markers.forEach(function(p) {
  var m = L.marker([p.lat, p.lng]).addTo(map).bindPopup('<b>' + p.name + '</b>');
  markerLayers.push(m);
});
map.fitBounds(L.featureGroup(markerLayers).getBounds().pad(0.2));
```

### 示例 3：3D 建筑场景

**用户说：** _"显示上海陆家嘴的 3D 建筑地图，建筑高度用颜色区分"_

**Agent 生成的 HTML 核心代码：**

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

**运行结果：** 陆家嘴 3D 建筑群，低矮建筑青绿色、高层建筑金黄色渐变，双击 `leaf-3d-demo.html` 选择上海可查看。

### 示例 4：鼠标悬停高亮

**用户说：** _"加载全国省份数据，鼠标划过省份时高亮，移出恢复"_

**Agent 生成的 HTML 核心代码：**

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

### 示例 5：分级统计图（Choropleth）

**用户说：** _"做一个全国省份人口分级统计图，人口越多的省颜色越深"_

**Agent 生成的 HTML 核心代码：**

```javascript
fetch('data/china_provinces.geojson')
  .then(r => r.json())
  .then(data => {
    function getColor(pop) {
      return pop > 8000 ? '#800026' : pop > 5000 ? '#BD0026'
           : pop > 3000 ? '#E31A1C' : pop > 1000 ? '#FC4E2A'
           : pop > 500  ? '#FD8D3C' : pop > 200  ? '#FEB24C'
           : '#FFEDA0';
    }
    L.geoJSON(data, {
      style: function(f) {
        return { fillColor: getColor(f.properties.population || 0),
                 weight: 1, color: '#fff', fillOpacity: 0.8 };
      }
    }).addTo(map);
  });
```

### 示例 6：地图特效

**用户说：** _"显示北京城区地图，加一个脉动标记在天安门位置，周围加发光圆圈"_

**Agent 生成的 HTML 核心代码：**

```javascript
// 脉动标记
var pulseIcon = L.divIcon({
  className: 'pulse-dot',
  html: '<div style="width:16px;height:16px;background:#ff4444;border-radius:50%;box-shadow:0 0 8px #ff4444;"></div>',
  iconSize: [16, 16]
});
L.marker([39.9042, 116.3974], { icon: pulseIcon }).addTo(map);

// 发光圆圈
L.circle([39.9042, 116.3974], {
  radius: 500, color: '#ff4444', fillColor: '#ff4444', fillOpacity: 0.1, weight: 2
}).addTo(map);

// CSS 脉动动画
// @keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.5); } 100% { transform: scale(1); } }
// .pulse-dot { animation: pulse 1.5s ease-in-out infinite; }
```

更多特效（遮罩、蚂蚁线、颜色变换等）见 `assets/leaf-effects.html`。

## Demo

| 文件 | 功能 | 打开方式 |
|------|------|----------|
| `assets/leaf-demo.html` | 四川省高亮 + hover/click 交互 | 双击 / 本地 HTTP 服务 |
| `assets/leaf-effects.html` | 遮罩、脉动、发光、蚂蚁线、色调变换 | 同上 |
| `assets/leaf-3d-demo.html` | 4 城市 3D 建筑 + 高度着色 + 点击高亮 + 阴影 | 同上 |
| `assets/leaf-card-demo.html` | 6 个 POI 卡片 + 省指标卡 + Card/Tooltip/Float 三模式 | 同上 |

## 数据源

- **中国行政区划**：阿里云 DataV.GeoAtlas `https://geo.datav.aliyun.com/areas_v3/bound/{adcode}_full.json`
- **全球数据**：OpenStreetMap Overpass API `https://overpass-api.de/api/interpreter`
- **3D 建筑**：OSMBuildings `https://{s}.data.osmbuildings.org/0.2/59fcc2e8/tile/{z}/{x}/{y}.json`
- **地图卡片**：`references/tooltip-card-guide.md`（Popup 卡式化、浮动卡片、CSS、模板）
- **真实案例**：`references/real-world-examples.md`（实时追踪、热力图、MarkerCluster、搜索定位等）
