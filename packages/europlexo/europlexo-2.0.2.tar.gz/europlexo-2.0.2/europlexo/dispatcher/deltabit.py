from re import findall, sub
from time import sleep

import cloudscraper
import requests
from bs4 import BeautifulSoup as bs


class SiteError(Exception):
    pass


def encrypt2deltabit(linkup_url):
    return requests.get(linkup_url.replace("delta", "adelta"), allow_redirects=True).url


def deltabit2deltabitGen(deltabit_url):
    soup = bs(requests.get(deltabit_url, allow_redirects=True).text, "html.parser")
    try:
        get_attrs = sub(
            r"download_video|\'|\(|\)",
            "",
            [l["onclick"] for l in soup.find_all("a") if "onclick" in l.attrs][0],
        ).split(",")
    except IndexError:
        raise SiteError("DeltaBit not working!")
    return "https://deltabit.co/dl?op=download_orig&id={}&mode={}&hash={}".format(
        get_attrs[0], "o", get_attrs[2]
    )


def deltabitGen2deltabitCloud(deltabit_gen_url):
    scraper = cloudscraper.create_scraper()
    urls = list()
    tries, max_tries = 0, 10
    while len(urls) == 0 and tries < max_tries:
        tries += 1
        urls = findall(
            r"(?:onclick=\"window.open\(\')([^\s]+)(?:\')",
            scraper.get(deltabit_gen_url).text,
        )
        sleep(1)
    return urls[0] if urls else None


def get_DeltaBit_download_link(url):
    try:
        return deltabitGen2deltabitCloud(deltabit2deltabitGen(encrypt2deltabit(url)))
    except SiteError:
        return None
