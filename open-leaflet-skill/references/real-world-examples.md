# Leaflet 真实案例参考

网上基于 Leaflet.js 构建的优秀项目与参考示例，按功能分类整理。后续接到类似需求时优先参考。

## 一、真实在线案例

### 实时交通追踪

- **MBTA Train Tracker** — 波士顿地铁实时位置追踪，每节车厢在地图上显示为 marker，通过 API 轮询更新。技术栈：Leaflet + MBTA v3 API + setInterval
  - 参考：https://www.namiraharis.com/MBTA-Train-Tracker/
  - 教程：https://www.storybench.org/your-first-interactive-map-with-leaflet-js/
- **leaflet-realtime** — 通用实时 GeoJSON 数据轮询插件，支持 AJAX/JSONP/WebSocket
  - GitHub：https://github.com/perliedman/leaflet-realtime
  - 适合场景：航班追踪、外卖骑手位置、共享单车实时分布

### 天气 / 气象

- **RainViewer** — 全球雷达降水地图，Leaflet + 雷达瓦片动画叠加层
  - 示例：https://jsfiddle.net/hwmz670c
- **USGS Earthquake Map** — 美国地质调查局实时地震数据，使用 Leaflet + USGS API + circle 表示震级
  - 参考：https://earthquake.usgs.gov/earthquakes/map/

### 热力图

- **Leaflet.heat** — Leaflet 官方热力图插件，基于 simpleheat，支持 10,000+ 点实时渲染
  - GitHub：https://github.com/Leaflet/Leaflet.heat
  - CDN：`https://unpkg.com/leaflet.heat@0.2.0/dist/leaflet-heat.js`
- **heatmap.js** — 基于 Canvas 的热力图，支持 Leaflet 图层
  - 示例：https://www.patrick-wied.at/static/heatmapjs/example-heatmap-leaflet.html

### 数据可视化 / 新闻地图

- **Leaflet Choropleth (USA Population)** — Leaflet 官方分级统计图教程，按人口密度着色
  - 教程：https://leafletjs.com/examples/choropleth/
- **BBC / NYT 新闻地图** — 新闻机构广泛使用 Leaflet + GeoJSON 做选举地图、疫情地图、灾害分布
  - 常见模式：按 feature 属性着色 + legend + hover 高亮 + 点击弹窗

### 地点 / POI 展示

- **Wikipedia Map** — 维基百科条目地理展示
- **OpenStreetMap** — 自己的各图层切换界面就基于 Leaflet
- **WordPress Leaflet Map** — 一款在 25,000+ 站点使用的 WordPress 地图插件
  - https://wordpress.org/plugins/leaflet-map/

---

## 二、重点参考的 Plugins

| 插件 | ⭐ 星 | 功能 | 适用需求 |
|------|-------|------|----------|
| **MarkerCluster** | 4.2k | 海量标记点聚类，带展开动画 | 成百上千个 POI 标注 |
| **Leaflet.heat** | 1.6k | Canvas 热力图 | 密度热区展示 |
| **Leaflet.Realtime** | 500+ | GeoJSON 实时更新 | 实时位置刷新 |
| **leaflet-velocity** | — | 风场/流线动画 | 气象数据可视化 |
| **Leaflet.GridLayer.GoogleMutant** | — | 在 Leaflet 中使用 Google 底图 | 需要卫星/混合图 |
| **Leaflet.fullscreen** | — | 全屏按键 | 需要全屏展示 |
| **Leaflet.Geoman** | — | 绘制/编辑几何图形 | 用户画线画面功能 |
| **Leaflet.Locate** | — | 定位用户当前位置 | "找附近"功能 |
| **Leaflet.CanvasLayer** | — | 自定义 Canvas 图层 | 逐帧动画渲染 |

> 完整插件列表：https://leafletjs.com/plugins.html（按功能分类：地图图层、覆盖层、交互、格式化、数据等）

---

## 三、常见需求实现模式

### 1. 海量点 + 聚类

```javascript
// 加载 MarkerCluster
// <script src="https://unpkg.com/leaflet.markercluster@1.4.1/dist/leaflet.markercluster.js"></script>
// <link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.4.1/dist/MarkerCluster.css" />

var mcg = L.markerClusterGroup({ chunkedLoading: true, maxClusterRadius: 50 });
// 批量添加 10000+ 点
points.forEach(function(p) {
  mcg.addLayer(L.marker([p.lat, p.lng]));
});
map.addLayer(mcg);
```

### 2. 热力图

```javascript
// 加载 leaflet.heat.js后：
var heatPoints = data.map(function(p) {
  return [p.lat, p.lng, p.intensity || 0.5];
});
L.heatLayer(heatPoints, {
  radius: 25, blur: 15, maxZoom: 17,
  gradient: { 0.4: 'blue', 0.6: 'lime', 0.8: 'yellow', 1.0: 'red' }
}).addTo(map);
```

### 3. 实时更新（每 N 秒拉取）

```javascript
function fetchData() {
  fetch('/api/points')
    .then(function(r) { return r.json(); })
    .then(function(data) {
      geoLayer.clearLayers();
      geoLayer.addData(data);
    });
}
setInterval(fetchData, 5000);
fetchData();
```

### 4. 搜索定位 + 飞入动画

```javascript
function searchAndFly(query) {
  fetch('https://nominatim.openstreetmap.org/search?q=' + encodeURIComponent(query) + '&format=json&limit=1')
    .then(function(r) { return r.json(); })
    .then(function(results) {
      if (results.length > 0) {
        var loc = results[0];
        map.flyTo([loc.lat, loc.lon], 14, { duration: 1.5 });
        L.marker([loc.lat, loc.lon]).addTo(map).bindPopup(loc.display_name).openPopup();
      }
    });
}
```

### 5. 暗色底图（夜间模式 / 仪表盘）

```javascript
// 使用 CartoDB 暗色瓦片
L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
  maxZoom: 19
}).addTo(map);

// 或 Stadia Alidade Dark
L.tileLayer('https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png', {
  maxZoom: 20
}).addTo(map);
```

### 6. 叠加热力图 + MarkerCluster

先聚合显示（低缩放级别显示聚类），放大后自动展示独立 marker + 热力：
```javascript
// 结合 L.LayerGroup.Conditional 或者分层控制
// 缩放 <= 13 用聚类，>= 14 用热力图
map.on('zoomend', function() {
  if (map.getZoom() <= 13) {
    map.removeLayer(heatLayer);
    map.addLayer(clusterGroup);
  } else {
    map.removeLayer(clusterGroup);
    map.addLayer(heatLayer);
  }
});
```

---

## 四、项目架构参考

### 小项目（单 HTML 文件）
- 所有代码在一个 HTML 中（CDN 加载 Leaflet + 插件）
- 适合：原型、演示、简单地图展示

### 中等项目（模块化）
```
src/
├── map.js              # 地图初始化 + 通用配置
├── layers/
│   ├── base.js         # 底图管理（明/暗/卫星切换）
│   ├── markers.js      # 标记 + 弹窗
│   └── geojson.js      # GeoJSON 加载 + 样式
├── controls/
│   ├── search.js       # 搜索控件
│   └── legend.js       # 图例
└── data/
    └── cache.js        # 数据缓存逻辑
```

### React 项目
- 推荐：react-leaflet (v4+)
- 参考：https://docs.maptiler.com/leaflet/examples/react/
- 核心：`<MapContainer>` → `<TileLayer>` → `<GeoJSON>` / `<Marker>` 组件

---

## 五、CDN 快速引用表

```html
<!-- Leaflet 1.x (推荐，稳定) -->
<link rel="stylesheet" href="./lib/leaflet.css" />
<script src="./lib/leaflet.js"></script>

<!-- Leaflet 2.0 alpha (ESM 模块，2025 年) -->
<script type="importmap">
  { "imports": { "leaflet": "https://unpkg.com/leaflet@2.0.0-alpha.1/dist/leaflet.js" } }
</script>

<!-- MarkerCluster -->
<link rel="stylesheet" href="https://unpkg.com/leaflet.markercluster@1.4.1/dist/MarkerCluster.css" />
<script src="https://unpkg.com/leaflet.markercluster@1.4.1/dist/leaflet.markercluster.js"></script>

<!-- Leaflet.heat -->
<script src="https://unpkg.com/leaflet.heat@0.2.0/dist/leaflet-heat.js"></script>

<!-- OSMBuildings (3D 建筑) -->
<link rel="stylesheet" href="https://cdn.osmbuildings.org/classic/0.2.2b/OSMBuildings.css" />
<script src="https://cdn.osmbuildings.org/classic/0.2.2b/OSMBuildings-Leaflet.js"></script>
```

## 六、设计建议

1. **不在地图上展示"关于"功能** — 信息弹窗 / 工具提示更为适用
2. **用户交互更为直接** — 在地图点击展示详细信息，并且可以使用侧边栏进行展示
3. **设计风格建议** — 根据场景选择底图主题——数据展示选择对比度较小的底图
4. **移动为先** — 保持控件的间距，支持触摸交互并提供滑动平移功能
5. **高性能** — 大量数据时使用聚类或热力图，而非逐个加载 marker
6. **数据缓存** — 所有非实时数据都应落入 localStorage（24h 过期机制）
7. **降级处理** — 网络异常时显示友好提示，并提供缓存数据的回退
