import json
import requests
from bs4 import BeautifulSoup as bs
import re
import csv
import time
from config import *




def init_headers(headers: dict):
    """Initial request to obtain CSRF token for further requests. Update request headers."""
    response = requests.get(url="https://www.zomato.com/webroutes/auth/csrf", headers=headers)
    data = response.json()
    csrf = data.get("csrf", "")
    headers["x-zomato-csrft"] = csrf


def init_payload(filename):
    """Read initial payload for initial request. See README for more details."""
    source = json.loads(open(filename, 'r').read())
    return source


def build_filters(payload: dict, params: dict):
    """Build the payload for next request based on the last request."""
    original_filters = payload["filters"]
    json_filters = json.loads(original_filters)
    json_filters["searchMetadata"]["getInactive"] = params["getInactive"]
    json_filters["searchMetadata"]["hasMore"] = params["hasMore"]
    json_filters["searchMetadata"]["totalResults"] = params["totalResults"]
    json_filters["searchMetadata"]["postbackParams"] = json.loads(params["postbackParams"])
    json_filters["searchMetadata"]["previousSearchParams"] = json.loads(params["previousSearchParams"])
    for f in json_filters["appliedFilter"]:
        f["postKey"] = json.loads(f["postKey"])
    temp = []
    for f in json_filters["searchMetadata"]["previousSearchParams"]["PreviousSearchFilter"]:
        temp.append(json.loads(f) if f else "")
    json_filters["searchMetadata"]["previousSearchParams"]["PreviousSearchFilter"] = temp

    json_filters["searchMetadata"]["postbackParams"] = json.dumps(json_filters["searchMetadata"]["postbackParams"], separators=(',', ':'))
    for f in json_filters["appliedFilter"]:
        f["postKey"] = json.dumps(f["postKey"], separators=(',', ':'))
    temp = []
    for p in json_filters["searchMetadata"]["previousSearchParams"]["PreviousSearchFilter"]:
        temp.append(json.dumps(p, separators=(',', ':')) if p else '')
    json_filters["searchMetadata"]["previousSearchParams"]["PreviousSearchFilter"] = temp
    json_filters["searchMetadata"]["previousSearchParams"] = json.dumps(json_filters["searchMetadata"]["previousSearchParams"], separators=(',', ':'))
    filters = json.dumps(json_filters, separators=(',', ':'))
    return filters


def get_restaurants(session):
    """Get restaurants information of one district by given pages. Each page contains 12 restaurants."""
    payload = init_payload(filename=f"{DISTRICT}_source.json")
    res = []
    file = open(f"{DISTRICT}.json", 'w')
    for _ in range(PAGES):
        response = session.post(url=REQUEST_URL, json=payload)
        data = response.json()
        if len(data.get("sections", {}).get("SECTION_SEARCH_RESULT", [])) > 0:
            print(f"Successfully crawled page {_}.")
            params = data["sections"]["SECTION_SEARCH_META_INFO"]["searchMetaData"]
            filters = build_filters(payload, params)
            payload["filters"] = filters
            res.append(data)
        else:
            print(f"Unsuccessfully crawled page {_}.")
    json.dump(res, file)


def get_coordinates(session):
    """Read from pre-processed file and get geo coordinates of the restaurants. Store them
    to csv file.
    """
    f = open("restaurant_data.csv", 'a')
    writer = csv.writer(f)
    filename = f"{DISTRICT}.json"
    with open(filename) as r:
        data = json.load(r)
        for ss in data:
            search_results = ss["sections"]["SECTION_SEARCH_RESULT"]
            for search_result in search_results:
                click_url = search_result["cardAction"]["clickUrl"]
                restaurant_name = search_result["info"]["name"]
                image = search_result["info"]["image"]["url"]
                rating = search_result["info"]["rating"]["aggregate_rating"]
                url = ROOT_URL + click_url
                response = session.get(url=url)
                content = response.text
                soup = bs(content, "html.parser")
                # Fast match with coordinates of the restaurant
                url_regex = r"https://www.google.com/maps"
                links = [a.get("href") for a in soup.find_all("a")]
                geo_url = ""
                for link in links:
                    if link:
                        if re.search(url_regex, link):
                            geo_url = link
                            break
                destination = geo_url.split("=")[-1].split(",")
                lat = float(destination[0])
                lon = float(destination[1])
                writer.writerow([
                    restaurant_name, image, rating, url, lat, lon
                ])
                f.flush()
                # Sleep 1 second to avoid restriction
                time.sleep(SUBPAGE_REQUEST_DELAY)


def main():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 "
                      "Safari/537.36",
        "cookie": COOKIE,
        "origin": ROOT_URL,
    }
    session = requests.Session()
    init_headers(headers)
    session.headers = headers
    get_restaurants(session)
    get_coordinates(session)


if __name__ == '__main__':
    main()
