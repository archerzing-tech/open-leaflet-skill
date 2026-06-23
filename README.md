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
├── assets/
│   ├── leaf-demo.html            # 2D 演示：四川省高亮 + hover/click
│   ├── leaf-effects.html         # 特效演示：遮罩/脉动/发光/蚂蚁线/色调
│   ├── leaf-3d-demo.html         # 3D 演示：上海/北京/成都/深圳 + 高度着色
│   ├── leaf-card-demo.html       # 地图卡片演示：6 POI + 指标卡 + 3 种模式切换
│   └── examples/
│       ├── sichuan-highlight.html     # 案例1：四川省高亮 + 信息卡片
│       ├── chengdu-pois.html          # 案例2：成都景点图文卡片
│       ├── choropleth-population.html # 案例3：全国人口分级统计图
│       ├── screenshot-sichuan.png     # 案例1 截图
│       ├── screenshot-chengdu.png     # 案例2 截图
│       └── screenshot-choropleth.png  # 案例3 截图
```

## 使用案例

以下展示用户输入的自然语言描述 → Agent 生成的 HTML 效果截图 → 核心代码。

### 案例 1：省份高亮 + 数据指标卡片

**用户说：** _"把四川省高亮显示，用红色边框，点击弹出省会成都的数据指标卡片"_

**效果：**

![sichuan-highlight](assets/examples/screenshot-sichuan.png)

**核心代码：**

```javascript
var CACHE_KEY = 'sichuan_example';
function loadCached(url) {
  var cached = localStorage.getItem(CACHE_KEY);
  if (cached && Date.now() - JSON.parse(cached).time < 86400000) {
    return Promise.resolve(JSON.parse(cached).data);
  }
  return fetch(url).then(function(r) { return r.json(); }).then(function(data) {
    localStorage.setItem(CACHE_KEY, JSON.stringify({ data: data, time: Date.now() }));
    return data;
  });
}

loadCached('data/china_provinces.geojson').then(function(data) {
  var sichuan = data.features.find(function(f) { return f.properties.name === '四川省'; });
  var layer = L.geoJSON(sichuan, {
    style: { color: '#dc2626', weight: 3, fillColor: '#fef2f2', fillOpacity: 0.3 }
  }).addTo(map);
  map.fitBounds(layer.getBounds().pad(0.2));

  layer.bindPopup(
    '<div class="map-card"><div class="map-card-body">' +
      '<h3>四川省</h3><div class="sub">中国西南 · 省会 成都市</div>' +
      '<div class="metric-row"><span class="metric-label">面积</span><span class="metric-value gold">48.6万 km²</span></div>' +
      '<div class="metric-row"><span class="metric-label">人口</span><span class="metric-value blue">8372万</span></div>' +
      '<div class="metric-row"><span class="metric-label">GDP</span><span class="metric-value gold">5.9万亿元</span></div>' +
    '</div></div>',
    { className: 'card-popup', maxWidth: 260 }
  );
});
```

**完整文件：** `assets/examples/sichuan-highlight.html`

---

### 案例 2：成都景点标记 + 图文卡片

**用户说：** _"在成都地图上标出宽窄巷子、锦里、熊猫基地、春熙路、九眼桥、天府广场六个景点，用自定义图标，点击显示带图片和标签的卡片"_

**效果：**

![chengdu-pois](assets/examples/screenshot-chengdu.png)

**核心代码：**

```javascript
var pois = [
  { lat: 30.670, lng: 104.063, name: '天府广场', sub: '市中心地标',
    desc: '成都市中心最大的广场...', img: 'https://picsum.photos/seed/cd-tianfu/400/200',
    tags: [{label:'地标',cls:'orange'},{label:'免费',cls:'green'}] },
  { lat: 30.645, lng: 104.047, name: '锦里古街', sub: '三国文化街区', ... },
  { lat: 30.735, lng: 104.145, name: '大熊猫基地', sub: '世界著名熊猫保护区', ... },
  { lat: 30.685, lng: 104.087, name: '春熙路', sub: '成都时尚商业街', ... },
  { lat: 30.700, lng: 104.045, name: '宽窄巷子', sub: '清代古街巷', ... },
  { lat: 30.620, lng: 104.070, name: '九眼桥', sub: '夜景酒吧街', ... }
];

pois.forEach(function(p) {
  var tagHtml = p.tags.map(function(t) {
    return '<span class="tag ' + (t.cls || '') + '">' + t.label + '</span>';
  }).join('');
  var html = '<div class="map-card">' +
    '<img class="map-card-img" src="' + p.img + '" />' +
    '<div class="map-card-body"><h3>' + p.name + '</h3>' +
    '<div class="sub">' + p.sub + '</div><p>' + p.desc + '</p>' +
    '<div class="tags">' + tagHtml + '</div></div></div>';
  L.marker([p.lat, p.lng])
    .addTo(map)
    .bindPopup(html, { className: 'card-popup', maxWidth: 320 });
});
```

**完整文件：** `assets/examples/chengdu-pois.html`

---

### 案例 3：全国人口分级统计图

**用户说：** _"用颜色表示各省人口密度，颜色越深人口越多，鼠标划过时显示省份名称和人口数量"_

**效果：**

![choropleth](assets/examples/screenshot-choropleth.png)

**核心代码：**

```javascript
function getColor(pop) {
  return pop > 8000 ? '#800026' : pop > 5000 ? '#BD0026'
       : pop > 3000 ? '#E31A1C' : pop > 1000 ? '#FC4E2A'
       : pop > 500  ? '#FD8D3C' : pop > 200  ? '#FEB24C'
       : '#FFEDA0';
}

function style(feature) {
  return { fillColor: getColor(feature.properties.population || 0),
           weight: 1, color: '#fff', fillOpacity: 0.85 };
}

var geojson = L.geoJSON(data, {
  style: style,
  onEachFeature: function(feature, layer) {
    layer.on({
      mouseover: function(e) {
        e.target.setStyle({ weight: 3, color: '#333', fillOpacity: 0.95 });
        info.update(feature.properties);
      },
      mouseout: function(e) { geojson.resetStyle(e.target); info.update(); }
    });
  }
}).addTo(map);
```

**完整文件：** `assets/examples/choropleth-population.html`

---

## Demo

| 文件 | 功能 | 打开方式 |
|------|------|----------|
| `assets/leaf-demo.html` | 四川省高亮 + hover/click 交互 | 双击 / 本地 HTTP 服务 |
| `assets/leaf-effects.html` | 遮罩、脉动、发光、蚂蚁线、色调变换 | 同上 |
| `assets/leaf-3d-demo.html` | 4 城市 3D 建筑 + 高度着色 + 点击高亮 + 阴影 | 同上 |
| `assets/leaf-card-demo.html` | 6 个 POI 卡片 + 省指标卡 + Card/Tooltip/Float 三模式 | 同上 |
| `assets/examples/sichuan-highlight.html` | 四川省高亮 + 成都数据指标卡片 | 同上 |
| `assets/examples/chengdu-pois.html` | 成都 6 景点图文卡片标记 | 同上 |
| `assets/examples/choropleth-population.html` | 全国人口分级统计 + hover 交互 | 同上 |

## 数据源

- **中国行政区划**：阿里云 DataV.GeoAtlas `https://geo.datav.aliyun.com/areas_v3/bound/{adcode}_full.json`
- **全球数据**：OpenStreetMap Overpass API `https://overpass-api.de/api/interpreter`
- **3D 建筑**：OSMBuildings `https://{s}.data.osmbuildings.org/0.2/59fcc2e8/tile/{z}/{x}/{y}.json`
- **地图卡片**：`references/tooltip-card-guide.md`（Popup 卡式化、浮动卡片、CSS、模板）
- **真实案例**：`references/real-world-examples.md`（实时追踪、热力图、MarkerCluster、搜索定位等）
