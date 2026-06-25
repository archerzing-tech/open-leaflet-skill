#!/usr/bin/env python3
"""Download f4map building tiles and convert to lat/lng GeoJSON."""
import json, math, os, sys, urllib.request

def parse_way(way_str):
    def parse_ring(r):
        s = r.strip()
        while s.startswith('('): s = s[1:]
        while s.endswith(')'): s = s[:-1]
        if not s: return None
        pts = s.split(',')
        out = []
        ax = ay = 0
        for i, p in enumerate(pts):
            c = p.strip().split()
            if len(c) < 2: return None
            try:
                x, y = int(c[0]), int(c[1])
            except:
                return None
            if i == 0:
                ax, ay = x, y
            else:
                ax += x; ay += y
            out.append([ax, ay])
        return out
    if way_str[0] == 'N': return None
    body = way_str[2:-1]
    rings = []
    if way_str[0] == 'P':
        r = parse_ring(body)
        if r: rings.append(r)
    elif way_str[0] == 'M':
        i = 0
        while i < len(body):
            if body[i] == '(':
                d = 1; j = i + 1
                while j < len(body) and d > 0:
                    if body[j] == '(': d += 1
                    if body[j] == ')': d -= 1
                    j += 1
                r = parse_ring(body[i+1:j-1])
                if r: rings.append(r)
                i = j
            else:
                i += 1
    return rings

def tile_to_latlng(tx, ty, z, cx, cy):
    ts = 65536
    wx = tx + cx / ts
    wy = ty + cy / ts
    n = 2 ** z
    lon = wx / n * 360 - 180
    lat = math.degrees(math.atan(math.sinh(math.pi - wy / n * 2 * math.pi)))
    return lat, lon

def get_tile_bounds(bounds, z):
    n = 2 ** z
    sw_lat, sw_lng = bounds[0]
    ne_lat, ne_lng = bounds[1]
    min_tx = int((sw_lng + 180) / 360 * n)
    max_tx = int(math.ceil((ne_lng + 180) / 360 * n))
    min_ty = int((1 - math.log(math.tan(math.radians(ne_lat)) + 1 / math.cos(math.radians(ne_lat))) / math.pi) / 2 * n)
    max_ty = int(math.ceil((1 - math.log(math.tan(math.radians(sw_lat)) + 1 / math.cos(math.radians(sw_lat))) / math.pi) / 2 * n))
    tiles = []
    for tx in range(min_tx, max_tx + 1):
        for ty in range(min_ty, max_ty + 1):
            tiles.append((tx, ty))
    return tiles

def download_tile(tx, ty, z):
    import subprocess, tempfile
    url = f'https://buildings.f4map.com/buildings/{z}/{tx}/{ty}.json?query=%7B%22maxage%22%3A43200%2C%22straightSkeleton%22%3A1%7D'
    try:
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False, mode='w') as f:
            tmp = f.name
        subprocess.run(['curl', '-s', '--max-time', '10', url, '-o', tmp],
                       capture_output=True, timeout=15)
        with open(tmp) as f:
            data = json.load(f)
        os.unlink(tmp)
        return data
    except Exception as e:
        print(f'  Failed tile {tx}/{ty}: {e}')
        try: os.unlink(tmp)
        except: pass
        return []

def tile_to_geojson(tx, ty, z, buildings):
    features = []
    for b in buildings:
        if not b.get('way'): continue
        rings = parse_way(b['way'])
        if not rings: continue
        levels = b.get('building:levels', 0)
        if isinstance(levels, str) and ';' in levels: levels = levels.split(';')[0]
        h = b.get('height') or (int(levels or 0) * 3.8) or 5
        name = b.get('name') or b.get('name:en') or ''
        for ring in rings:
            if not ring or len(ring) < 3: continue
            coords = [[tile_to_latlng(tx, ty, z, p[0], p[1]) for p in ring]]
            coords[0] = [[lng, lat] for lat, lng in coords[0]]
            coords[0].append(coords[0][0])
            features.append({'type': 'Feature',
                'properties': {'height': h, 'name': name},
                'geometry': {'type': 'Polygon', 'coordinates': coords}})
    return features

def main():
    cities = {
        'shanghai': {'center': [31.241, 121.500], 'bounds': [[31.22, 121.47], [31.27, 121.53]]},
        'hongkong': {'center': [22.319, 114.169], 'bounds': [[22.29, 114.14], [22.35, 114.20]]},
        'shenzhen': {'center': [22.543, 114.058], 'bounds': [[22.52, 114.03], [22.57, 114.09]]},
    }

    base_dir = os.path.join(os.path.dirname(__file__), '..', 'assets', 'data')
    os.makedirs(base_dir, exist_ok=True)

    for city_name, cfg in cities.items():
        z = 16
        tiles = get_tile_bounds(cfg['bounds'], z)
        print(f'\n{city_name}: {len(tiles)} tiles at z{z}')
        all_features = []
        for tx, ty in tiles:
            print(f'  downloading {tx}/{ty}...')
            data = download_tile(tx, ty, z)
            features = tile_to_geojson(tx, ty, z, data)
            all_features.extend(features)
            print(f'    -> {len(features)} buildings')

        geojson = {'type': 'FeatureCollection', 'features': all_features}
        out_path = os.path.join(base_dir, f'{city_name}-buildings.json')
        with open(out_path, 'w') as f:
            json.dump(geojson, f)
        print(f'  saved {len(all_features)} buildings to {out_path}')

if __name__ == '__main__':
    main()
