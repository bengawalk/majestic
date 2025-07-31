import csv

# Read bus-stops.csv and create a dictionary mapping bus numbers to platform numbers
bus_stops_pf_path = 'input/bus-stops-pf.csv' # When we receive data we get platforms, we remove them for simplicity
platform_index_path = 'input/platform-index.csv'
updated_platform_index_path = 'input/platform-index-updated.csv'

# Create a dictionary to map bus numbers to platform numbers
bus_platform_map = {}
with open(bus_stops_pf_path, mode='r', newline='', encoding='utf-8') as bus_stops_file:
    reader = csv.DictReader(bus_stops_file)
    for row in reader:
        bus_number = row['Route']
        platform_number = row['Platform']
        if bus_number not in bus_platform_map:
            bus_platform_map[bus_number] = platform_number

# Read platform-index.csv and update platform numbers
updated_rows = []
with open(platform_index_path, mode='r', newline='', encoding='utf-8') as platform_index_file:
    reader = csv.DictReader(platform_index_file)
    fieldnames = reader.fieldnames
    for row in reader:
        bus_number = row['Bus Number']
        if bus_number in bus_platform_map:
            row['Platform Number'] = bus_platform_map[bus_number]
        updated_rows.append(row)

# Write the updated rows to platform-index.csv
with open(updated_platform_index_path, mode='w', newline='', encoding='utf-8') as updated_file:
    writer = csv.DictWriter(updated_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(updated_rows)

print(f"Updated platform-index.csv and saved as {updated_platform_index_path}")
