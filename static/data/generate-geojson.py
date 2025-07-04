import csv
import json
from collections import defaultdict

# File paths
platform_index_path = 'static/data/platform-index.csv'
bus_routes_path = 'static/data/bus-routes.csv'
platforms_geojson_path = 'static/data/platforms-majestic.geojson'
output_geojson_path = 'static/data/platforms-routes-majestic.geojson'

# Read platform index
platform_index = defaultdict(list)
with open(platform_index_path, encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        platform_number = row['Platform Number'].strip()
        platform_index[platform_number].append(row)

# Read bus routes
routes_by_number = defaultdict(list)
with open(bus_routes_path, encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        platform = row[0].strip()
        route_numbers = row[1].split(',') if row[1] else []
        major_stops = [stop.strip() for stop in row[2:] if stop and stop.strip()]
        for route_number in route_numbers:
            route_number = route_number.strip()
            if route_number:
                routes_by_number[(platform, route_number)].append(major_stops)

# Read platform geometries and build a lookup
with open(platforms_geojson_path, encoding='utf-8') as f:
    platforms_geojson = json.load(f)
platform_geom_lookup = {}
platform_color_lookup = {}
for plat in platforms_geojson['features']:
    plat_num = str(plat['properties'].get('Platform', '')).strip()
    platform_geom_lookup[plat_num] = plat['geometry']
    platform_color_lookup[plat_num] = plat['properties'].get('Color', '#FFFFFF')

features = []
for plat_num, plat_rows in platform_index.items():
    plat_num = plat_num.upper()
    geometry = platform_geom_lookup.get(plat_num)
    color = platform_color_lookup.get(plat_num, '#FFFFFF')
    routes = []
    for plat_row in plat_rows:
        bus_numbers = plat_row['Bus Number'].split(',') if plat_row['Bus Number'] else []
        for bus_number in bus_numbers:
            bus_number = bus_number.strip()
            if not bus_number:
                continue
            # Find major stops for this platform and route
            major_stops = []
            key = (plat_num, bus_number)
            if key in routes_by_number:
                major_stops = routes_by_number[key][0]  # Take the first match
            else:
                # fallback: try to find by route only (any platform)
                for (plat_k, route_k), stops_list in routes_by_number.items():
                    if route_k == bus_number:
                        major_stops = stops_list[0]
                        break
            route_obj = {
                'Route': bus_number,
                'Destination': plat_row['Destination'],
                'Via': plat_row['Via'],
                'Area': plat_row['Area'],
                'PlatformNumber': plat_row['Platform Number'],
                'KannadaDestination': plat_row['Destination - Kannada'],
                'KannadaArea': plat_row['Area - Kannada'],
                'KannadaVia': plat_row['Via - Kannada'],
                'Stops': major_stops
            }
            routes.append(route_obj)
    if geometry is None:
        # Print error for each route if platform not found
        for route in routes:
            print(f"ERROR: Platform geometry not found for Platform {plat_num}, Route {route['Route']}")
        continue
    if routes:
        feature = {
            'type': 'Feature',
            'geometry': geometry,
            'properties': {
                'Platform': plat_num,
                'Color': color,
                'Routes': routes
            }
        }
        features.append(feature)
    else:
        print("PF no routes", plat_num, color, routes)

geojson = {
    'type': 'FeatureCollection',
    'features': features
}

with open(output_geojson_path, 'w', encoding='utf-8') as f:
    json.dump(geojson, f, ensure_ascii=False, indent=2)

print(f"Wrote {len(features)} platform features to {output_geojson_path}")
