# Leaflet 中 GeoJSON 使用指南

来源：Leaflet 官方教程

## 什么是 GeoJSON

GeoJSON 是一种基于 JSON 的地理数据格式，支持：Point、LineString、Polygon、MultiPoint、MultiLineString、MultiPolygon、GeometryCollection。

**注意**：GeoJSON 使用 (经度, 纬度) 顺序，Leaflet 使用 (纬度, 经度) 顺序。

## 基本用法

```javascript
var geojsonFeature = {
  "type": "Feature",
  "properties": {
    "name": "某地点",
    "popupContent": "这里是说明"
  },
  "geometry": {
    "type": "Point",
    "coordinates": [104.0, 30.5]
  }
};

L.geoJSON(geojsonFeature).addTo(map);
```

## 样式设置

```javascript
// 统一样式
var myStyle = { color: '#ff7800', weight: 5, opacity: 0.65 };
L.geoJSON(myLines, { style: myStyle }).addTo(map);

// 基于属性动态样式
L.geoJSON(states, {
  style: function(feature) {
    switch (feature.properties.party) {
      case 'Republican': return { color: '#ff0000' };
      case 'Democrat':   return { color: '#0000ff' };
    }
  }
}).addTo(map);
```

## pointToLayer

自定义点标记的渲染方式：

```javascript
L.geoJSON(data, {
  pointToLayer: function(feature, latlng) {
    return L.circleMarker(latlng, {
      radius: 8,
      fillColor: '#ff7800',
      color: '#000',
      weight: 1,
      fillOpacity: 0.8
    });
  }
}).addTo(map);
```

## onEachFeature

为每个 feature 添加交互：

```javascript
L.geoJSON(data, {
  onEachFeature: function(feature, layer) {
    if (feature.properties && feature.properties.popupContent) {
      layer.bindPopup(feature.properties.popupContent);
    }
    layer.on({
      mouseover: function(e) { /* 高亮 */ },
      mouseout: function(e) { /* 重置 */ },
      click: function(e) { /* 缩放 */ }
    });
  }
}).addTo(map);
```

## filter

过滤 features：

```javascript
L.geoJSON(someFeatures, {
  filter: function(feature, layer) {
    return feature.properties.show_on_map;
  }
}).addTo(map);
```

## 异步加载 GeoJSON

```javascript
// 本地文件
fetch('data.geojson').then(r => r.json()).then(data => {
  L.geoJSON(data).addTo(map);
});

// 远程 URL
fetch('https://example.com/data.geojson').then(r => r.json()).then(data => {
  L.geoJSON(data).addTo(map);
});
```

## 中国省级 GeoJSON 数据

- 本地：`data/china_provinces.geojson`
- 字段：`properties.name` = 省名, `properties.adcode` = 行政区划代码
- 中心点：`properties.center` = [经度, 纬度]
