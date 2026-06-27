# 地理数据源参考

> 针对中国网络环境优化，提供多个数据获取渠道及优先级建议。

---

## 渠道总览

| 渠道 | 国内访问 | 坐标系 | 覆盖范围 | 推荐场景 |
|------|---------|--------|---------|---------|
| ① DataV.GeoAtlas（阿里云） | ✅ 极快 | GCJ-02 | 省/市/区县 | 首选实时数据 |
| ② GeoJSON.cn | ✅ 极快 | GCJ-02 | 省/市/区县 | 离线/缓存首选 |
| ③ 天地图 API | ✅ 极快 | CGCS2000 | 省/市/区县 | 官方数据需求 |
| ④ 高德地图 API | ✅ 极快 | GCJ-02 | 省/市/区县 | 动态边界查询 |
| ⑤ GitHub 仓库（国内镜像） | ⚠️ 可能慢 | WGS-84 | 省/市/区县 | 离线数据 |
| ⑥ Overpass API | ⚠️ 受限 | WGS-84 | 全球 | 国外数据 |
| ⑦ geoBoundaries | ⚠️ 受限 | WGS-84 | 全球 ADM0-2 | 学术/标准数据 |
| ⑧ 本地 GeoJSON 文件 | ✅ 无网络 | 取决于来源 | 预先准备 | 离线/稳定需求 |

---

## 渠道详解

### ① 阿里云 DataV.GeoAtlas（推荐 · 国内首选）

**URL**: https://datav.aliyun.com/tools/atlas/

DataV.GeoAtlas 提供中国各级行政区划边界数据，支持国/省/市/区县四级，数据来源于高德地图。国内访问速度快，适合实时加载。

#### 数据 API

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

#### 行政区划代码（adcode）

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

完整 CSV: https://docs-aliyun.cn-hangzhou.oss.aliyun-inc.com/assets/attach/84544/cn_zh/1530167929977/%E7%9C%81%E5%B8%82%E5%8C%BAadcode%E3%80%81%E7%BB%8F%E7%BA%AC%E5%BA%A6%E6%98%A0%E5%B0%84%E8%A1%A8gbk.csv

#### 使用示例（Leaflet）

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

---

### ② GeoJSON.cn（推荐 · 离线/批量获取）

**URL**: https://geojson.cn/data/atlas/china

国内维护的中国行政区域数据源，提供标准 GeoJSON 和 TopoJSON 格式，覆盖省/市/区县三级。更新及时，国内访问快。

#### API 接口

```bash
# 全国数据
https://geojson.cn/api/china/100000.json

# 省级数据（如四川省 510000）
https://geojson.cn/api/china/510000.json

# 市级数据（如成都市 510100）
https://geojson.cn/api/china/510000/510100.json

# 获取元数据（所有可用文件列表）
https://geojson.cn/api/china/_meta.json

# TopoJSON 格式（文件体积更小）
https://geojson.cn/api/china/510000.topo.json
```

#### 数据属性

| 属性 | 含义 | 示例 |
|------|------|------|
| `name` | 行政区名称 | "北京市" |
| `code` | 六位行政编码 | "110100" |
| `level` | 行政级别 | 0:国, 1:省, 2:市, 3:县 |
| `center` | 行政中心经纬度 | [116.4, 39.9] |
| `pinyin` | 拼音缩写 | "bj" |

> **坐标系**：v1.6.0+ 基于 GCJ-02（火星坐标）系。如果在 Leaflet/OSM 等 WGS-84 地图上叠加，需进行坐标转换。

---

### ③ 天地图 API（官方数据）

**URL**: http://lbs.tianditu.gov.cn/server/administrative2.html

国家官方地理信息服务平台，数据权威合规。适合对数据合规性有要求的项目。

#### 获取方式

1. 在天地图开发者官网申请 Key
2. 调用行政区划服务接口：

```bash
# 查询四川省边界
https://api.tianditu.gov.cn/v2/administrative?keyword=510000&extensions=true&tk=YOUR_KEY
```

> **坐标系**：CGCS2000（国家大地坐标系），与 WGS-84 差异极小，一般可直接使用。
> **注意**：返回的 `boundary` 是压缩编码格式，需解析为 GeoJSON。

---

### ④ 高德地图 API（动态边界）

**URL**: https://lbs.amap.com/api/javascript-api/example/district-search/draw-district-boundaries

适合需要动态获取行政区边界的场景（如下钻查询）。

#### 使用方式

```javascript
// 高德 JS API 的 DistrictSearch
var district = new AMap.DistrictSearch({ extensions: 'all' });
district.search('四川省', function(status, result) {
  var boundaries = result.districtList[0].boundaries; // 坐标数组
  // 需转为 GeoJSON 格式
});
```

> **坐标系**：GCJ-02
> **注意**：返回的是坐标数组，需自行封装为 GeoJSON Feature 对象。GitHub 上有 `amap-to-geojson` 工具库可用。

---

### ⑤ GitHub 仓库（离线数据）

从 GitHub 克隆到本地，避免在线 API 依赖。适合生产环境使用。

> ⚠️ **国内网络提示**：`raw.githubusercontent.com` 在国内可能访问慢或不稳定。推荐：
> - 克隆后作为本地静态文件使用（本项目已预置在 `assets/data/`）
> - 使用 jsDelivr CDN 镜像：`https://cdn.jsdelivr.net/gh/user/repo@branch/path`

#### 推荐仓库

| 仓库 | 说明 | 国内镜像 |
|------|------|---------|
| [xyanmi/MapData](https://github.com/xyanmi/MapData) | 省级及全国边界 | `https://cdn.jsdelivr.net/gh/xyanmi/MapData/main/provinces.cn.geojson` |
| [longwosion/geojson-map-china](https://github.com/longwosion/geojson-map-china) | 省市区县 GeoJSON | jsDelivr 可用 |
| [BarbarossaWang/cn-atlas](https://github.com/BarbarossaWang/cn-atlas) | 更新较频繁的边界数据 | jsDelivr 可用 |
| [echarts-maps](https://github.com/echarts-maps) | ECharts 兼容 GeoJSON | jsDelivr 可用 |

```javascript
// 通过 jsDelivr 镜像加速
fetch('https://cdn.jsdelivr.net/gh/xyanmi/MapData@main/provinces.cn.geojson')
  .then(r => r.json())
  .then(data => { /* ... */ });
```

---

### ⑥ OpenStreetMap Overpass API（全球数据）

**URL**: https://overpass-api.de/api/interpreter

用于从 OpenStreetMap 获取全球行政边界。**国内访问速度较慢**，建议作为备选。

#### 查询示例

```bash
# 查询四川省边界 (relation id: 913069)
curl "https://overpass-api.de/api/interpreter?data=[out:json];relation(913069);out geom;"
```

#### 获取 OSM Relation ID

```bash
# 通过 Nominatim 查询
curl "https://nominatim.openstreetmap.org/search?q=Sichuan&format=json&polygon_geojson=1"
```

> 在线工具：https://overpass-turbo.eu/（国内可能受限）

---

### ⑦ geoBoundaries（国际标准数据）

**URL**: https://www.geoboundaries.org/

开放许可（CC BY 4.0）的全球行政边界数据库，标准化程度高。

| 级别 | 说明 |
|------|------|
| ADM0 | 国家边界 |
| ADM1 | 省级边界（如四川省） |
| ADM2 | 市级边界 |

> 数据可直接下载 GeoJSON，学术和研究场景推荐。

---

## 坐标系转换指南

| 坐标系 | 来源 | 说明 |
|--------|------|------|
| WGS-84 | OSM, GPS, GeoJSON.cn 旧版 | 国际通用，Leaflet 默认 |
| GCJ-02 | 高德、DataV、GeoJSON.cn v1.6+ | 火星坐标系，国内地图常用 |
| BD-09 | 百度地图 | 在 GCJ-02 基础上二次加密 |
| CGCS2000 | 天地图 | 国家大地坐标系，与 WGS-84 差异微小 |

### 坐标系转换工具

```javascript
// gcoord - 轻量级坐标转换库
// https://github.com/hujiulong/gcoord
import gcoord from 'gcoord';

// GCJ-02 → WGS-84 转换
var result = gcoord.transform(
  [116.397, 39.908],  // [经度, 纬度]
  gcoord.GCJ02,       // 当前坐标系
  gcoord.WGS84        // 目标坐标系
);
// result: [116.391, 39.907]
```

> **建议**：直接在 HTML 中通过 CDN 引入 `gcoord`，例如 `<script src="https://cdn.jsdelivr.net/npm/gcoord"></script>`

---

## 多通道 Fallback 策略

建议在生成 HTML 时使用以下 fallback 链，确保在任意网络环境下数据都能加载：

```javascript
function loadGeoJSON(urls, callback) {
  var index = 0;
  function tryNext() {
    if (index >= urls.length) {
      console.error('所有数据源均加载失败');
      return;
    }
    fetch(urls[index])
      .then(r => { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); })
      .then(data => callback(data))
      .catch(function() {
        console.warn('数据源加载失败，尝试下一个: ' + urls[index]);
        index++;
        tryNext();
      });
  }
  tryNext();
}

// 使用：DataV → GeoJSON.cn → 本地文件 → CDN 镜像
loadGeoJSON([
  'https://geo.datav.aliyun.com/areas_v3/bound/510000_full.json',  // DataV
  'https://geojson.cn/api/china/510000.json',                      // GeoJSON.cn
  './data/china_provinces.geojson',                                 // 本地文件
  'https://cdn.jsdelivr.net/gh/xyanmi/MapData@main/provinces.cn.geojson'  // CDN 镜像
], function(data) {
  L.geoJSON(data).addTo(map);
});
```

### 推荐优先级

**中国地图场景**（按推荐顺序）：
1. 本地预置数据 → 最快最稳（本项目 `assets/data/china_provinces.geojson`）
2. DataV.GeoAtlas API → 国内速度快，实时性好
3. GeoJSON.cn API → 国内速度快，支持 TopoJSON
4. jsDelivr CDN 镜像 → GitHub 仓库的加速访问
5. GitHub raw → 备选

**全球地图场景**：
1. Natural Earth Data → 下载后本地加载
2. geoBoundaries → 标准开放数据
3. Overpass API → 实时查询（国内可能慢）
4. Nominatim → 地名解析

---

## 本技能内置数据

| 文件 | 覆盖范围 | 说明 |
|------|---------|------|
| `assets/data/china_provinces.geojson` | 全国 34 个省级行政区 | 含港澳台，WGS-84 |
| `assets/data/taiwan.geojson` | 台湾省 | 独立文件 |
| `assets/data/hongkong.geojson` | 香港 18 区 | 独立文件 |
| `assets/data/macau.geojson` | 澳门 8 堂区 | 独立文件 |
| `assets/data/geo-data.js` | 全国省级 + 香港 + 澳门 | 全局变量 `GEO_DATA`，script 标签引入即可用 |

---

## 网络环境速查表

| 数据源 URL | 国内访问 | 建议用法 |
|-----------|---------|---------|
| `geo.datav.aliyun.com` | ✅ 极快 | 首选实时获取 |
| `geojson.cn` | ✅ 极快 | 离线/批量获取 |
| `api.tianditu.gov.cn` | ✅ 极快 | 官方数据需求 |
| `raw.githubusercontent.com` | ⚠️ 可能慢 | 走 jsDelivr 镜像 |
| `cdn.jsdelivr.net` | ✅ 较快 | GitHub 仓库加速 |
| `overpass-api.de` | ⚠️ 可能慢 | 仅用于全球数据 |
| `nominatim.openstreetmap.org` | ⚠️ 可能慢 | 仅用于地名查询 |
| `picsum.photos` | ⚠️ 可能慢 | 替换为本地图片 |
