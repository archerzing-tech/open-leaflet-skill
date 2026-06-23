# Leaflet + OSM Buildings 3D 建筑指南

## 概述

OSM Buildings Classic 2.5D 是一个将 OpenStreetMap 建筑数据渲染为 3D 建筑的 Leaflet 插件。它基于 OSM 中的 `building` 标签和 `height`/`building:levels` 等属性，自动生成建筑的三维几何体。

## 快速集成

### CDN 引用

```html
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="https://cdn.osmbuildings.org/classic/0.2.2b/OSMBuildings-Leaflet.js"></script>
```

### 最小示例

```javascript
var map = L.map('map').setView([52.51836, 13.40438], 16);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 18
}).addTo(map);

var osmb = new OSMBuildings(map)
  .load('https://{s}.data.osmbuildings.org/0.2/59fcc2e8/tile/{z}/{x}/{y}.json');
```

## API 参考

### 构造函数

| 方法 | 说明 |
|------|------|
| `new OSMBuildings(map)` | 初始化建筑图层 |
| `.load(url)` | 从瓦片服务器加载建筑数据 |
| `.set(geoJSON)` | 加载 GeoJSON FeatureCollection |
| `.style({...})` | 设置默认样式 |
| `.date(new Date(...))` | 设置阴影投影日期/时间 |
| `.each(fn)` | 遍历每个 feature，可修改或跳过 |
| `.click(fn)` | 建筑点击事件回调 |

### GeoJSON 属性（每个 building feature）

| 属性 | OSM 标签来源 | 说明 |
|------|-------------|------|
| `height` | `height` / `building:levels * 3` | 建筑高度（米），默认级别×3m |
| `minHeight` | `min_height` | 底部抬升高度 |
| `wallColor` | `building:colour` / `building:color` | 墙面颜色 |
| `roofColor` | `roof:colour` / `roof:color` | 屋顶颜色 |
| `material` | `building:material` / `building:facade:material` | 墙面材质 |
| `roofMaterial` | `roof:material` | 屋顶材质 |
| `shape` | `building:shape` | 建筑形状（`cylinder`/`sphere`）|
| `roofShape` | `roof:shape` | 屋顶形状（`dome`）|
| `roofHeight` | `roof:height` | 屋顶高度 |

### 样式方法

```javascript
// 默认建筑样式
osmb.style({
  color: 'rgb(220, 220, 220)',    // 墙面颜色（默认）
  roofColor: 'rgb(200, 200, 200)', // 屋顶颜色（默认）
  shadows: true                     // 是否显示阴影
});
```

### each 回调（高亮/筛选建筑）

```javascript
osmb.each(function(feature) {
  // feature.id: OSM element ID
  // feature.properties: { height, minHeight, wallColor, ... }

  // 高亮特定建筑
  if (feature.id === 12345) {
    feature.properties.wallColor = 'rgb(255, 0, 0)';
    feature.properties.roofColor = 'rgb(255, 200, 0)';
  }

  // 过滤掉某些建筑
  if (feature.properties.height < 5) {
    return false; // 跳过这个 feature
  }
});
```

### click 回调

```javascript
osmb.click(function(feature) {
  console.log('点击建筑:', feature);
  // feature.id
  // feature.properties
  // feature.geometry

  // 高亮点击的建筑
  feature.properties.wallColor = 'rgb(255, 0, 0)';
  osmb.set(feature); // 更新显示
});
```

## 加载自定义建筑 GeoJSON

```javascript
var building = {
  "type": "FeatureCollection",
  "features": [{
    "type": "Feature",
    "id": 1001,
    "geometry": {
      "type": "Polygon",
      "coordinates": [[
        [104.0665, 30.5728],
        [104.0675, 30.5728],
        [104.0675, 30.5735],
        [104.0665, 30.5735],
        [104.0665, 30.5728]
      ]]
    },
    "properties": {
      "wallColor": "rgb(255,0,0)",
      "roofColor": "rgb(200,200,200)",
      "height": 100,
      "minHeight": 0
    }
  }]
};

new OSMBuildings(map).set(building);
```

## 查询特定建筑的 OSM 数据

使用 Overpass API 获取特定建筑的 GeoJSON：

```bash
# 根据建筑名称查询（例如：成都天府广场）
curl "https://overpass-api.de/api/interpreter?data=[out:json];(way[\"building\"][\"name\"~\"天府广场\"](30.6,104.0,30.7,104.1););out geom;"
```

```javascript
// 在 JavaScript 中
var query = '[out:json];(way["building"]["name"~"成都"](30.5,104.0,30.7,104.2););out geom;';
fetch('https://overpass-api.de/api/interpreter?data=' + encodeURIComponent(query))
  .then(function(r) { return r.json(); })
  .then(function(osmData) {
    // 将 OSM JSON 转为 GeoJSON
    var geojson = convertOsmToGeoJSON(osmData);
    osmb.set(geojson);
  });
```

## 特定地点 3D 建筑加载

```javascript
function load3DBuildings(map, lat, lng, zoom) {
  map.setView([lat, lng], zoom || 16);
  var osmb = new OSMBuildings(map)
    .load('https://{s}.data.osmbuildings.org/0.2/59fcc2e8/tile/{z}/{x}/{y}.json');
  return osmb;
}

// 使用示例：北京天安门
load3DBuildings(map, 39.9042, 116.3974, 16).style({ shadows: true });
```

## 性能优化

1. 限制缩放级别范围：OSMBuildings 建议 zoom 15-20
2. 使用 `keepBuffer` 预加载周边的建筑数据
3. 通过 `each()` 过滤掉低矮或不重要的建筑
4. 结合 Leaflet 的 `preferCanvas: true` 提升渲染性能

## CDN 资源

| 资源 | URL |
|------|-----|
| OSMBuildings CSS | `https://cdn.osmbuildings.org/classic/0.2.2b/OSMBuildings.css` |
| OSMBuildings Leaflet JS | `https://cdn.osmbuildings.org/classic/0.2.2b/OSMBuildings-Leaflet.js` |
| 建筑数据瓦片 | `https://{s}.data.osmbuildings.org/0.2/59fcc2e8/tile/{z}/{x}/{y}.json` |
| Leaflet | `https://unpkg.com/leaflet@1.9.4/dist/leaflet.js` |
