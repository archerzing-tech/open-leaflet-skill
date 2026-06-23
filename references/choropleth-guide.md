# Leaflet 交互式 Choropleth 地图教程

来源：Leaflet 官方教程

## 基本结构

```javascript
var map = L.map('map').setView([37.8, -96], 4);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19
}).addTo(map);

L.geoJson(statesData).addTo(map);
```

## 配色函数

```javascript
function getColor(d) {
  return d > 1000 ? '#800026' :
         d > 500  ? '#BD0026' :
         d > 200  ? '#E31A1C' :
         d > 100  ? '#FC4E2A' :
         d > 50   ? '#FD8D3C' :
         d > 20   ? '#FEB24C' :
         d > 10   ? '#FED976' :
                    '#FFEDA0';
}
```

## 样式函数

```javascript
function style(feature) {
  return {
    fillColor: getColor(feature.properties.density),
    weight: 2,
    opacity: 1,
    color: 'white',
    dashArray: '3',
    fillOpacity: 0.7
  };
}
```

## 高亮交互

```javascript
function highlightFeature(e) {
  var layer = e.target;
  layer.setStyle({
    weight: 5, color: '#666',
    dashArray: '', fillOpacity: 0.7
  });
  layer.bringToFront();
}

function resetHighlight(e) {
  geojson.resetStyle(e.target);
}

function zoomToFeature(e) {
  map.fitBounds(e.target.getBounds());
}
```

## 信息控件

```javascript
var info = L.control();

info.onAdd = function(map) {
  this._div = L.DomUtil.create('div', 'info');
  this.update();
  return this._div;
};

info.update = function(props) {
  this._div.innerHTML = '<h4>标题</h4>' + (props ?
    '<b>' + props.name + '</b><br />' + props.value
    : '悬停查看');
};

info.addTo(map);
```

## 图例控件

```javascript
var legend = L.control({position: 'bottomright'});

legend.onAdd = function(map) {
  var div = L.DomUtil.create('div', 'info legend'),
      grades = [0, 10, 20, 50, 100, 200, 500, 1000];

  for (var i = 0; i < grades.length; i++) {
    div.innerHTML +=
      '<i style="background:' + getColor(grades[i] + 1) + '"></i> ' +
      grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
  }
  return div;
};

legend.addTo(map);
```

## CSS 样式

```css
.info {
  padding: 6px 8px;
  font: 14px/16px Arial, Helvetica, sans-serif;
  background: white;
  background: rgba(255,255,255,0.8);
  box-shadow: 0 0 15px rgba(0,0,0,0.2);
  border-radius: 5px;
}
.info h4 { margin: 0 0 5px; color: #777; }
.legend { line-height: 18px; color: #555; }
.legend i { width: 18px; height: 18px; float: left; margin-right: 8px; opacity: 0.7; }
```
