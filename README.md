# zomato_spider
Python scrawler for zomato. This spider can collect restaurant information near **Melbourne**, **Australia** (including restaurant name, thumbnail, rating, info url and geo location). Collecting geo locations are the main purpose of this spider. You can also extract other data since the raw data list will be kept in a single json file. 5 pages of restaurants in carlton will be saved in JSON files, and then the detailed restaurant info will be saved to a single CSV file.

## To start with
1. You should identify `DISTRICT` variable in `config.py`. In this demo example, modify it to be **carlton**.
2. You should identify `COOKIE` variable in `config.py`. Cookie can be found by opening browser and visit zomato website. The expiration time is unknown, but it should be OK.
3. You can leave `ROOT_URL` and `REQUEST_URL` unchanged.
4. By default, spider crawls 5 pages of restaurants. You can modify this variable to collect more. However, `SUBPAGE_REQUEST_DELAY` which defines delay time should be set to avoid being blocked by zomato.
5. After that, run `crawl.py`.

## Requirements
Language: Python \
Version: 3.6+ \
Modules: requests and bs4

## Run the program
If you would like to crawl other district data:
1. create a file, named `DISTRICT_source.json`, where DISTRICT is the constant in `config.py`. This can be done by browsing to any district of zomato. Then, just open F12 to see the initial payload (This require basic skills of package capture). Copy source payload to this json file.
2. Follow steps in the "To start with" section. Run `crawl.py`

## Possible improvements
1. Concurrent crawling: asyncio, Scrapy.
2. Database: pymongo.
3. Other cities support (possibly not).

## Bugs or suggestions
If you find any bugs or have any suggestions for me, welcome to create an issue or contact me via WeChat: 
![image](https://user-images.githubusercontent.com/58167095/196018421-f8c0d2cf-6c83-4cc1-8c1a-6bc4e49af965.png)
Or via email: 913248383@qq.com

## Policy Declaration
Use this spider under any legal policy and use crawled data for visualisation or machine learning purpose ONLY. Anyone using this code to make business profit should be responsible for any prosecutions that may incur in the future.
