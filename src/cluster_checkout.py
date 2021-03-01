import os
import subprocess
import sys
# import shlex
import asyncio
import argparse

async def show_output(process):
    while True:
        output = process.stdout.readline()
        if process.poll() is not None: # returns None if the process is still running.
            break
        if output:
            out = output.strip()
            print(out)
    rc = process.poll()
    return 

async def main(args):
    product= f"--product={args['product']}"
    try:
        if args['test_mode'] and not args['headless']:
            newegg = subprocess.Popen(["python", "checkout.py", "--test_mode", "--newegg",  product], shell=False, stdout=subprocess.PIPE)
            bestbuy = subprocess.Popen(["python", "checkout.py", "--test_mode", "--bestbuy",  product], shell=False, stdout=subprocess.PIPE)
            walmart = subprocess.Popen(["python", "checkout.py", "--test_mode", "--walmart",  product], shell=False, stdout=subprocess.PIPE)
            bandh = subprocess.Popen(["python", "checkout.py", "--test_mode", "--bandh",  product], shell=False, stdout=subprocess.PIPE)
        
        elif args['headless'] and not args['test_mode']:
            newegg = subprocess.Popen(["python", "checkout.py", "--newegg",  product, "--headless"], shell=False, stdout=subprocess.PIPE)
            bestbuy = subprocess.Popen(["python", "checkout.py", "--bestbuy",  product, "--headless"], shell=False, stdout=subprocess.PIPE)
            walmart = subprocess.Popen(["python", "checkout.py", "--walmart",  product, "--headless"], shell=False, stdout=subprocess.PIPE)
            bandh = subprocess.Popen(["python", "checkout.py", "--bandh",  product, "--headless"], shell=False, stdout=subprocess.PIPE)
        
        elif not args['test_mode'] and not args['headless']:
            newegg = subprocess.Popen(["python", "checkout.py", "--newegg",  product], shell=False, stdout=subprocess.PIPE)
            # bestbuy = subprocess.Popen(["python", "checkout.py", "--bestbuy",  product], shell=False, stdout=subprocess.PIPE)
            # walmart = subprocess.Popen(["python", "checkout.py", "--walmart",  product], shell=False, stdout=subprocess.PIPE)
            bandh = subprocess.Popen(["python", "checkout.py", "--bandh",  product], shell=False, stdout=subprocess.PIPE)
        
        elif args['test_mode'] and args['headless']:
            newegg = subprocess.Popen(["python", "checkout.py", "--test_mode", "--newegg",  product, "--headless"], shell=False, stdout=subprocess.PIPE)
            bestbuy = subprocess.Popen(["python", "checkout.py", "--test_mode", "--bestbuy",  product, "--headless"], shell=False, stdout=subprocess.PIPE)
            walmart = subprocess.Popen(["python", "checkout.py", "--test_mode", "--walmart",  product, "--headless"], shell=False, stdout=subprocess.PIPE)
            bandh = subprocess.Popen(["python", "checkout.py", "--test_mode", "--bandh",  product, "--headless"], shell=False, stdout=subprocess.PIPE)
        
        newegg_coro = show_output(newegg)
        # bestbuy_coro = show_output(bestbuy)
        # walmart_coro = show_output(walmart)
        bandh_coro = show_output(bandh)

        await asyncio.gather(newegg_coro, bandh_coro)
    except:
        pass

if __name__== "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test_mode", help="use this flag to turn on test_mode. Defaults to False unless specified", action="store_true")
    parser.add_argument("--headless", help="use this flag to turn on headless mode. Defaults to False unless specified", action="store_true")
    parser.add_argument("--product", help="type in what product you're looking for", default="ps5 disk")
    args = vars(parser.parse_args())
    asyncio.run(main(args))