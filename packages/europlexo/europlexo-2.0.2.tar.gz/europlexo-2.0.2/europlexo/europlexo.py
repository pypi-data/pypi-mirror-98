from argparse import ArgumentParser
from datetime import datetime
from os import makedirs, path, walk
from re import search
from subprocess import PIPE, STDOUT, Popen

from colorifix.colorifix import Color, paint
from emoji import emojize
from europlexo.linkfinder import LinkFinder
from europlexo.manage import get_config, manage
from halo import Halo
from pymortafix.utils import multisub
from requests import get
from requests.exceptions import ConnectionError, MissingSchema
from telegram import Bot

CONFIG = get_config()
SPINNER = Halo()


def get_eurostreaming_site():
    auto_site = CONFIG.get("eurostreaming-master")
    manual_site = CONFIG.get("eurostreaming")
    try:
        site = search(r"(?:site:)([\w\.\/\:]+)(?:\W)", get(auto_site).text).group(1)
        return site if search("http", site) else "https://{}".format(site)
    except (ConnectionError, AttributeError):
        try:
            get(manual_site)
            return manual_site
        except (ConnectionError, MissingSchema):
            return None


def get_downloaded_episodes(folder_name):
    tree = list(walk(path.join(CONFIG.get("path"), folder_name)))
    if not tree:
        return []
    return sorted(
        [
            (int(seep.group(1)), int(seep.group(2)))
            for _, _, files in tree[1:]
            for file in files
            if (seep := search(r"s(\d+)e(\d+)", file)) and not search("part", file)
        ]
    )


def episodes_to_download(folder, page, mode):
    online_eps = page.get_episodes_list()
    downloaded_eps = get_downloaded_episodes(folder)
    if mode == "full":
        eps_to_download = [ep for ep in online_eps if ep not in downloaded_eps]
    elif mode == "new":
        last_downloaded = max(downloaded_eps) if downloaded_eps else (0, 0)
        eps_to_download = [ep for ep in online_eps if ep > last_downloaded]
    elif mode == "last":
        last_season_online = max(online_eps)[0] if online_eps else 0
        last_online_season = [
            (se, ep) for se, ep in online_eps if se == last_season_online
        ]
        eps_to_download = [ep for ep in last_online_season if ep not in downloaded_eps]
    return eps_to_download


def sanitize_name(name):
    return multisub({":": "", " ": "_"}, name)


def send_telegram_log(name, season, episode, success=True):
    config = get_config()
    bot_token = config.get("telegram-bot-token")
    chat_id = config.get("telegram-chat-id")
    if bot_token and chat_id:
        emoji = ":white_check_mark:" if success else ":no_entry:"
        title = "Download Succesfull" if success else "Download Failed"
        msg = (
            f"{emoji} *{title}* {emoji}\n\n"
            f":clapper: *{name}*\n"
            f":cyclone: Episode *{season}*×*{episode}*\n"
            f":calendar: {datetime.now():%d.%m.%Y}\n"
        )
        Bot(bot_token).send_message(
            chat_id, emojize(msg, use_aliases=True), parse_mode="Markdown"
        )


def download_video(url, name, filename):
    popen = Popen(
        f"{CONFIG.get('youtube-dl-path')} {url} -o '{filename}' --no-check-certificate",
        shell=True,
        stdout=PIPE,
        stderr=STDOUT,
    )
    while True:
        next_line = popen.stdout.readline()
        line = next_line.rstrip().decode("utf8")
        if line == "" and popen.poll() is not None:
            break
    return filename


def download(action):
    serie_list = [list(serie.values()) for serie in CONFIG.get("serie")]
    for name, url, folder, lang, mode in serie_list:
        SPINNER.start(f"Scanning {paint(name,Color.BLUE)}")
        eurostreaming_url = path.join(get_eurostreaming_site(), url)
        page = LinkFinder(eurostreaming_url, sub=lang == "eng")
        eps_to_download = episodes_to_download(folder, page, mode)
        for se, ep in eps_to_download:
            SPINNER.start(
                f"Finding link for {paint(name,Color.BLUE)} "
                f"{paint(f'{se}x{ep}',Color.MAGENTA)}"
            )
            try:
                link = page.get_direct_links(se, ep)
            except ValueError:
                SPINNER.fail(
                    f"Fail to get link for {paint(name,Color.BLUE)} "
                    f"{paint(f'{se}x{ep}',Color.MAGENTA)}"
                )
                send_telegram_log(name, se, ep, success=False)
                break
            if action == "run":
                basepath = path.join(CONFIG.get("path"), folder, f"Stagione {se}")
                if not path.exists(basepath):
                    makedirs(basepath)
                filename = path.join(
                    basepath, f"{sanitize_name(name)}_s{int(se):02d}e{ep:02d}.mp4"
                )
                SPINNER.start(
                    f"Downloading {paint(name,Color.BLUE)} "
                    f"{paint(f'{se}x{ep}',Color.MAGENTA)}"
                )
                try:
                    download_video(link, name, filename)
                except Exception:
                    SPINNER.fail(
                        f"Fail to download {paint(name,Color.BLUE)} "
                        f"{paint(f'{se}x{ep}',Color.MAGENTA)}"
                    )
                    send_telegram_log(name, se, ep, success=False)
                    break
                SPINNER.succeed(
                    f"Downloaded {paint(name,Color.BLUE)} "
                    f"{paint(f'{se}x{ep}',Color.MAGENTA)}"
                )
                send_telegram_log(name, se, ep)
            elif action == "test":
                SPINNER.info(
                    f"Found {paint(name, Color.BLUE)} "
                    + paint(f"{se}x{ep}", Color.MAGENTA)
                )


def argparsing():
    parser = ArgumentParser(
        prog="Europlexo",
        description="We are pirates.",
        usage=("europlexo action:{manage, run, test}"),
    )
    parser.add_argument(
        "action",
        type=str,
        nargs=1,
        help="action to do",
        choices=("manage", "run", "test"),
    )
    return parser.parse_args()


def main():
    try:
        args = argparsing()
        if args.action[0] == "manage":
            manage(get_eurostreaming_site())
        if args.action[0] in ("run", "test"):
            download(args.action[0])
    except KeyboardInterrupt:
        SPINNER.stop()
        print(f"{paint('Interrupted!',Color.RED)} Saving...")


if __name__ == "__main__":
    main()
