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
            print(output.strip())
    rc = process.poll()
    return 

async def main(args):
    test_mode = ""
    if args['test_mode']:
        test_mode = "--test_mode"
    product= f"--product='{args['product']}'"
    newegg = subprocess.Popen(["python", "checkout.py", test_mode, "--newegg",  product], shell=False, stdout=subprocess.PIPE)
    bestbuy = subprocess.Popen(["python", "checkout.py", test_mode, "--bestbuy",  product], shell=False, stdout=subprocess.PIPE)
    walmart = subprocess.Popen(["python", "checkout.py", test_mode, "--walmart",  product], shell=False, stdout=subprocess.PIPE)
    bandh = subprocess.Popen(["python", "checkout.py", test_mode, "--bandh",  product], shell=False, stdout=subprocess.PIPE)
    
    newegg_coro = show_output(newegg)
    bestbuy_coro = show_output(bestbuy)
    walmart_coro = show_output(walmart)
    # bandh_coro = show_output(bandh)

    await asyncio.gather(newegg_coro, bestbuy_coro, walmart_coro)

if __name__== "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test_mode", help="use this flag to turn on test_mode. Defaults to False unless specified", action="store_true")
    parser.add_argument("--product", help="type in what product you're looking for", default="ps5 disk")
    args = vars(parser.parse_args())
    asyncio.run(main(args))