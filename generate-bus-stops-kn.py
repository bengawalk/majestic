import csv
import asyncio
import aiohttp
import sys

INPUT_CSV = 'input/bus-stops.csv'
OUTPUT_CSV = 'input/bus-stops-kn.csv'
API_URL = 'https://api.varnamproject.com/tl/kn/{stop}'
CONCURRENCY = 4
TIMEOUT = 30  # seconds
RETRIES = 3

async def fetch_kn(session, stop, sem, retries=RETRIES):
    url = API_URL.format(stop=stop.lower())
    for attempt in range(retries):
        async with sem:
            try:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=TIMEOUT)) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        # Use the first result if available
                        result = data.get('result')
                        if isinstance(result, list) and result:
                            return stop, result[0]
                        elif isinstance(result, str):
                            return stop, result
                        else:
                            return stop, stop
                    else:
                        await asyncio.sleep(1)
            except Exception as e:
                if attempt < retries - 1:
                    await asyncio.sleep(2 ** attempt)  # Exponential backoff
                else:
                    return stop, stop
    return stop, stop

def shakedown_bus_stops_kn():
    input_path = OUTPUT_CSV
    output_path = OUTPUT_CSV
    best = {}
    with open(input_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            stop = row['stop_name'].strip()
            stop_kn = row['stop_name_kn'].strip()
            if stop and stop_kn:
                # Keep the row with the longest stop_kn for each stop
                if stop not in best or len(stop_kn) > len(best[stop]):
                    best[stop] = stop_kn
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['stop_name', 'stop_name_kn'])
        for stop in sorted(best):
            writer.writerow([stop, best[stop]])
    print(f"Wrote {len(best)} unique stops (by stop_name, longest stop_name_kn) to {output_path}")

async def main():
    # Read all unique stops
    stops = set()
    with open(INPUT_CSV, encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            for stop in row[1:]:
                stop = stop.strip()
                if stop:
                    stops.add(stop)
    stops = sorted(stops)

    sem = asyncio.Semaphore(CONCURRENCY)
    results = []
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_kn(session, stop, sem) for stop in stops]
        for fut in asyncio.as_completed(tasks):
            result = await fut
            results.append(result)

    # Write to output CSV
    with open(OUTPUT_CSV, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['stop_name', 'stop_name_kn'])
        for stop, stop_kn in sorted(results):
            writer.writerow([stop, stop_kn])
    print(f"Wrote {len(results)} stops to {OUTPUT_CSV}")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'shakedown':
        shakedown_bus_stops_kn()
    else:
        asyncio.run(main()) 