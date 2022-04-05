from asyncio import run, sleep

from cache import  CacheController
from bus_controller import BusSenderController

from service import generate_datas, init_datas


async def main():
    # launch main logic
    async with BusSenderController() as bus:
        async with CacheController() as cache:
            init_data = await init_datas(cache)
            if init_data:
                await bus.publish(init_data, queue="data_gen")
            while True:
                await sleep(1)
                async for pkg in generate_datas(cache):
                    await bus.publish(pkg, queue="data_gen")


if __name__ == "__main__":
    run(main())
