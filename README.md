# A Stock Checking & Checkout Bot for GPU and PS5
Author: Jae Ro
#### Supports the Following Stores
- Bestbuy
- Walmart
- Newegg
- BandH

#### Before Running
1. You will need to add a ```.env``` file to the root directory of the project
   -  inside the .env file you will need the following variables filled out
      -  WALMART_USERNAME= 
      -  WALMART_PASSWORD=
      -  BESTBUY_USERNAME=
      -  BESTBUY_PASSWORD=
      -  NEWEGG_USERNAME=
      -  NEWEGG_PASSWORD=
      -  BANDH_USERNAME=
      -  BANDH_PASSWORD=
      -  CVV=
      -  MAX_PRICE=
2. Login to the account for the store you're trying to run this on and make sure..
    - You have your credit card information saved as well as billing and shipping address (if the site has an option for you to choose between in-store pickup or shipping, pick shipping)
    - You clear your cart (this bot will add things to your cart, but does not yet have the feature to clear it)
3. Look through the config file for the store you're trying to buy your product from and make sure that the product you're looking for has an entry (if not, you will need to add one).
##### Example Product Entry
```
{
    "name": "Apple Airpods",
    "description": "Apple AirPods (2nd Generation) MV7N2AM/A with Charging Case - Stereo - Wireless - Bluetooth - Earbud - Binaural - In-ear",
    "product_url": "https://www.newegg.com/apple-airpods-gloss-white/p/2MA-00JB-00031?Description=airpods&cm_re=airpods-_-2MA-00JB-00031-_-Product",
    "keywords": [
        "apple",
        "airpods",
        "air",
        "pods"
    ]
}

```
4. Make sure you add the ```--test_mode``` flag to the run argument if you're not trying to actually buy the product
5. Make sure to download and install the geckodriver (webdriver for Firefox). If you're on mac and have homebrew installed you can run ```brew install geckodriver```
6. Install the following python packages (note: this project uses python 3.7.6)
   - selenium
   - requests
   - python-decouple
   - asyncio
   - locale

#### Basic Run Command:
- note: make sure to look at table of command line arguments before running
- note: make sure when you run it for the first time to not run it in headless mode. The first run is to log you in to the selected store and then save your credentials as cookies (for newegg you will need to check your email and enter the security code for 2fa)
```
$ python checkout.py --{argument1} --{argument2} --{etc}
```

| Command Line Argument | Description                                                      | Default    |
| --------------------- | :--------------------------------------------------------------- | ---------- |
| --test_mode           | Turn on test_mode. Goes all the way up to final purchase button  | False      |
| --headless            | Turn on headless mode. No visual browser, but runs in background | False      |
| --walmart             | Set store to walmart                                             | False      |
| --bestbuy             | Set store to bestbuy                                             | False      |
| --newegg              | Set store to newegg                                              | False      |
| --bandh               | Set store to bandh                                               | False      |
| --max_price           | Set max price you're willing to pay for item                     | .env       |
| --product             | Search string for what you're looking for (ex. "ps5")            | "ps5 disk" |

#### Advanced Run Command (still in beta):
- note: this currently is set to work with walmart and bestbuy to run both in parallel at the same time so don't set the store argument
```
$ python cluster_checkout.py --{argument1} --{argument2} --{etc}
```


