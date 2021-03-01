import os
import sys
import asyncio
import argparse
import checkout
from decouple import config as env_config
from datetime import datetime

class BotCluster():
    def __init__(self, args):
        self.store_list = [i for i in args if args[i] and i in ["walmart", "bestbuy", "newegg", "bandh"]]
        self.args = args
        for store in self.store_list:
            self.args[store] = False
        self.max_prices = {}
        self.wallet = 1000
    
    async def producer(self):
        walmart = self.args.copy()
        bandh = self.args.copy()
        walmart['walmart'] = True
        completed1 = asyncio.create_task(checkout.main(walmart))
        bandh['bandh'] = True
        completed2 = asyncio.create_task(checkout.main(bandh))
        await completed2
        await completed1
        return

    async def consumer(self):

        return  
    
    async def run(self):
        producer = await self.producer()
        # consumer = self.consumer()
        # await asyncio.gather(producer, consumer)

async def main(args):
    try:
        cluster = BotCluster(args)
        await cluster.run()
    except Exception as e:
        print(e)

if __name__== "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test_mode", help="use this flag to turn on test_mode. Defaults to False unless specified", action="store_true")
    parser.add_argument("--headless", help="use this flag to turn on headless mode. Defaults to False unlesss used", action="store_true")
    parser.add_argument("--walmart", help="use this flag to turn on walmart bot. Defaults to False unlesss used", action="store_true")
    parser.add_argument("--bestbuy", help="use this flag to turn on bestbuy bot. Defaults to False unlesss used", action="store_true")
    parser.add_argument("--newegg", help="use this flag to turn on newegg bot. Defaults to False unlesss used", action="store_true")
    parser.add_argument("--bandh", help="use this flag to turn on bandh bot. Defaults to False unlesss used", action="store_true")
    parser.add_argument("--max_price", help="set max price willing to pay", default=env_config('MAX_PRICE'))
    parser.add_argument("--product", help="type in what product you're looking for", default="ps5 disk")
    parser.add_argument("--all_products", help="use this flag to turn on searching for all products you have listed in the config for the stores you are searching", action="store_true")
    args = vars(parser.parse_args())
    asyncio.run(main(args))