# Leaflet 快速入门指南

来源：Leaflet 官方文档

## 1. 引入 Leaflet

```html
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
```

## 2. 创建地图容器

```html
<div id="map" style="height: 500px;"></div>
```

## 3. 初始化地图

```javascript
var map = L.map('map').setView([51.505, -0.09], 13);
```

## 4. 添加底图瓦片

```javascript
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);
```

## 5. 添加标记

```javascript
var marker = L.marker([51.5, -0.09]).addTo(map);
marker.bindPopup('<b>Hello!</b>').openPopup();
```

## 6. 添加圆形

```javascript
var circle = L.circle([51.508, -0.11], {
  color: 'red',
  fillColor: '#f03',
  fillOpacity: 0.5,
  radius: 500
}).addTo(map);
```

## 7. 添加多边形

```javascript
var polygon = L.polygon([
  [51.509, -0.08],
  [51.503, -0.06],
  [51.51, -0.047]
]).addTo(map);
```

## 8. 处理事件

```javascript
function onMapClick(e) {
  L.popup()
    .setLatLng(e.latlng)
    .setContent('点击位置: ' + e.latlng.toString())
    .openOn(map);
}
map.on('click', onMapClick);
```

## 完整 HTML 模板

```html
<!DOCTYPE html>
<html>
<head>
  <title>Leaflet 地图</title>
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <style>
    body { margin: 0; padding: 0; }
    #map { width: 100%; height: 100vh; }
  </style>
</head>
<body>
  <div id="map"></div>
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <script>
    var map = L.map('map').setView([39.9, 116.4], 5);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);
  </script>
</body>
</html>
```
