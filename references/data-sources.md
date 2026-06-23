# 地理数据源参考

## 1. 阿里云 DataV.GeoAtlas（推荐·国内）

**URL**: https://datav.aliyun.com/tools/atlas/

DataV.GeoAtlas 提供中国各级行政区划边界数据，支持国/省/市/区县四级，数据来源于高德地图。

### 数据 API

所有数据可通过 HTTP GET 直接获取：

```bash
# 全国边界（包含省级边界）
https://geo.datav.aliyun.com/areas_v3/bound/100000_full.json

# 省级边界（例如四川省 510000）
# 省 + 市 + 区县完整层级
https://geo.datav.aliyun.com/areas_v3/bound/510000_full.json

# 省本级（不含下级）
https://geo.datav.aliyun.com/areas_v3/bound/510000.json

# 市级边界（例如成都市 510100）
https://geo.datav.aliyun.com/areas_v3/bound/510100_full.json
```

### 行政区划代码（adcode）

| 省份 | adcode |
|------|--------|
| 北京市 | 110000 |
| 天津市 | 120000 |
| 河北省 | 130000 |
| 山西省 | 140000 |
| 内蒙古 | 150000 |
| 辽宁省 | 210000 |
| 吉林省 | 220000 |
| 黑龙江 | 230000 |
| 上海市 | 310000 |
| 江苏省 | 320000 |
| 浙江省 | 330000 |
| 安徽省 | 340000 |
| 福建省 | 350000 |
| 江西省 | 360000 |
| 山东省 | 370000 |
| 河南省 | 410000 |
| 湖北省 | 420000 |
| 湖南省 | 430000 |
| 广东省 | 440000 |
| 广西 | 450000 |
| 海南省 | 460000 |
| 重庆市 | 500000 |
| 四川省 | 510000 |
| 贵州省 | 520000 |
| 云南省 | 530000 |
| 西藏 | 540000 |
| 陕西省 | 610000 |
| 甘肃省 | 620000 |
| 青海省 | 630000 |
| 宁夏 | 640000 |
| 新疆 | 650000 |
| 台湾省 | 710000 |
| 香港 | 810000 |
| 澳门 | 820000 |

完整 CSV: https://docs-aliyun.cn-hangzhou.oss.aliyun-inc.com/assets/attach/84544/cn_zh/1530167929977/%E7%9C%81%E5%B8%82%E5%8C%BAadcode%E4%B8%8E%E7%BB%8F%E7%BA%AC%E5%BA%A6%E6%98%A0%E5%B0%84%E8%A1%A8gbk.csv

### 使用示例（Leaflet）

```javascript
// 从 DataV API 加载四川省数据
fetch('https://geo.datav.aliyun.com/areas_v3/bound/510000_full.json')
  .then(r => r.json())
  .then(data => {
    L.geoJSON(data, {
      style: { color: '#ff0000', weight: 2, fillOpacity: 0.2 }
    }).addTo(map);
  });
```

## 2. OpenStreetMap Overpass API

**URL**: https://overpass-api.de/api/interpreter

用于从 OpenStreetMap 获取全球任意行政边界。使用 Overpass QL 查询语言。

### 查询行政边界示例

```bash
# 查询四川省边界 (OSM relation ID)
# 先通过 Nominatim 获取 relation ID
curl "https://nominatim.openstreetmap.org/search?q=Sichuan&format=json&polygon_geojson=1"
```

### Overpass QL 查询

```
// 查询四川省边界 (relation id: 913069)
[out:json];
relation(913069);
out geom;
```

### 在线工具

- **Overpass Turbo**: https://overpass-turbo.eu/ — 可视化查询工具
- **OSM Boundaries**: https://osm-boundaries.com/ — 方便下载边界数据
- **Nominatim**: https://nominatim.openstreetmap.org/ — 地名搜索

## 3. GitHub GeoJSON 仓库

### xyanmi/MapData
https://github.com/xyanmi/MapData

包含中国省级和城市级行政边界 GeoJSON 数据。

```bash
# 省级（已本地保存）
https://raw.githubusercontent.com/xyanmi/MapData/main/provinces.cn.geojson

# 全国
https://raw.githubusercontent.com/xyanmi/MapData/main/countries.geojson
```

### zhChuXiao/ChinaGeoJson
https://github.com/zhChuXiao/ChinaGeoJson

包含省/市/区县三级数据，来自 DataV.GeoAtlas。

### Natural Earth Data
https://www.naturalearthdata.com/

全球尺度的自然和行政边界数据。

## 4. 其他数据源

| 数据源 | URL | 说明 |
|--------|-----|------|
| SimpleMaps | https://simplemaps.com/gis/country/cn | 免费中国 GIS 数据 |
| ChinaBoundary | https://chinaboundary.com/ | 标准中国边界数据 |
| OSM-Boundaries | https://osm-boundaries.com/ | 全球边界数据 |
