# Leaflet API 参考摘要

来源：Leaflet 官方文档 (v1.9.4)

## 核心类

### L.Map
```javascript
// 创建
var map = L.map('mapId', { center, zoom, zoomControl, attributionControl, fadeAnimation, zoomAnimation });
// 方法
map.setView(center, zoom)          // 设置视图
map.fitBounds(bounds)              // 缩放至范围
map.getBounds()                    // 获取当前可视范围
map.getCenter()                    // 获取中心点
map.getZoom()                      // 获取缩放级别
map.invalidateSize()               // 容器大小变化时刷新
// 事件
map.on('click', fn)                // 点击事件
map.on('moveend', fn)              // 移动结束
map.on('zoomend', fn)              // 缩放结束
```

### 图层类

#### L.TileLayer - 瓦片底图
```javascript
L.tileLayer(urlTemplate, { maxZoom, attribution, subdomains }).addTo(map);
// URL模板: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
```

#### L.Marker - 标记
```javascript
var m = L.marker([lat, lng], { draggable, icon }).addTo(map);
m.bindPopup('content')            // 绑定弹窗
m.bindTooltip('content')           // 绑定提示
m.openPopup()                      // 打开弹窗
m.setLatLng([lat, lng])            // 改变位置
m.dragging.enable()                // 启用拖动
```

#### L.Popup - 弹窗
```javascript
L.popup({ maxWidth, className })
  .setLatLng([lat, lng])
  .setContent('html content')
  .openOn(map);
```

#### L.Circle - 圆形
```javascript
L.circle([lat, lng], { radius, color, fillColor, fillOpacity }).addTo(map);
```

#### L.Polygon - 多边形
```javascript
L.polygon([[lat,lng], [lat,lng], ...], { color, fillColor }).addTo(map);
```

#### L.Polyline - 折线
```javascript
L.polyline([[lat,lng], [lat,lng], ...], { color, weight }).addTo(map);
```

#### L.Rectangle - 矩形
```javascript
L.rectangle([[lat1,lng1], [lat2,lng2]], { color, weight }).addTo(map);
```

### L.GeoJSON - GeoJSON 图层
```javascript
L.geoJSON(data, { style, pointToLayer, onEachFeature, filter }).addTo(map);
layer.addData(moreData)            // 追加数据
layer.clearLayers()                // 清除
layer.resetStyle(target)           // 重置单个feature样式
```

## 控件类

```javascript
// 缩放控件
L.control.zoom({ position: 'topleft' }).addTo(map);
// 图层控制
L.control.layers(baseMaps, overlayMaps).addTo(map);
// 比例尺
L.control.scale({ imperial: false }).addTo(map);
// 自定义控件
L.control({ position }).onAdd = function(map) { return div; };
```

## 样式选项（Path options）

```javascript
{
  color: '#3388ff',         // 线条颜色
  weight: 3,                // 线宽
  opacity: 1.0,             // 线条透明度
  fillColor: '#3388ff',     // 填充颜色
  fillOpacity: 0.2,         // 填充透明度
  dashArray: null,          // 虚线 eg.'5,5'
  dashOffset: null,         // 虚线偏移
  lineCap: 'round',         // 端点形状
  lineJoin: 'round'         // 连接点形状
  className: ''             // CSS class
}
```

## 工具方法

```javascript
// 坐标转换
L.latLng(lat, lng)
L.latLngBounds(southWest, northEast)
L.point(x, y)
L.bounds(point1, point2)

// 实用工具
L.DomUtil.create(tagName, className, container)
L.DomEvent.on(el, events, fn)
L.DomEvent.stopPropagation(ev)

// 投影
L.CRS.EPSG3857     // Web Mercator (默认)
L.CRS.EPSG4326     // WGS84
L.CRS.EPSG3395     // 用于某些商业地图
```
