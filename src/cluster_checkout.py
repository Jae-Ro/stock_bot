import os
import subprocess
import sys
# import shlex
import asyncio

async def show_output(process):
    while True:
        output = process.stdout.readline()
        if process.poll() is not None: # returns None if the process is still running.
            break
        if output:
            print(output.strip())
    rc = process.poll()
    return 

async def main():
    process1 = subprocess.Popen(["python", "checkout.py", "--test_mode", "--newegg",  "--product='airpods'"],  stdout=subprocess.PIPE)
    process2 = subprocess.Popen(["python", "checkout.py", "--test_mode", "--bestbuy",  "--product='airpods'"],  stdout=subprocess.PIPE)
    
    coroutine_1 = show_output(process1)
    coroutine_2 = show_output(process2)
    await asyncio.gather(coroutine_1, coroutine_2)

if __name__== "__main__":
    asyncio.run(main())