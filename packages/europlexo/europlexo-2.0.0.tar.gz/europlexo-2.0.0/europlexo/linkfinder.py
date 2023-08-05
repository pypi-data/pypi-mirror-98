from re import findall, search

import requests
from bs4 import BeautifulSoup as bs
from europlexo.dispatcher.deltabit import get_DeltaBit_download_link
from europlexo.dispatcher.turbovid import get_TurboVid_download_link


class LinkFinder:
    def __init__(self, url, sub=True):
        """Instance with url,sub and info,soup to compute one-time"""
        self._url = url
        self._sub = sub
        self._soup = bs(requests.get(url).text, "html.parser")
        self.info = [
            (n, int(x.group(1)))
            for n, div in self._get_seasons_html_div().items()
            for x in [
                search(r"(?:[0-9]{1,2}×)(?!00)([0-9]{1,2})", e)
                for e in str(div).split("<br/>")
            ]
            if x
        ]

    def _is_season(self, div):
        """Check if a html div is a season"""
        try:
            return (
                div["class"][0] == "su-spoiler"
                and ("SUB" in div.text.split("\n")[0]) == self._sub
            )
        except KeyError:
            return False

    def _is_episode_out(self, season, episode):
        """Check if an episode is out"""
        return (season, episode) <= max(self.info)

    def _get_real_season_number(self, div):
        """Get the real season number (possible seasons missing)"""
        return int(search(r"(?:STAGIONE\s+)(\d{1,2})(?:.+)", str(div)).group(1))

    def _get_seasons_html_div(self):
        """Get all seasons in html div"""
        return {
            self._get_real_season_number(div): div
            for div in self._soup.find_all("div")
            if self._is_season(div)
        }

    def _get_crypted_links(self, season=None, episode=None):
        """Get html crypted links for an episode, if not specified get last"""
        if not season and not episode:
            season, episode = max(self.info)
            episode += 1
        try:
            div = [
                d
                for d in str(self._get_seasons_html_div()[season]).split("<br/>")
                if search(r"\d{1,2}×0?" + str(episode) + r"(?!\d)", d)
            ][-1]
        except IndexError:
            div = ""
        return (
            season,
            episode,
            findall(r"(?:<a href=\")([^\s]+)(?:\".+?>)([a-zA-Z0-9]+)", div),
        )

    def _site_dispacher(self, link, site):
        """Call the link finder for every site"""
        sites = {
            "DeltaBit": get_DeltaBit_download_link,
            "Turbovid": get_TurboVid_download_link,
        }
        return sites[site](link) if site in sites else None

    def get_episodes_list(self):
        return self.info

    def get_direct_links(self, season=None, episode=None):
        """Get all the direct links for an episode, if not specified get last"""
        if season and episode and not self._is_episode_out(season, episode):
            raise ValueError(f"Episode {season}×{episode} isn't out yet")
        else:
            season, episode, crypted_links = self._get_crypted_links(season, episode)
        direct_links = sorted(
            [
                link
                for link in [self._site_dispacher(link, n) for link, n in crypted_links]
                if link
            ],
            key=lambda x: x[1],
            reverse=True,
        )
        if direct_links:
            return direct_links[0]
        else:
            raise ValueError(f"No link found for episode {season}×{episode}.")
