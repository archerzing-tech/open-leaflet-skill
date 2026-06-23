---
name: leaflet
description: Leaflet.js 地图技能——根据用户自然语言描述，调用 Leaflet API 生成交互式地图 Web 组件。支持地图定位、GeoJSON 加载、多边形高亮、标记、弹窗、热力图、图层控制等。
metadata:
  category: visualization
  trigger: 地图, map, leaflet, 定位, 高亮, 轮廓线, GEOJSON, 可视化, 地理, 省份, 边界
---

# Leaflet 地图技能

你是一位 Leaflet.js 地图专家。根据用户的自然语言描述，生成交互式地图 HTML 文件。

## 核心原则

1. **从本地 GeoJSON 数据查找地理信息**：`data/china_provinces.geojson` 包含全国所有省级行政区划（含港澳台），也支持独立文件 `data/taiwan.geojson`、`data/hongkong.geojson`、`data/macau.geojson` 按需加载
2. **生成独立 HTML 文件**：产出是自包含的 `.html` 文件（双击可打开，使用 CDN 加载 Leaflet）
3. **组件化 + 可嵌入**：每个 HTML 文件包含完整的 Leaflet 地图组件，**默认支持嵌入到任何页面或 iframe**
4. **事实验证先于假设**：涉及具体地理信息时，先搜索确认
5. **善用在线数据源**：优先使用 DataV.GeoAtlas API 获取实时数据，OSM Overpass API 获取全球数据

## 地图缓存与显示优化（所有生成的文件必须包含）

### 瓦片缓存与平滑渲染

```javascript
// 地图初始化：开启所有动画
var map = L.map('map', {
  center: [纬度, 经度],
  zoom: 级别,
  zoomControl: false,
  attributionControl: false,
  fadeAnimation: true,        // 瓦片淡入
  zoomAnimation: true,        // 缩放动画
  markerZoomAnimation: true,  // 标记缩放
  zoomAnimationThreshold: 4   // 跨级别动画阈值
});

// 底图：keepBuffer 预加载周边瓦片，平滑拖动
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  keepBuffer: 8,              // 周边额外缓存 8 组瓦片
  updateWhenZooming: false,   // 缩放时不重载，动画结束后再加载
  updateInterval: 100         // 拖动时瓦片更新间隔(ms)
}).addTo(map);
```

### CSS 瓦片渲染优化

```css
/* 加载中的瓦片用 crisp 保证清晰，加载完成后 auto 启用 GPU 平滑 */
.leaflet-tile { image-rendering: -webkit-optimize-contrast; image-rendering: crisp-edges; }
.leaflet-tile-loaded { image-rendering: auto; }
```

### GeoJSON 数据缓存（localStorage）

所有从网络加载的 GeoJSON 数据必须缓存到 localStorage，避免重复请求：

```javascript
var CACHE_KEY = 'map_geo_data';
function loadCachedGeo(url) {
  var cached = localStorage.getItem(CACHE_KEY);
  // 24 小时过期
  if (cached && Date.now() - JSON.parse(cached).time < 86400000) {
    return Promise.resolve(JSON.parse(cached).data);
  }
  return fetch(url)
    .then(function(r) { return r.json(); })
    .then(function(data) {
      localStorage.setItem(CACHE_KEY, JSON.stringify({ data: data, time: Date.now() }));
      return data;
    });
}
```

### 加载提示

数据加载期间显示加载状态，加载完成后移除或隐藏：

```html
<div id="map"><div class="loading">加载中...</div></div>
```

```css
.loading { position: absolute; top: 50%; left: 50%; transform: translate(-50%,-50%); z-index: 999; }
```

```javascript
// 数据渲染完成后移除
document.querySelector('.loading') && document.querySelector('.loading').remove();
// 加载失败时提示
document.querySelector('.loading') && (document.querySelector('.loading').textContent = '⚠️ 加载失败');
```

### 自适应嵌入规则（所有生成的文件必须遵守）

每个生成的 HTML 必须实现以下自适应机制：

```html
<style>
  html, body { margin: 0; padding: 0; height: 100%; }
  #map { width: 100%; height: 100%; min-height: 300px; }
</style>
<script>
// 1) ResizeObserver 监听容器尺寸变化（支持页面内嵌动态容器）
var ro = new ResizeObserver(function() { map.invalidateSize(); });
ro.observe(document.getElementById('map'));

// 2) window resize 兜底
window.addEventListener('resize', function() { map.invalidateSize(); });

// 3) iframe 场景：父页面 postMessage('resize') 后自适应
if (window !== window.top) {
  window.addEventListener('message', function(e) {
    if (e.data === 'resize') map.invalidateSize();
  });
}
</script>
```

使用方在父页面嵌入方式：
```html
<!-- 作为子容器嵌入 -->
<div style="width: 100%; height: 500px;">
  <object data="map.html" type="text/html" style="width:100%;height:100%"></object>
</div>

<!-- 或通过 iframe -->
<iframe src="map.html" style="width:100%;height:500px;border:0"></iframe>
<!-- 父窗口尺寸变化时通知子 iframe 自适应 -->
<script>
  document.querySelector('iframe').contentWindow.postMessage('resize', '*');
</script>
```

## 可用的 Leaflet API

### 地图初始化
```javascript
var map = L.map('map', {
  center: [纬度, 经度],
  zoom: 级别,
  zoomControl: false,
  attributionControl: false
});
```

### 底图瓦片（Tile Layer，缓存优化版）
```javascript
// OpenStreetMap（默认推荐，关闭 Leaflet 商标显示）
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  keepBuffer: 8,
  updateWhenZooming: false,
  updateInterval: 100
}).addTo(map);
```

### GeoJSON 加载与样式
```javascript
// 基础加载
L.geoJSON(data).addTo(map);

// 带样式
L.geoJSON(data, {
  style: function(feature) {
    return {
      color: '#ff7800',
      weight: 3,
      opacity: 0.8,
      fillColor: '#ffff00',
      fillOpacity: 0.4
    };
  },
  onEachFeature: function(feature, layer) {
    layer.bindPopup(feature.properties.name);
  }
}).addTo(map);
```

### 常用 API

| 功能 | 代码 |
|------|------|
| 定位并缩放 | `map.setView([lat, lng], zoom)` 或 `map.fitBounds(layer.getBounds())` |
| 标记点 | `L.marker([lat, lng]).addTo(map).bindPopup('内容')` |
| 圆形 | `L.circle([lat, lng], {radius: 1000, color: 'red'}).addTo(map)` |
| 多边形 | `L.polygon([[lat1,lng1],[lat2,lng2],...]).addTo(map)` |
| 折线 | `L.polyline([[lat1,lng1],[lat2,lng2],...]).addTo(map)` |
| 弹窗 | `L.popup().setLatLng([lat,lng]).setContent('内容').openOn(map)` |
| 重置样式 | `geojsonLayer.resetStyle(layer)` |
| 高亮样式 | `layer.setStyle({weight: 5, color: '#666', fillOpacity: 0.7})` |
| 置顶 | `layer.bringToFront()` |
| 图层控制 | `L.control.layers(baseMaps, overlayMaps).addTo(map)` |
| 自定义控件 | `L.control({position: 'topleft'}).onAdd = function(map) { ... }` |

## 工作流程

### 1. 理解用户需求
- 识别用户想要的地图操作类型（定位、高亮、标记、路径、区域等）
- 确定涉及的地理位置（省份、城市、经纬度等）

### 2. 查找地理数据

按优先级从高到低使用以下数据源：

#### 中国省级数据
- **首选**：本地 `data/china_provinces.geojson`（按 `properties.name` 匹配省名，含港澳台）
- **独立港澳台文件**：`data/taiwan.geojson`、`data/hongkong.geojson`、`data/macau.geojson`（香港 18 区 / 澳门 8 堂区）
- **最佳在线源**：`阿里云 DataV.GeoAtlas` → `https://geo.datav.aliyun.com/areas_v3/bound/{adcode}_full.json`
  - 全国：`https://geo.datav.aliyun.com/areas_v3/bound/100000_full.json`
  - 四川：`https://geo.datav.aliyun.com/areas_v3/bound/510000_full.json`
  - 支持省/市/区县三级，adcode 见 `references/data-sources.md`

#### 全球数据
- **自然地球**: `https://raw.githubusercontent.com/xyanmi/MapData/main/countries.geojson`
- **OpenStreetMap Overpass API**: `https://overpass-api.de/api/interpreter`
  - 用 Overpass QL 查询: `[out:json]; relation(OSM_ID); out geom;`
  - 先用 Nominatim 查 OSM ID: `https://nominatim.openstreetmap.org/search?q=地名&format=json`
- **OSM Boundaries**: `https://osm-boundaries.com/`
- 完整参考 → `references/data-sources.md`

### 3. 生成立即可用的 HTML
使用 `assets/leaf-demo.html` 作为模板，根据需求替换地图配置。
- 本地 GeoJSON 使用相对路径 `data/china_provinces.geojson`
- DataV API 使用完整 URL（无需下载，直接 fetch）
- 确保代码有 fallback 机制（数据加载失败时显示提示）

### 4. 验证
- 检查 HTML 文件是否完整
- 确认 Leaflet CSS/JS 引用正确（via CDN）
- 确认 GeoJSON 数据路径正确
- 测试：双击 HTML 文件在浏览器中打开

## 地图特效（effects）

所有生成的文件可根据需求添加以下特效。完整实现参考 `references/effects-guide.md` 和 `assets/leaf-effects.html`（后者可直接双击运行，含可视化开关控件）。

生成的地图 HTML 默认不含特效（保持简洁），根据用户需求选择添加。特效开关建议通过界面 checkbox 控制。

### 遮罩（Mask）
压暗非目标区域，突出显示指定区域。通过世界矩形挖洞实现：
```javascript
var b = targetLayer.getBounds().pad(0.3);
var world = [[-90, -180], [-90, 180], [90, 180], [90, -180]];
var hole = [[b.getSouth(), b.getWest()], [b.getNorth(), b.getWest()],
            [b.getNorth(), b.getEast()], [b.getSouth(), b.getEast()]];
L.polygon([world, hole], {
  fillColor: '#000', fillOpacity: 0.5, weight: 0, interactive: false
}).addTo(map);
```

### 发光 / 阴影（Glow & Shadow）
通过 SVG filter 实现：
```html
<svg style="position:absolute;width:0;height:0">
  <defs>
    <filter id="glow">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="shadow">
      <feDropShadow dx="2" dy="2" stdDeviation="3" flood-opacity="0.5"/>
    </filter>
  </defs>
</svg>
```
```css
.glow-polygon { filter: url(#glow); }
.shadow-path { filter: url(#shadow); }
```

### 脉动 / 呼吸（Pulse）
CSS 动画让标记/多边形周期缩放或透明度变化：
```css
@keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.4); } 100% { transform: scale(1); } }
@keyframes breathe { 0%, 100% { fill-opacity: 0.25; } 50% { fill-opacity: 0.55; } }
.pulse-dot { animation: pulse 1.5s ease-in-out infinite; }
.breathe { animation: breathe 2.5s ease-in-out infinite; }
```

### 蚂蚁线（Marching Ants）
虚线描边动画，用于选中区域标识：
```css
@keyframes dash-march { to { stroke-dashoffset: -24; } }
.marching-ants { stroke-dasharray: 12 6; animation: dash-march 0.6s linear infinite; }
```

### 颜色变换（Color Transform）
对底图应用 CSS filter：
```javascript
document.querySelector('.leaflet-tile-pane').style.filter = 'hue-rotate(150deg) saturate(0.7)';
// 或: grayscale(1) | sepia(0.5) | brightness(0.6) contrast(1.2)
```

### 控件控制
所有特效建议配合 toggle 控件实现开关：
```html
<label><input type="checkbox" id="chkEffect" checked> 特效名称</label>
<script>
document.getElementById('chkEffect').addEventListener('change', function() {
  // this.checked ? 开启 : 暂停
});
</script>
```

## 3D 建筑场景（OSM Buildings）

根据用户需求，可生成 3D 建筑地图。需要在页面中加载 OSMBuildings Classic 2.5D 作为 Leaflet 插件图层。

### CDN 引用

```html
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="https://cdn.osmbuildings.org/classic/0.2.2b/OSMBuildings-Leaflet.js"></script>
```

### 基础集成

```javascript
var osmb = new OSMBuildings(map)
  .load('https://{s}.data.osmbuildings.org/0.2/59fcc2e8/tile/{z}/{x}/{y}.json');

osmb.style({
  color: '#ddd',
  roofColor: '#ccc',
  shadows: true
});
```

### API

| 方法 | 说明 |
|------|------|
| `new OSMBuildings(map)` | 创建建筑图层并添加到地图 |
| `.load(url)` | 从瓦片服务器加载建筑数据 |
| `.set(geoJSON)` | 加载自定义 GeoJSON FeatureCollection |
| `.style({color, roofColor, shadows})` | 设置默认样式 |
| `.each(fn)` | 遍历每个 building feature，可修改属性或返回 `false` 跳过 |
| `.click(fn)` | 建筑点击事件回调，参数为 feature 对象 |

### 高度着色（height-based coloring）

```javascript
osmb.each(function(f) {
  if (f.properties.height) {
    f.properties.wallColor = heightColor(f.properties.height);
    f.properties.roofColor = heightColor(f.properties.height * 0.9);
  }
});
```

### 建筑点击高亮

```javascript
osmb.click(function(f) {
  osmb.each(function(f2) {
    f2.properties.wallColor = f2.id === f.id ? '#f59e0b' : defaultColor(f2.properties.height);
  });
  osmb.set(osmb._data);
});
```

### Overpass API 查询特定建筑

```javascript
var query = '[out:json];(way["building"]["name"~"建筑名"](lat1,lng1,lat2,lng2););out geom;';
fetch('https://overpass-api.de/api/interpreter?data=' + encodeURIComponent(query))
  .then(r => r.json())
  .then(osmData => { /* 转换 OSM JSON 为 GeoJSON 后调用 osmb.set() */ });
```

### 注意事项

- 推荐缩放级别 zoom 15-20
- OSMBuildings 使用全球建筑瓦片数据，城市地区数据丰富
- 需要底图（TileLayer）配合显示道路/地名
- `keepBuffer: 8` 同样适用，预加载周边建筑瓦片
- 中国区域建筑数据在主要城市（上海、北京、成都、深圳等）较完整

完整 3D 参考见 `references/3d-buildings-guide.md`，可直接运行的 3D 演示见 `assets/leaf-3d-demo.html`（含上海/北京/成都/深圳四城预设 + 建筑高度渐变着色 + 点击高亮 + 阴影开关）。

## 本地资料

| 文件 | 说明 |
|------|------|
| `references/leaflet-quickstart.md` | Leaflet 快速入门指南 |
| `references/geojson-guide.md` | GeoJSON 使用教程 |
| `references/choropleth-guide.md` | Choropleth（分级统计）地图教程 |
| `references/api-reference.md` | Leaflet API 参考摘要 |
| `references/best-practices.md` | Leaflet 最佳实践与性能优化 |
| `references/data-sources.md` | 地理数据源参考（DataV、OSM、Overpass API）|
| `references/effects-guide.md` | 地图特效指南（遮罩、发光、脉动、颜色变换）|
| `references/3d-buildings-guide.md` | 3D 建筑场景指南（OSM Buildings API + Overpass 查询） |
| `data/china_provinces.geojson` | 中国省级行政区划 GeoJSON 数据（含港澳台，~1MB） |
| `data/taiwan.geojson` | 台湾省边界 GeoJSON |
| `data/hongkong.geojson` | 香港特别行政区边界 GeoJSON（含 18 区） |
| `data/macau.geojson` | 澳门特别行政区边界 GeoJSON（含 8 堂区） |
| `assets/leaf-demo.html` | 默认演示 HTML（四川省高亮） |
| `assets/leaf-effects.html` | 特效演示 HTML（遮罩、脉动、发光、蚂蚁线等） |
| `assets/leaf-3d-demo.html` | 3D 建筑演示 HTML（4 城市预设 + 高度着色 + 点击高亮） |

## 常见用例模板

### 用例 1：定位到省份并高亮
**用户说：** "把四川省高亮显示，用红色边框"
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

### 用例 2：景点标记
**用户说：** "在成都标出宽窄巷子、锦里、熊猫基地三个景点，点击弹窗显示名称"
```javascript
var markers = [
  { name: '宽窄巷子', lat: 30.670, lng: 104.052 },
  { name: '锦里',     lat: 30.645, lng: 104.047 },
  { name: '熊猫基地', lat: 30.735, lng: 104.145 }
];
markers.forEach(function(p) {
  L.marker([p.lat, p.lng]).addTo(map).bindPopup('<b>' + p.name + '</b>');
});
```

### 用例 3：鼠标悬停高亮
**用户说：** "加载全国省份数据，鼠标划过省份时高亮，移出恢复"
```javascript
function highlightFeature(e) {
  var layer = e.target;
  layer.setStyle({ weight: 5, color: '#666', fillOpacity: 0.7 });
  layer.bringToFront();
}
function resetHighlight(e) { geojson.resetStyle(e.target); }
geojson = L.geoJSON(data, {
  style: style,
  onEachFeature: function(feature, layer) {
    layer.on({ mouseover: highlightFeature, mouseout: resetHighlight });
  }
}).addTo(map);
```

### 用例 4：3D 建筑场景（指定城市）
**用户说：** "显示上海的 3D 建筑地图，建筑高度用颜色区分"
```javascript
var map = L.map('map', { center: [31.241, 121.500], zoom: 16, zoomControl: false, attributionControl: false });
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19, keepBuffer: 8 }).addTo(map);
new ResizeObserver(function() { map.invalidateSize(); }).observe(document.getElementById('map'));

var osmb = new OSMBuildings(map)
  .load('https://{s}.data.osmbuildings.org/0.2/59fcc2e8/tile/{z}/{x}/{y}.json');
osmb.style({ shadows: true });
osmb.each(function(f) {
  if (f.properties.height) {
    var t = Math.min(f.properties.height / 150, 1);
    f.properties.wallColor = 'rgb(' + Math.round(13 + 227 * t) + ',' + Math.round(148 - 60 * t) + ',' + Math.round(136 - 106 * t) + ')';
  }
});
osmb.click(function(f) {
  osmb.each(function(f2) {
    f2.properties.wallColor = f2.id === f.id ? '#f59e0b' : (f2.properties.height ? 'rgb(' + Math.round(13 + 227 * Math.min(f2.properties.height / 150, 1)) + ',' + Math.round(148 - 60 * Math.min(f2.properties.height / 150, 1)) + ',' + Math.round(136 - 106 * Math.min(f2.properties.height / 150, 1)) + ')' : '#ddd');
  });
  osmb.set(osmb._data);
});
```

### 用例 5：分级统计图（Choropleth）
**用户说：** "做一个全国省份人口分级统计图，人口越多的省颜色越深"
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

### 用例 6：地图特效
**用户说：** "显示北京城区地图，加一个脉动标记在天安门位置，周围加发光圆圈"
```javascript
var pulseIcon = L.divIcon({
  className: 'pulse-dot',
  html: '<div style="width:16px;height:16px;background:#ff4444;border-radius:50%;box-shadow:0 0 8px #ff4444;"></div>',
  iconSize: [16, 16]
});
L.marker([39.9042, 116.3974], { icon: pulseIcon }).addTo(map);
L.circle([39.9042, 116.3974], {
  radius: 500, color: '#ff4444', fillColor: '#ff4444', fillOpacity: 0.1, weight: 2
}).addTo(map);
```
