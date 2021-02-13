import requests
import asyncio
import argparse
from utils import logger

async def main():
    logging = logger.create_logger()
    logging.info('Hello ...')
    await asyncio.sleep(1)
    logging.info('... World!')

if __name__== "__main__":
    asyncio.run(main())