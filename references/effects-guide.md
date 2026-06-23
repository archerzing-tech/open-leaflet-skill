# Leaflet 地图特效指南

## 1. 遮罩（Mask）— 高亮目标区域，压暗背景

### 全屏遮罩 + 镂空高亮

在目标区域上方创建黑暗半透明遮罩层，使目标区域突出显示。

```javascript
// 创建遮罩：压暗全图，目标区域保持明亮
function createMask(targetLayer) {
  var bounds = targetLayer.getBounds().pad(0.3);
  // 世界范围矩形，逆时针坐标（遮罩外部）
  var worldCoords = [[-90, -180], [-90, 180], [90, 180], [90, -180]];
  // 目标边界（顺时针，形成镂空）
  var holeCoords = [
    [bounds.getSouthWest().lat, bounds.getSouthWest().lng],
    [bounds.getNorthWest().lat, bounds.getNorthWest().lng],
    [bounds.getNorthEast().lat, bounds.getNorthEast().lng],
    [bounds.getSouthEast().lat, bounds.getSouthEast().lng]
  ];

  var mask = L.polygon([worldCoords, holeCoords], {
    color: 'transparent',
    fillColor: '#000',
    fillOpacity: 0.55,
    weight: 0,
    interactive: false,
    pane: 'overlayPane'
  }).addTo(map);

  return mask;
}
```

### 简单遮罩（不镂空，适合过渡效果）

```javascript
L.rectangle(map.getBounds().pad(2), {
  color: '#000', weight: 0,
  fillColor: '#000', fillOpacity: 0.5,
  interactive: false
}).addTo(map);
```

## 2. 发光 / 阴影（Glow & Shadow）— 多边形外发光 / 投影

### SVG drop-shadow filter

```html
<svg style="position:absolute;width:0;height:0">
  <defs>
    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <filter id="shadow">
      <feDropShadow dx="2" dy="2" stdDeviation="3" flood-color="#000" flood-opacity="0.4"/>
    </filter>
  </defs>
</svg>
```

在 GeoJSON 样式中引用：

```javascript
style: {
  color: '#ff4444',
  weight: 2,
  fillColor: '#ff4444',
  fillOpacity: 0.25,
  className: 'glow-polygon'
}
```

```css
.glow-polygon { filter: url(#glow); }
.leaflet-overlay-pane svg path.shadow-path { filter: url(#shadow); }
```

### JS 动态发光

```javascript
function highlightGlow(layer) {
  layer.setStyle({ weight: 5, fillOpacity: 0.4 });
  layer.getElement() && layer.getElement().classList.add('glow-polygon');
}
```

## 3. 闪动 / 脉动（Pulse）— 标记或区域呼吸闪动

### CSS 脉动标记

```css
@keyframes pulse {
  0% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.3); opacity: 0.7; }
  100% { transform: scale(1); opacity: 1; }
}
@keyframes pulse-shadow {
  0% { box-shadow: 0 0 0 0 rgba(233,69,96,0.7); }
  50% { box-shadow: 0 0 0 12px rgba(233,69,96,0); }
  100% { box-shadow: 0 0 0 0 rgba(233,69,96,0); }
}
.pulse-icon {
  width: 16px; height: 16px;
  background: #e94560;
  border-radius: 50%;
  border: 2px solid #fff;
  animation: pulse 1.5s ease-in-out infinite, pulse-shadow 1.5s ease-in-out infinite;
}
```

```javascript
L.divIcon({
  className: '',
  html: '<div class="pulse-icon"></div>',
  iconSize: [16, 16]
});
```

### SVG 描边脉动（适用于多边形/折线）

```css
@keyframes dash-march {
  to { stroke-dashoffset: -20; }
}
.pulse-stroke {
  stroke-dasharray: 10;
  animation: dash-march 0.8s linear infinite;
}
```

应用：

```javascript
style: { color: '#ff0', weight: 4, dashArray: '10', className: 'pulse-stroke' }
```

### 多边形呼吸光晕

```css
@keyframes glow-pulse {
  0%, 100% { fill-opacity: 0.2; stroke-opacity: 0.8; }
  50% { fill-opacity: 0.5; stroke-opacity: 1; }
}
.breathing-polygon {
  animation: glow-pulse 2s ease-in-out infinite;
}
```

## 4. 颜色变换（Color Transform）

### Tile Layer CSS 滤镜

对整个地图底图应用色调/亮度/对比度变换：

```javascript
// 地图底图上叠加 CSS filter
map.getContainer().style.filter = 'hue-rotate(180deg) saturate(0.5) brightness(1.1)';
// 或者只对 tile pane 应用
document.querySelector('.leaflet-tile-pane').style.filter = 'sepia(0.3) hue-rotate(30deg)';
```

常用滤镜效果：

| 效果 | filter 值 |
|------|-----------|
| 灰度 | `grayscale(1)` |
| 暖色 | `sepia(0.4) hue-rotate(-10deg)` |
| 冷色 | `hue-rotate(150deg) saturate(0.7)` |
| 夜间 | `brightness(0.6) contrast(1.2) hue-rotate(180deg)` |
| 复古 | `sepia(0.6) saturate(0.5) brightness(0.9)` |
| 高对比 | `contrast(1.5) brightness(0.9)` |

### GeoJSON 动态着色

```javascript
// 根据属性着色
function getColor(value) {
  return value > 80 ? '#b10026' :
         value > 60 ? '#fc4e2a' :
         value > 40 ? '#feb24c' :
         value > 20 ? '#ffeda0' :
                      '#ffffcc';
}
L.geoJSON(data, {
  style: function(feature) {
    return { fillColor: getColor(feature.properties.value), fillOpacity: 0.7 };
  }
});
```

### 动画颜色渐变

```css
@keyframes color-shift {
  0% { fill: #e94560; }
  33% { fill: #0f3460; }
  66% { fill: #533483; }
  100% { fill: #e94560; }
}
.color-shift { animation: color-shift 6s ease-in-out infinite; }
```

## 5. 渐变填充（Gradient Fill）

Leaflet 的 SVG 渲染器支持渐变：

```html
<svg style="position:absolute;width:0;height:0">
  <defs>
    <linearGradient id="grad-red" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#ff4444"/>
      <stop offset="100%" stop-color="#ff8888"/>
    </linearGradient>
  </defs>
</svg>
```

```javascript
style: { fillColor: 'url(#grad-red)', fillOpacity: 0.6 }
```

## 6. 动画标记（Animated Marker）

### 弹跳标记

```css
@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}
.bounce-icon { animation: bounce 1s ease-in-out infinite; }
```

### CSS 旋转标记

```css
@keyframes spin { to { transform: rotate(360deg); } }
.spin-icon { animation: spin 3s linear infinite; }
```

## 7. 组合示例：脉动发光多边形 + 遮罩

```javascript
// 1) SVG filters
var svgFilters = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
svgFilters.setAttribute('style', 'position:absolute;width:0;height:0');
svgFilters.innerHTML = '<defs>' +
  '<filter id="glow"><feGaussianBlur stdDeviation="4" result="blur"/>' +
  '<feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>' +
  '</defs>';
document.body.appendChild(svgFilters);

// 2) 脉动多边形
<style>
@keyframes breathe {
  0%, 100% { fill-opacity: 0.3; stroke-opacity: 0.9; }
  50% { fill-opacity: 0.6; stroke-opacity: 1; }
}
.breathe { animation: breathe 2s ease-in-out infinite; filter: url(#glow); }
</style>

// 3) 应用
var target = L.geoJSON(feature, {
  style: { color: '#ff0', weight: 3, fillColor: '#ff0', fillOpacity: 0.3, className: 'breathe' }
}).addTo(map);

// 4) 遮罩
createMask(target);
```
