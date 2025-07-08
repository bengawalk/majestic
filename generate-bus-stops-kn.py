import csv
import asyncio
import aiohttp

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
    asyncio.run(main()) 