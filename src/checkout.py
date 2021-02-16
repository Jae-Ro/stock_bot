import requests
import argparse
import json
from utils import logger
from Bot import StockBot
import os
from decouple import config as env_config

def main(args):
    logging = logger.create_logger()
    if args['bestbuy']:
        config_file_path = "./configs/bestbuy_config.json"
    elif args['walmart']:
        config_file_path="./configs/walmart_config.json"
    else:
        logging.info("No website was selected. Terminating Program.")
        return
    with open(config_file_path) as file:
        config = json.load(file)
    products = config['products']
    site_name = config_file_path.split("/")[-1].split("_config.json")[0]
    bot = StockBot(site=site_name, username=env_config(f"{site_name.upper()}_USERNAME"), password=env_config(f"{site_name.upper()}_PASSWORD"), 
                    website_dict=config['website'], product_dict=products[0], 
                    logger=logging, cvv_code=env_config("CVV"), max_price=env_config("MAX_PRICE"), 
                    headless=args['headless'], test_mode=args['test_mode'])
    bot.run()

if __name__== "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test_mode", help="use this flag to turn on test_mode. Defaults to False unless specified", action="store_true")
    parser.add_argument("--headless", help="use this flag to turn on headless mode. Defaults to False unlesss used", action="store_true")
    parser.add_argument("--walmart", help="use this flag to turn on walmart bot. Defaults to False unlesss used", action="store_true")
    parser.add_argument("--bestbuy", help="use this flag to turn on bestbuy bot. Defaults to False unlesss used", action="store_true")

    args = vars(parser.parse_args())
    main(args)