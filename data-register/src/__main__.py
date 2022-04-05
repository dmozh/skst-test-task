from asyncio import run

from database import controller
from service import PricesService
from logger import log
from publisher import PublisherController
from bus_controller import BusReceiverController


async def main():
    # launch main logic
    # future = create_task(publishing())
    # await future
    async with PublisherController('channel_all_tickers') as publisher:
        service = PricesService(publisher)
        async with BusReceiverController() as receiver:
            await receiver.consume('data_gen', [service.write_to_store, service.publish_data])

if __name__ == "__main__":
    run(main())
    log.info("END")
