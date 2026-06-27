---
name: open-leaflet-skill
description: Leaflet.js 地图技能——根据用户自然语言描述，调用 Leaflet API 生成交互式地图 Web 组件。支持地图定位、GeoJSON 加载、多边形高亮、标记、弹窗、热力图、图层控制等。
license: MIT
compatibility: Requires network access for map tiles (OpenStreetMap). GeoJSON data supports multiple channels (DataV, GeoJSON.cn, Tianditu, local files) optimized for China network environment. Generated HTML files need a browser to display maps.
metadata:
  category: visualization
  trigger: 地图, map, leaflet, 定位, 高亮, 轮廓线, GEOJSON, 可视化, 地理, 省份, 边界
---

# Leaflet 地图技能

你是一位 Leaflet.js 地图专家。根据用户的自然语言描述，生成交互式地图 HTML 文件。

## 核心原则

1. **从本地 GeoJSON 数据查找地理信息**（文件生成在 `assets/` 目录内时，路径用 `./data/`）：`./data/china_provinces.geojson` 包含全国所有省级行政区划（含港澳台），也支持独立文件 `./data/taiwan.geojson`、`./data/hongkong.geojson`、`./data/macau.geojson` 按需加载。也支持 `./data/geo-data.js` 通过 `GEO_DATA` 全局变量方式引入。
   - **多通道 fallback 策略**：推荐实现 DataV → GeoJSON.cn → 本地文件 → CDN 镜像的降级加载链，参见 `references/data-sources.md`
2. **生成独立 HTML 文件**：产出是自包含的 `.html` 文件（双击可打开，使用本地 `assets/lib/` 加载 Leaflet）。**文件必须生成在 `open-leaflet-skill/assets/` 目录内**（这样才能用正确相对路径 `./lib/leaflet.js` 引用 Leaflet）。如果用户指定其他输出路径，则将 `assets/lib/` 目录复制到输出目录同级。
3. **组件化 + 可嵌入**：每个 HTML 文件包含完整的 Leaflet 地图组件，**默认支持嵌入到任何页面或 iframe**
4. **事实验证先于假设**：涉及具体地理信息时，先搜索确认
5. **善用多通道数据源**：优先使用国内可访问的数据源（DataV.GeoAtlas、GeoJSON.cn、天地图），辅以本地预置文件和 CDN 镜像作为 fallback。完整参考 → `references/data-sources.md`

## 地图缓存与显示优化（所有生成的文件必须包含）

### Marker 点击边框去除

```css
.leaflet-marker-icon:focus,
.leaflet-marker-icon:focus-visible {
  outline: none !important;
  box-shadow: none !important;
}
```

### 瓦片动画平滑

```javascript
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  keepBuffer: 8,
  updateWhenZooming: false,
  updateInterval: 100
});
```

```css
.leaflet-tile { image-rendering: -webkit-optimize-contrast; image-rendering: crisp-edges; }
.leaflet-tile-loaded { image-rendering: auto; }
```

### GeoJSON 缓存（localStorage + 24h TTL）

```javascript
var CACHE_KEY = 'my_geojson_cache';
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
```

### 自适应嵌入（ResizeObserver）

```javascript
if (window.ResizeObserver) {
  new ResizeObserver(function() { map.invalidateSize(); }).observe(document.getElementById('map'));
}
window.addEventListener('resize', function() { map.invalidateSize(); });
```

### 加载提示

```html
<div id="map"><div class="loading" id="loading">加载中...</div></div>
```
```javascript
fetch(url).then(r => r.json()).then(data => {
  document.getElementById('loading').style.display = 'none';
}).catch(() => { document.getElementById('loading').textContent = '加载失败'; });
```

## 工作流程

### 1. 理解用户需求
- 识别地图操作类型（定位、高亮、标记、路径、区域等）
- 确定地理位置（省份、城市、经纬度等）

### 2. 查找地理数据

**中国省级数据**（优先级从高到低，多通道 fallback）：
1. 本地文件 `./data/china_provinces.geojson`（文件生成在 `assets/` 目录内时；按 `properties.name` 匹配）— **最快最稳，无需网络**
2. 独立文件：`./data/taiwan.geojson`、`./data/hongkong.geojson`、`./data/macau.geojson`
3. DataV.GeoAtlas（国内极快）：`https://geo.datav.aliyun.com/areas_v3/bound/{adcode}_full.json`
4. GeoJSON.cn（国内极快）：`https://geojson.cn/api/china/{adcode}.json`
5. jsDelivr CDN 镜像：`https://cdn.jsdelivr.net/gh/xyanmi/MapData@main/provinces.cn.geojson`

**全球数据**（国内可能受限，建议下载后本地使用）：
- geoBoundaries：`https://www.geoboundaries.org/` — CC BY 4.0 开放许可
- Overpass API：`https://overpass-api.de/api/interpreter` — 实时查询
- Nominatim（地名查询）：`https://nominatim.openstreetmap.org/search?q=地名&format=json`
- 自然地球（CDN 镜像）：`https://cdn.jsdelivr.net/gh/xyanmi/MapData@main/countries.geojson`

> 完整数据源参考 → `references/data-sources.md`（含 8 个渠道详解、坐标系转换、多通道 fallback 代码）

### 3. 生成立即可用的 HTML
- 使用 `assets/leaf-demo.html` 作为模板
- 本地 GeoJSON 用相对路径 `./data/china_provinces.geojson`（文件在 `assets/` 目录内时）
- 在线 API 用完整 URL（直接 fetch），推荐实现多通道 fallback：DataV → GeoJSON.cn → 本地文件 → CDN 镜像
- 必须有 fallback（数据加载失败时显示提示），参考 `references/data-sources.md` 中的 `loadGeoJSON` 函数
- **Leaflet 引用路径规则**：
  - 文件生成在 `assets/` 目录内：使用 `./lib/leaflet.js` 和 `./lib/leaflet.css`（与模板一致）
  - 文件生成在其他目录：使用相对于该目录的路径指向 `open-leaflet-skill/assets/lib/leaflet.js`，或将 `assets/lib/` 目录复制到输出目录同级后使用 `./lib/leaflet.js`
- ⚠️ **常见错误**：不要用 `assets/lib/leaflet.js` 或 `open-leaflet-skill/assets/lib/leaflet.js` 作为 HTML 内部引用路径——HTML 中的路径必须是相对于 HTML 文件自身的位置。路径写错会导致 `L is not defined` 错误。
- ⚠️ **`file://` 协议限制**：部分浏览器在 `file://` 协议下会因安全策略阻止跨域请求。如遇到 `'file:' URLs are treated as unique security origins` 错误，请通过本地 HTTP 服务器打开（如 `python3 -m http.server`）。生成 HTML 时确保 `<script src="..."></script>` 标签在同一行闭合，不要有换行。

### 4. 验证
- HTML 文件是否完整
- Leaflet CSS/JS 引用正确
- GeoJSON 数据路径正确
- 双击 HTML 在浏览器中测试

## 地图特效

参考 `references/effects-guide.md` + `assets/leaf-effects.html`。支持：遮罩（Mask）、发光（Glow）、脉动（Pulse）、蚂蚁线（Marching Ants）、颜色变换（Color Transform）。默认不含特效，按需添加，建议用 checkbox 控制开关。

## 3D 建筑场景（f4map）

参考 `references/3d-buildings-guide.md` + `assets/examples/shanghai-3d.html`。使用 [f4map](https://f4map.com) Buildings Tile API 获取实时 OSM 建筑数据，用 Leaflet Polygon 挤出实现 3D 效果：

```html
<!-- 文件生成在 assets/ 目录内时 -->
<link rel="stylesheet" href="./lib/leaflet.css" />
<script src="./lib/leaflet.js"></script>
```

数据端点：`https://buildings.f4map.com/buildings/{z}/{x}/{y}.json?query={"maxage":43200,"straightSkeleton":1}`

`way` 字段格式（tile 局部坐标，65536 网格，增量编码）：
- `P((x1 y1,dx2 dy2,...))` — 多边形
- `M(((ring1)),((ring2)))` — 多多边形
- `N(x y)` — 点（跳过）

坐标转换（tile → lat/lng）：`lat = atan(sinh(π - (ty + cy/65536)/2^z * 2π)) * 180/π`，`lon = (tx + cx/65536)/2^z * 360 - 180`

3D 挤出：基座（地面）→ 墙面（连接基座和屋顶顶点）→ 屋顶（NE 偏移 `height * 0.000004`）

注意事项：使用 zoom 16 获取数据、缓存 `osm_id` 防重复、`keepBuffer: 8`、中国主要城市数据较完整。

## 地图卡片（Tooltip / Popup）

参考 `references/tooltip-card-guide.md` + `assets/leaf-card-demo.html`。支持三种模式：
1. **卡式 Popup**（点击弹出，`bindPopup` + CSS class `card-popup`）
2. **卡式 Tooltip**（悬停弹出，`bindTooltip` + CSS class `card-tooltip`）
3. **自定义浮动卡片**（`latLngToContainerPoint` 计算屏幕坐标，DOM 绝对定位）

## 本地资料

| 文件 | 说明 |
|------|------|
| `references/leaflet-quickstart.md` | Leaflet 快速入门指南 |
| `references/geojson-guide.md` | GeoJSON 使用教程 |
| `references/choropleth-guide.md` | Choropleth（分级统计）地图教程 |
| `references/api-reference.md` | Leaflet API 参考摘要 |
| `references/best-practices.md` | Leaflet 最佳实践与性能优化 |
| `references/data-sources.md` | 地理数据源参考（DataV、OSM、Overpass API）|
| `references/effects-guide.md` | 地图特效指南 |
| `references/3d-buildings-guide.md` | 3D 建筑场景指南 |
| `references/tooltip-card-guide.md` | 地图卡片 / Tooltip 指南 |
| `references/real-world-examples.md` | 真实 Leaflet 案例参考 |
| `assets/data/china_provinces.geojson` | 中国省级行政区划 GeoJSON（含港澳台） |
| `assets/data/taiwan.geojson` | 台湾省边界 |
| `assets/data/hongkong.geojson` | 香港 18 区边界 |
| `assets/data/macau.geojson` | 澳门 8 堂区边界 |
| `assets/leaf-demo.html` | 默认演示（四川省高亮） |
| `assets/leaf-effects.html` | 特效演示 |
| `assets/leaf-3d-demo.html` | 3D 建筑演示（上海/香港/重庆） |
| `assets/leaf-card-demo.html` | 地图卡片演示（6 POI + 3 模式） |
| `assets/examples/sichuan-highlight.html` | 案例：四川省高亮 + 指标卡片 |
| `assets/examples/chengdu-pois.html` | 案例：成都 6 景点图文卡片 |
| `assets/examples/choropleth-population.html` | 案例：全国人口分级统计图 |
| `assets/examples/shanghai-3d.html` | 案例：上海金茂中心 3D 直升机视角 |
| `assets/examples/hongkong-3d.html` | 案例：香港维多利亚港 3D 直升机视角 |
| `assets/examples/chongqing-3d.html` | 案例：重庆解放碑 3D 直升机视角 |

## 常见用例模板

### 用例 1：省份高亮（文件生成在 `assets/` 目录内时）
```javascript
fetch('./data/china_provinces.geojson').then(r => r.json()).then(data => {
  var province = data.features.find(f => f.properties.name === '四川省');
  var layer = L.geoJSON(province, { style: { color: '#ff0000', weight: 3, fillColor: '#ff0000', fillOpacity: 0.3 } }).addTo(map);
  map.fitBounds(layer.getBounds());
});
```

### 用例 2：景点标记
```javascript
L.marker([30.670, 104.052]).addTo(map).bindPopup('<b>宽窄巷子</b>');
L.marker([30.645, 104.047]).addTo(map).bindPopup('<b>锦里</b>');
L.marker([30.735, 104.145]).addTo(map).bindPopup('<b>熊猫基地</b>');
```

### 用例 3：悬停高亮
```javascript
function highlight(e) { e.target.setStyle({ weight: 5, color: '#666', fillOpacity: 0.7 }).bringToFront(); }
function reset(e) { geojson.resetStyle(e.target); }
L.geoJSON(data, { onEachFeature: (f, l) => l.on({ mouseover: highlight, mouseout: reset }) }).addTo(map);
```

### 用例 4：3D 建筑
```javascript
// 加载本地 3D 建筑数据
var xhr = new XMLHttpRequest();
xhr.open('GET', './data/3d/shanghai/buildings.json', true);
xhr.onload = function() {
  var data = JSON.parse(xhr.responseText);
  osmb.set(data);
  osmb.style({ shadows: true });
};
xhr.send();
```

### 用例 5：分级统计图
```javascript
function getColor(pop) { return pop > 8000 ? '#800026' : pop > 5000 ? '#BD0026' : pop > 3000 ? '#E31A1C' : pop > 1000 ? '#FC4E2A' : pop > 500 ? '#FD8D3C' : pop > 200 ? '#FEB24C' : '#FFEDA0'; }
L.geoJSON(data, { style: f => ({ fillColor: getColor(f.properties.population || 0), weight: 1, color: '#fff', fillOpacity: 0.8 }) }).addTo(map);
```

### 用例 6：地图特效
```javascript
var pulseIcon = L.divIcon({ className: 'pulse-dot', html: '<div style="width:16px;height:16px;background:#ff4444;border-radius:50%;box-shadow:0 0 8px #ff4444;"></div>', iconSize: [16, 16] });
L.marker([39.9042, 116.3974], { icon: pulseIcon }).addTo(map);
```
