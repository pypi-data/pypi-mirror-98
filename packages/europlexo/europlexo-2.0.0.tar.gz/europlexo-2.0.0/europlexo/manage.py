from datetime import datetime
from json import dump, load
from os import path, walk
from re import search

from colorifix.colorifix import Background, Color, Style, erase, paint
from europlexo.seriesfinder import get_suggestion_list
from halo import Halo
from pymortafix.utils import direct_input, multisub, strict_input
from requests import get
from requests.exceptions import ConnectionError, MissingSchema
from telegram import Bot
from telegram.error import InvalidToken

SPINNER = Halo()

# --- Config file


def get_config():
    return load(open(f"{path.abspath(path.dirname(__file__))}/config.json"))


def save_config(config_dict):
    return dump(
        config_dict,
        open(f"{path.abspath(path.dirname(__file__))}/config.json", "w"),
        indent=4,
    )


def remove_serie(index):
    config = get_config()
    config["serie"] = [
        serie for i, serie in enumerate(config.get("serie")) if index != i
    ]
    save_config(config)


def add_serie(name, link, folder, lang, mode):
    new = {"name": name, "site": link, "folder": folder, "language": lang, "mode": mode}
    config = get_config()
    config["serie"] += [new]
    save_config(config)


def add_new_path(path):
    config = get_config()
    config["path"] = path
    save_config(config)


def is_folder_unique(folder_name):
    folders = [serie.get("folder") for serie in get_config().get("serie")]
    return folder_name not in folders


def add_telegram_config(bot_token, chat_id):
    config = get_config()
    config["telegram-bot-token"] = bot_token
    config["telegram-chat-id"] = chat_id
    save_config(config)


def add_youtube_dl(ytd_path):
    config = get_config()
    config["youtube-dl-path"] = ytd_path
    save_config(config)


def add_eurostreaming_site(es_url):
    config = get_config()
    config["eurostreaming"] = es_url
    save_config(config)


# --- Pretty Print


def pprint_row(serie_name, lang, mode, index=False, remove=False):
    if index and remove:
        return paint(f"[#] {serie_name} [{mode}]", background=Background.RED)
    if index and not remove:
        ret_str = paint("[>] ", Color.GREEN) + paint(serie_name, Color.GREEN)
    else:
        ret_str = "[ ] " + paint(serie_name)
    return ret_str + paint(f" ({lang}) ", Color.CYAN) + paint(f"[{mode}]", Color.BLUE)


def pprint_serie(serie_list, index, remove=None):
    if not serie_list:
        return "No serie added.."
    return "\n".join(
        [
            pprint_row(name, lang, mode, index == i, remove=remove)
            for i, (name, _, _, lang, mode) in enumerate(serie_list)
        ]
    )


def pprint_actions(mode=None):
    if mode == "confirm":
        actions = {"y": "confirm", "n": "back"}
    elif mode == "add":
        actions = {"ws": "move", "c": "confirm", "b": "back"}
    elif mode == "back":
        actions = {"b": "back"}
    elif mode == "settings":
        actions = {
            "u": "backup",
            "r": "restore",
            "p": "path",
            "t": "telegram",
            "y": "youtube-dl",
            "e": "eurostreaming",
            "b": "back",
        }
    elif mode == "path":
        actions = {"e": "edit", "b": "back"}
    else:
        actions = {
            "ws": "move",
            "a": "add",
            "r": "remove",
            "e": "settings",
            "q": "quit",
        }
    return (
        "-" * sum(len(action) + 5 for action in actions.values())
        + "\n"
        + " ".join(
            f"[{paint(key,style=Style.BOLD)}]:{paint(action,Color.MAGENTA)}"
            for key, action in actions.items()
        )
    )


def pprint_query(query_list, selected):
    return "\n".join(
        paint(f"[>] {name}", Color.GREEN) if selected == i else f"[ ] {name}"
        for i, (name, _) in enumerate(query_list)
    )


def pprint_settings():
    config = get_config()
    labels = ("Eurostreaming", "Current path", "Backup", "Telegram", "Youtube-dl")
    eurostreaming_url = paint(config.get("eurostreaming"), Color.BLUE)
    path_str = paint(config.get("path"), Color.BLUE)
    backup = get_last_backup()
    backup_str = paint(backup, Color.BLUE)
    telegram_str = (
        (
            paint(config.get("telegram-bot-token"), Color.BLUE)
            + paint(":", style=Style.BOLD)
            + paint(config.get("telegram-chat-id"), Color.BLUE)
        )
        if config.get("telegram-bot-token")
        else ""
    )
    youtube_dl_str = paint(config.get("youtube-dl-path"), Color.BLUE)
    values = (eurostreaming_url, path_str, backup_str, telegram_str, youtube_dl_str)
    return "\n".join(
        f"{paint(lab,style=Style.BOLD)}: {val}" for lab, val in zip(labels, values)
    )


def get_last_backup():
    _, _, files = list(walk("."))[0]
    backups = sorted(
        [file for file in files if search(r"europlexo-backup\.json$", file)],
        reverse=True,
    )
    return backups[0] if backups else ""


def recap_new_serie(name, url, folder, lang, mode):
    return (
        f"Name: {paint(name,Color.BLUE)}\n"
        f"Link: {paint(url,Color.BLUE)}\n"
        f"Folder: {paint(folder,Color.BLUE)}\n"
        f"Language: {paint(lang,Color.BLUE)}\n"
        f"Mode: {paint(mode,Color.BLUE)}"
    )


# --- Input


def is_bot_valid(token):
    try:
        Bot(token)
        return True
    except InvalidToken:
        return False


def is_yt_download_valid(ytd_path):
    return search(r"youtube-dl$", ytd_path) and path.exists(ytd_path)


def is_eurostreaming_valid(es_url):
    try:
        get(es_url)
        return search("eurostreaming", es_url)
    except Exception:
        return False


# --- Manage


def manage(eurostreaming_url):
    index = 0
    k = "start"
    while k != "q":
        serie_list = [list(serie.values()) for serie in get_config().get("serie")]
        print(pprint_serie(serie_list, index))
        print(pprint_actions())
        k = direct_input(choices=("w", "s", "e", "a", "r", "q"))
        erase(len(serie_list or [0]) + 2)

        if k in ("w", "s"):
            if k == "w" and index:
                index -= 1
            if k == "s" and index < len(serie_list) - 1:
                index += 1

        if k == "e":
            e_k = "start"
            while e_k != "b":
                print(pprint_settings())
                print(pprint_actions(mode="settings"))
                e_k = direct_input(choices=("u", "r", "p", "t", "y", "e", "b"))
                erase(7)
                if e_k == "p":
                    base = paint("Path", style=Style.BOLD) + ": "
                    new_path = strict_input(
                        base,
                        wrong_text=paint("Wrong path! ", Color.RED) + base,
                        check=path.exists,
                        flush=True,
                    )
                    add_new_path(new_path)
                    e_k = ""
                elif e_k == "r":
                    backup_filename = get_last_backup()
                    if backup_filename:
                        backup_dict = load(open(backup_filename))
                        save_config(backup_dict)
                elif e_k == "u":
                    now = datetime.now()
                    config = get_config()
                    dump(
                        config,
                        open(f"{now:%Y-%m-%d}_europlexo-backup.json", "w"),
                        indent=4,
                    )
                elif e_k == "t":
                    base = paint("Telegram bot token", style=Style.BOLD) + ": "
                    telegram_bot_token = strict_input(
                        base,
                        wrong_text=paint("Invalid token! ", Color.RED) + base,
                        check=is_bot_valid,
                        flush=True,
                    )
                    base = paint("Telegram chat ID", style=Style.BOLD) + ": "
                    telegram_chat_id = strict_input(
                        base,
                        wrong_text=paint("Invalid chat ID! ", Color.RED) + base,
                        regex=r"\-?\d+$",
                        flush=True,
                    )
                    add_telegram_config(telegram_bot_token, telegram_chat_id)
                elif e_k == "y":
                    base = paint("Youtube-dl path", style=Style.BOLD) + ": "
                    youtube_dl_path = strict_input(
                        base,
                        wrong_text=paint(
                            "Wrong path, MUST include 'youtube-dl'! ", Color.RED
                        )
                        + base,
                        check=is_yt_download_valid,
                        flush=True,
                    )
                    add_youtube_dl(youtube_dl_path)
                elif e_k == "e":
                    base = paint("Eurostreaming site", style=Style.BOLD) + ": "
                    eurostreaming_url = strict_input(
                        base,
                        wrong_text=paint("Wrong site, unreacheable! ", Color.RED)
                        + base,
                        check=is_eurostreaming_valid,
                        flush=True,
                    )
                    add_eurostreaming_site(eurostreaming_url)

        if serie_list and k == "r":
            print(pprint_serie(serie_list, index, remove=True))
            print(pprint_actions(mode="confirm"))
            r_k = direct_input(choices=("y", "n"))
            if r_k == "y":
                remove_serie(index)
                index = 0
            erase(len(serie_list) + 2)

        if k == "a":
            q_index = 0
            q_k = "start"
            # serie search
            query = input(paint("Serie name", style=Style.BOLD) + ": ")
            erase()
            SPINNER.start(f"Searching for {paint(query,Color.BLUE)}")
            query_list = get_suggestion_list(eurostreaming_url, query)
            SPINNER.stop()
            if not query_list:
                print(f"No serie found with {paint(query,Color.BLUE)}!")
                print(pprint_actions(mode="back"))
                q_k = direct_input(choices=("b",))
                erase(3)
            while q_k not in ("c", "b"):
                print(pprint_query(query_list, q_index))
                print(pprint_actions(mode="add"))
                q_k = direct_input()
                erase(len(query_list) + 2)
                if q_k in ("w", "s"):
                    if q_k == "w" and q_index:
                        q_index -= 1
                    if q_k == "s" and q_index < len(query_list) - 1:
                        q_index += 1
            # new serie
            if q_k == "c":
                base = paint("Folder name", style=Style.BOLD) + ": "
                folder = strict_input(
                    base,
                    f"{paint('Folder name must be unique!', Color.RED)} {base}",
                    check=is_folder_unique,
                    flush=True,
                )
                base = paint("Language [eng|ita]", style=Style.BOLD) + ": "
                lang = strict_input(
                    base,
                    f"{paint('Wrong language!',Color.RED)} {base}",
                    choices=("eng", "ita"),
                    flush=True,
                )
                base = paint("Mode [full|new|last]", style=Style.BOLD) + ": "
                mode = strict_input(
                    base,
                    f"{paint('Mode must be full, new or last!', Color.RED)} {base}",
                    choices=("full", "new", "last"),
                    flush=True,
                )
                print(recap_new_serie(*query_list[q_index], folder, lang, mode))
                print(pprint_actions(mode="confirm"))
                c_k = direct_input(choices=("y", "n"))
                if c_k == "y":
                    name, link = query_list[q_index]
                    link = multisub({eurostreaming_url: "", "/": ""}, link)
                    add_serie(name, link, folder, lang, mode)
                erase(7)
                index = 0
