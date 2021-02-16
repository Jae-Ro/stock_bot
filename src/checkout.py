import requests
import argparse
import json
from utils import logger
from Bot import StockBot
import os
from decouple import config as env_config

def main(args):
    logging = logger.create_logger()
    with open('./configs/walmart_config.json') as file:
        config = json.load(file)
    products = config['products']
    bot = StockBot(username=env_config("WALMART_USERNAME"), password=env_config("WALMART_PASSWORD"), 
                    website_dict=config['website'], product_dict=products[0], 
                    logger=logging, cvv_code=env_config("CVV"), max_price=env_config("MAX_PRICE"), 
                    headless=args['headless'], test_mode=args['test_mode'])
    bot.run()


if __name__== "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test_mode", help="use this flag to turn on test_mode. Defaults to False unless specified", action="store_true")
    parser.add_argument("--headless", help="use this flag to turn on headless mode. Defaults to False unlesss used", action="store_true")
    args = vars(parser.parse_args())
    main(args)