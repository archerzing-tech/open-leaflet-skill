# Leaflet 最佳实践与性能优化

## 性能优化

### 大量标记点处理
对于 1000+ 标记点：

1. **仅渲染可见区域**：监听 `moveend` 事件，只渲染当前视口内的标记
   ```javascript
   map.on('moveend', function() {
     var bounds = map.getBounds();
     markers.forEach(function(m) {
       if (bounds.contains(m.getLatLng())) {
         map.addLayer(m);
       } else {
         map.removeLayer(m);
       }
     });
   });
   ```

2. **使用 Canvas 渲染**：地图初始化时设置 `preferCanvas: true`
   ```javascript
   var map = L.map('map', { preferCanvas: true });
   ```

3. **标记聚类**：使用 `leaflet.markercluster` 插件

### GeoJSON 性能
- 大数据集（>10,000 个 feature）使用 TopoJSON 格式
- 简化几何减少坐标点数量
- 使用 `L.geoJSON()` 的 `filter` 只加载需要的 feature

## 常见模式

### 中国地图坐标偏移处理
中国地图服务（高德、百度等）使用 GCJ-02 坐标系，与 WGS-84 存在偏移。使用 OpenStreetMap 瓦片时使用 WGS-84。

### 多图层管理
```javascript
var baseMaps = {
  "OpenStreetMap": osmLayer,
  "卫星图": satelliteLayer
};
var overlayMaps = {
  "标记": markerLayer,
  "省份": provinceLayer
};
L.control.layers(baseMaps, overlayMaps).addTo(map);
```

### 交互高亮（悬停/点击）
```javascript
function hoverStyle(layer) {
  layer.setStyle({ weight: 4, color: '#ff0', fillOpacity: 0.5 });
  layer.bringToFront();
}
function normalStyle(layer) { geojsonLayer.resetStyle(layer); }
```

### 地图自适应
```javascript
// 页面resize时
window.addEventListener('resize', function() {
  map.invalidateSize();
});

// 缩放至所有layer的范围
var group = L.featureGroup([layer1, layer2, ...]);
map.fitBounds(group.getBounds().pad(0.1));
```

## 常用插件
- **leaflet-markercluster**：标记聚类
- **leaflet-draw**：绘图工具
- **leaflet-heat**：热力图
- **leaflet-search**：搜索功能
- **Leaflet.NonTiledLayer**：WMS 图层

## 瓦片缓存策略

### 浏览器 HTTP 缓存
浏览器会自动缓存瓦片（OSM 瓦片默认 `Cache-Control: max-age=86400`）。设置 `crossOrigin: 'anonymous'` 可启用更激进的缓存策略。

### keepBuffer 预加载
`keepBuffer: 8` 让 Leaflet 在视口外额外保留 8 组瓦片，用户拖动时无需等待加载：

```javascript
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  keepBuffer: 8,
  updateWhenZooming: false  // 缩放时不重新请求，用已有瓦片过渡
}).addTo(map);
```

### GeoJSON 数据缓存（localStorage）
```javascript
function cachedFetch(key, url, ttl) {
  ttl = ttl || 86400000; // 默认 24h
  var c = localStorage.getItem(key);
  if (c && Date.now() - JSON.parse(c).time < ttl) {
    return Promise.resolve(JSON.parse(c).data);
  }
  return fetch(url).then(function(r) { return r.json(); }).then(function(d) {
    localStorage.setItem(key, JSON.stringify({ data: d, time: Date.now() }));
    return d;
  });
}
```

### 预加载动画优化
```css
/* 加载时 crisp 防模糊，加载完 auto 用 GPU 渲染 */
.leaflet-tile { image-rendering: -webkit-optimize-contrast; image-rendering: crisp-edges; }
.leaflet-tile-loaded { image-rendering: auto; }
```

## 常见坑点
1. GeoJSON 的坐标顺序是 [经度, 纬度]，不是 [纬度, 经度]
2. 地图容器必须有固定高度（px 或 vh）
3. TileLayer 的 URL 模板参数顺序是 {z}/{x}/{y}
4. `invalidateSize()` 在容器尺寸变化后必须调用
