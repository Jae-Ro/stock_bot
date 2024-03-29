import requests
import argparse
import json
from utils import logger
from Bot import StockBot
import os
from decouple import config as env_config
from datetime import datetime
import asyncio

def start_run(config, config_path, product_index, args):
    products = config['products']
    now = datetime.now()
    dt_string = now.strftime("%m%d%Y-%H_%M_%S")
    site_name = config_path.split("/")[-1].split("_config.json")[0]
    logging_name = f"{products[product_index]['name']} - {site_name.upper()}"
    logging = logger.create_logger(dt_string, logging_name, site_name)
    bot = StockBot(site=site_name, username=env_config(f"{site_name.upper()}_USERNAME"), password=env_config(f"{site_name.upper()}_PASSWORD"), 
                    website_dict=config['website'], product_dict=products[product_index], 
                    logger=logging, cvv_code=env_config("CVV"), dt_str=dt_string, max_price=args['max_price'], 
                    headless=args['headless'], test_mode=args['test_mode'])
    ret = bot.run()
    return ret

def search_product_list(product_list, search_string):
    # print(str(search_string))
    search_terms = search_string.lower().split(" ")
    # print("original search terms: ", search_terms)
    max_match = []
    max_index = 0
    for i, p in enumerate(product_list):
        keywords = set(p['keywords'])
        matches = [s for s in search_terms if s.strip() in keywords]
        if len(matches) > len(max_match):
            max_match = matches
            max_index = i
    # print("Final Match: ", max_match)
    return max_index

async def main(args):
    try:
        finish = False
        if not args['all_products']:
            if args['bestbuy']:
                config_file_path = "./configs/bestbuy_config.json"
            elif args['walmart']:
                config_file_path="./configs/walmart_config.json"
            elif args['bandh']:
                config_file_path="./configs/bandh_config.json"
            elif args['newegg']:
                config_file_path="./configs/newegg_config.json"
            else:
                print("No website was selected. Terminating Program.")
                return
            with open(config_file_path) as file:
                config = json.load(file)
            product_index = search_product_list(config['products'], args['product'])
            finish = start_run(config, config_file_path, product_index, args)        
        else:
            pass
    
    except Exception as e:
        print(e)

    return finish

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