import requests
import argparse
import json
from utils import logger
from Bot import StockBot
import os

def main():
    logging = logger.create_logger()
    with open('./configs/walmart_config.json') as file:
        config = json.load(file)
    products = config['products']
    bot = StockBot(username=os.getenv("USERNAME", default=""), password=os.getenv("PASSWORD", default=""), 
                    website_dict=config['website'], product_dict=products[0], 
                    logger=logging, cvv_code=os.getenv("CVV", default=""), test_mode=True)
    bot.run()


if __name__== "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test_mode", help="use this flag to turn on test_mode. Defaults to False unless specified", action="store_true")
    main()