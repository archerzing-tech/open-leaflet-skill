# 3D Buildings with Leaflet + OSMBuildings

## Goal
- 实现 f4map.com 风格的 3D 建筑视觉效果（可见侧面墙壁），使用 Leaflet + Canvas 渲染确保截图稳定

## Constraints
- 所有 HTML 文件使用本地 `assets/lib/` 中的 Leaflet 1.9.4 + OSMBuildings-Leaflet.js（禁止 CDN）
- 建筑数据源使用 f4map Buildings Tile API（`buildings.f4map.com`）获取实时 OSM 建筑数据，不依赖本地 GeoJSON
- 截图必须在沙箱环境中稳定获取

## Solution
使用 **OSMBuildings Classic 2.5D**（`OSMBuildings-Leaflet.js`）作为渲染引擎：
- Canvas 2D 渲染（非 SVG），截图不再超时
- 自带透视投影，建筑墙壁可见、有屋顶颜色区分
- 数据源：f4map API → 转换 GeoJSON → `osmb.set(geoJSON)` 渲染

将 f4map 建筑数据转换为 OSMBuildings 所需的 GeoJSON FeatureCollection：
- `geometry.coordinates`: [lng, lat] 多边形（首尾闭合）
- `properties.height`: 建筑高度 (m)
- `properties.wallColor`: 按高度渐变色（绿→黄→橙→红）
- `properties.roofColor`: wallColor 加亮 40

### 文件
| 文件 | 坐标 | Zoom |
|------|------|------|
| `assets/examples/shanghai-3d.html` | 上海陆家嘴 [31.241, 121.500] | 16 |
| `assets/examples/hongkong-3d.html` | 香港中环 [22.319, 114.169] | 16 |
| `assets/examples/shenzhen-3d.html` | 深圳福田 [22.543, 114.058] | 16 |
| `assets/lib/OSMBuildings-Leaflet.js` | OSMBuildings v0.2.2b Leaflet 插件 | - |

### 截图
| 截图 | 大小 |
|------|------|
| `pics/screenshot-shanghai-3d.png` | 33K |
| `pics/screenshot-hongkong-3d.png` | 1.4M |
| `pics/screenshot-shenzhen-3d.png` | 771K |

## Key Decisions
- OSMBuildings-Leaflet.js v0.2.2b 已存在于 `assets/lib/`，直接使用
- 放弃 CDN 引用（OSMBuildings.org CDN 返回 403）
- 放弃 OSMBuildings 自有数据源（data.osmbuildings.org 需要 API key）
- f4map Buildings Tile API 有 CORS header，可直接在浏览器中跨域调用
- 禁用阴影（`shadows: false`）提升性能和截图一致性

## 截图不超时原因
- OSMBuildings 使用 Canvas 渲染，浏览器截图工具能快速捕获 Canvas 内容
- 相比之前手写的 SVG polygon 挤出（~16000+ SVG path），Canvas 渲染效率大幅提升
