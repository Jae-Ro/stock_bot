import requests
import asyncio
import argparse
from utils import logger
from Walmart import WalmartBot
from BestBuy import BestBuyBot

async def main():
    logging = logger.create_logger()
    logging.info('Hello ...')
    await asyncio.sleep(1)
    logging.info('... World!')

    # bb = BestBuyBot('username', 'password', {})
    wb = WalmartBot('username', 'password', {})
    wb.navigate("https://www.walmart.com/")


if __name__== "__main__":
    asyncio.run(main())