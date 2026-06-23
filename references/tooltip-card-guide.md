# Tooltip / Card 指南

在 Leaflet 地图上显示信息卡片（info card）。支持三种模式：内置 Popup 卡式化、内置 Tooltip 卡式化、自定义浮动卡片。

## 1. 卡式 Popup（点击弹出）

```javascript
var marker = L.marker([lat, lng]).addTo(map);
marker.bindPopup(
  '<div class="map-card">' +
    '<img class="map-card-img" src="https://..." alt="..." />' +
    '<div class="map-card-body">' +
      '<h3 class="map-card-title">Title</h3>' +
      '<p class="map-card-desc">Description text</p>' +
      '<span class="map-card-tag">Tag</span>' +
    '</div>' +
  '</div>',
  { className: 'card-popup', maxWidth: 320, minWidth: 240 }
);
```

```css
.leaflet-popup.card-popup .leaflet-popup-content-wrapper {
  padding: 0;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0,0,0,.15);
}
.leaflet-popup.card-popup .leaflet-popup-content {
  margin: 0;
  width: auto !important;
}
.leaflet-popup.card-popup .leaflet-popup-tip {
  box-shadow: none;
}
.map-card { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
.map-card-img {
  width: 100%; height: 140px; object-fit: cover;
  display: block;
}
.map-card-body { padding: 14px 16px 16px; }
.map-card-body h3 { margin: 0 0 6px; font-size: 16px; font-weight: 600; }
.map-card-body p { margin: 0 0 8px; font-size: 13px; color: #555; line-height: 1.5; }
.map-card-tag {
  display: inline-block; padding: 2px 8px; border-radius: 4px;
  font-size: 11px; font-weight: 500;
  background: #eef2ff; color: #4338ca;
}
```

---

## 2. 卡式 Tooltip（悬停弹出）

适合快速预览，鼠标悬浮时显示小卡片，移出自动隐藏。

```javascript
var marker = L.marker([lat, lng]).addTo(map);
marker.bindTooltip(
  '<div class="tooltip-card">' +
    '<strong>Title</strong><br/>' +
    '<span style="font-size:12px;color:#666;">Subtitle or short desc</span>' +
  '</div>',
  {
    direction: 'top',
    offset: [0, -10],
    className: 'card-tooltip',
    sticky: false
  }
);
```

```css
.leaflet-tooltip.card-tooltip {
  padding: 10px 14px;
  border: 0;
  border-radius: 8px;
  box-shadow: 0 3px 14px rgba(0,0,0,.12);
  font-size: 13px;
  line-height: 1.5;
  background: #fff;
}
.leaflet-tooltip-top.card-tooltip:before {
  border-top-color: #fff;
}
```

### Tooltip 选项

| 选项 | 说明 | 默认 |
|------|------|------|
| `direction` | 方向: `top`/`bottom`/`left`/`right`/`center` | `'auto'` |
| `offset` | 偏移 `[x, y]` | `[0, 0]` |
| `sticky` | 鼠标移入 feature 时才跟随 | `false` |
| `permanent` | 永久显示 | `false` |
| `opacity` | 透明度 | `0.9` |

---

## 3. 自定义浮动卡片（Custom Overlay）

使用 Leaflet 的 `map._container` 相对定位，在 JavaScript 中创建独立 DOM 卡片并通过 `map.latLngToContainerPoint()` 计算位置。支持任意复杂布局。

```css
.custom-card {
  position: absolute;
  z-index: 1000;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 8px 30px rgba(0,0,0,.18);
  width: 280px;
  overflow: hidden;
  pointer-events: auto;
  transition: opacity .2s, transform .2s;
  opacity: 0;
  transform: translateY(8px);
  pointer-events: none;
}
.custom-card.visible {
  opacity: 1;
  transform: translateY(0);
  pointer-events: auto;
}
.custom-card-img { width: 100%; height: 120px; object-fit: cover; display: block; }
.custom-card-body { padding: 12px 16px 16px; }
.custom-card-body h4 { margin: 0 0 4px; font-size: 15px; }
.custom-card-body p { margin: 0 0 8px; font-size: 13px; color: #555; }
.custom-card-footer { display: flex; gap: 8px; }
.custom-card-btn {
  padding: 6px 14px; border: 0; border-radius: 6px;
  font-size: 12px; font-weight: 500; cursor: pointer;
}
```

```javascript
var card = document.createElement('div');
card.className = 'custom-card';
card.innerHTML =
  '<img class="custom-card-img" src="..." />' +
  '<div class="custom-card-body">' +
    '<h4>Title</h4>' +
    '<p>Description</p>' +
    '<div class="custom-card-footer">' +
      '<button class="custom-card-btn" style="background:#2563eb;color:#fff;">Detail</button>' +
    '</div>' +
  '</div>';
document.getElementById('map').appendChild(card);

function showCard(latlng, content) {
  card.innerHTML = content;
  var point = map.latLngToContainerPoint(latlng);
  card.style.left = (point.x + 16) + 'px';
  card.style.top = (point.y - card.offsetHeight / 2) + 'px';
  card.classList.add('visible');
}

function hideCard() {
  card.classList.remove('visible');
}

// 在 marker 事件中使用
marker.on('mouseover', function() {
  showCard(marker.getLatLng(), '<img class="custom-card-img" src="..."/><div class="custom-card-body"><h4>Title</h4><p>Desc</p></div>');
});
marker.on('mouseout', hideCard);
```

---

## 4. 容器内边界约束

确保卡片不超出地图容器范围：

```javascript
function showCardConstrained(latlng, content) {
  card.innerHTML = content;
  var point = map.latLngToContainerPoint(latlng);
  var mapRect = document.getElementById('map').getBoundingClientRect();
  var cardW = 280, cardH = card.offsetHeight || 200;

  var left = point.x + 16;
  var top = point.y - cardH / 2;

  if (left + cardW > mapRect.width - 12) left = point.x - cardW - 16;
  if (top < 12) top = 12;
  if (top + cardH > mapRect.height - 12) top = mapRect.height - cardH - 12;

  card.style.left = Math.max(12, left) + 'px';
  card.style.top = Math.max(12, top) + 'px';
  card.classList.add('visible');
}
```

---

## 5. 卡片模板

### 图片 + 标题 + 描述

```javascript
function cardTemplate(img, title, desc, tags) {
  var tagHtml = (tags || []).map(function(t) {
    return '<span class="map-card-tag">' + t + '</span>';
  }).join(' ');
  return '<div class="map-card">' +
    (img ? '<img class="map-card-img" src="' + img + '" />' : '') +
    '<div class="map-card-body">' +
      '<h3>' + title + '</h3>' +
      (desc ? '<p>' + desc + '</p>' : '') +
      (tagHtml ? '<div style="display:flex;gap:4px;flex-wrap:wrap">' + tagHtml + '</div>' : '') +
    '</div>' +
  '</div>';
}
```

### 数据指标卡片

```javascript
function metricCard(title, metrics) {
  // metrics: [{ label: '人口', value: '2100万' }, ...]
  var rows = metrics.map(function(m) {
    return '<div style="display:flex;justify-content:space-between;padding:4px 0;border-bottom:1px solid #f0f0f0">' +
      '<span style="color:#666;font-size:13px">' + m.label + '</span>' +
      '<span style="font-weight:600;font-size:13px">' + m.value + '</span>' +
    '</div>';
  }).join('');
  return '<div class="map-card"><div class="map-card-body">' +
    '<h3 style="margin-bottom:8px">' + title + '</h3>' +
    rows +
  '</div></div>';
}
```

---

## 6. GeoJSON 中预置卡片内容

在 GeoJSON properties 中预置 `cardContent` 字段，Agent 自动生成时直接使用：

```javascript
onEachFeature: function(feature, layer) {
  if (feature.properties.cardContent) {
    layer.bindPopup(
      '<div class="map-card">' +
        '<div class="map-card-body">' +
          feature.properties.cardContent +
        '</div>' +
      '</div>',
      { className: 'card-popup', maxWidth: 300 }
    );
  }
}
```

---

## 7. 与特效组合

卡片可与地图特效（脉动标记、发光等）配合使用：

```javascript
// 脉动标记 + 点击弹出卡片
var icon = L.divIcon({
  className: 'pulse-dot',
  html: '<div style="width:14px;height:14px;background:#ef4444;border-radius:50%;"></div>',
  iconSize: [14, 14]
});
L.marker([lat, lng], { icon: icon })
  .addTo(map)
  .bindPopup(cardTemplate(img, title, desc, tags), { className: 'card-popup', maxWidth: 320 });
```
