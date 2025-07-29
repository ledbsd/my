import asyncio


async def fetch_data():
    print('Fetching data...')
    await asyncio.sleep(2)


loop = asyncio.new_event_loop()

tasks = [
    loop.create_task(fetch_data()),
    loop.create_task(fetch_data()),
    loop.create_task(fetch_data()),
    loop.create_task(fetch_data()),
    loop.create_task(fetch_data()),
]

loop.run_until_complete(asyncio.wait(tasks))
loop.close()

