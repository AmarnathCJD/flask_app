import random
import re
import sre_constants

from bs4 import BeautifulSoup
from requests import get, post
from youtubesearchpython import VideosSearch as vs


def imdb_search(q):
    r = get(f"https://www.imdb.com/find?q={q}&ref_=nv_sr_sm")
    soup = BeautifulSoup(r.content, "html.parser")
    div = soup.find_all("div", attrs={"class": "findSection"})
    movies = div[0].findAll("td", attrs={"class": "result_text"})
    id = movies[0].find("a", href=True)["href"].replace("title", "").replace("/", "")
    movie = f"https://m.imdb.com/title/{id}"
    r = get(movie)
    soup = BeautifulSoup(r.content, "html.parser")
    img = soup.find("meta", attrs={"property": "twitter:image"})
    img = img.get("content") if img else None
    rating = soup.find(class_="sc-7ab21ed2-1 jGRxWM")
    rating = rating.text if rating else 0
    title = (soup.find("meta", attrs={"property": "twitter:title"})).get("content")
    desc = (soup.find("meta", attrs={"property": "twitter:description"})).get("content")
    genre = [x.text for x in soup.findAll("span", attrs={"class": "ipc-chip__text"})]
    return {
        "title": title,
        "description": desc,
        "rating": rating,
        "poster": img,
        "genre": genre,
    }


def google_search(query, limit=8):
    url = f"https://www.google.com/search?&q={query}&num=8"
    usr_agent = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/61.0.3163.100 Safari/537.36"
    }
    r = get(url, headers=usr_agent)
    soup = BeautifulSoup(r.text, "html.parser")
    r = soup.findAll("div", attrs={"class": "g"})
    d = soup.findAll("div", attrs={"class": "IsZvec"})
    results = []
    qp = 0
    for x, y in zip(r, d):
        qp += 1
        if qp > limit:
            break
        results.append(
            {
                "title": x.find("h3").text if x.find("h3") else "undefined",
                "url": x.find("a", href=True)["href"],
                "description": y.text if y else "",
            }
        )
    return results


def go_eval(code):
    url = "https://go.dev/_/compile?"
    params = {"version": 2, "body": code, "withVet": True}
    r = post(url, params=params).json()
    result = {}
    if r["Events"] == None:
        result["output"] = ""
        result["delay"] = 0
        result["kind"] = "unknown"
    else:
        result["output"] = r["Events"][0]["Message"]
        result["kind"] = "stdout"
        result["delay"] = r["Events"][0]["Delay"]
    if r["Errors"] != "":
        result["errors"] = r["Errors"]
    else:
        result["errors"] = ""
    return result


PROXIES = [
    "http://ejasxrod:xez7r0q328ce@209.127.191.180:9279",
    "http://ejasxrod:xez7r0q328ce@45.136.228.154:6209/",
    "http://ejasxrod:xez7r0q328ce@193.8.56.119:9183",
    "http://ejasxrod:xez7r0q328ce@45.94.47.66:8110/",
    "http://ejasxrod-rotate:xez7r0q328ce@p.webshare.io:80",
    "http://qslftemw:0x5vkh1h6x5d@209.127.191.180:9279/",
    "http://qslftemw:0x5vkh1h6x5d@45.95.96.132:8691/",
    "http://qslftemw:0x5vkh1h6x5d@45.95.96.187:8746/",
    "http://qslftemw:0x5vkh1h6x5d@45.95.96.237:8796/",
    "http://qslftemw:0x5vkh1h6x5d@45.136.228.154:6209/",
    "http://qslftemw:0x5vkh1h6x5d@45.94.47.66:8110/",
    "http://qslftemw:0x5vkh1h6x5d@45.94.47.108:8152/",
    "http://qslftemw:0x5vkh1h6x5d@193.8.56.119:9183/",
    "http://qslftemw:0x5vkh1h6x5d@45.95.99.226:7786/",
    "http://qslftemw:0x5vkh1h6x5d@45.95.99.20:7580/",
]


def paste(text):
    url = "https://nekobin.com/api/documents"
    r = post(url, json={"content": text}, proxies={"https": random.choice(PROXIES)})
    print(r.json())
    try:
        return r.json()
    except:
        return {"error": "nekobin host down"}


def infinite_checker(repl):
    regex = [
        r"\((.{1,}[\+\*]){1,}\)[\+\*].",
        r"[\(\[].{1,}\{\d(,)?\}[\)\]]\{\d(,)?\}",
        r"\(.{1,}\)\{.{1,}(,)?\}\(.*\)(\+|\* |\{.*\})",
    ]
    for match in regex:
        status = re.search(match, repl)
        return bool(status)


DELIMITERS = ("/", ":", "|", "_")


def seperate_sed(sed_string):
    if (
        len(sed_string) >= 3
        and sed_string[1] in DELIMITERS
        and sed_string.count(sed_string[1]) >= 2
    ):
        delim = sed_string[1]
        start = counter = 2
        while counter < len(sed_string):
            if sed_string[counter] == "\\":
                counter += 1

            elif sed_string[counter] == delim:
                replace = sed_string[start:counter]
                counter += 1
                start = counter
                break

            counter += 1

        else:
            return None
        while counter < len(sed_string):
            if (
                sed_string[counter] == "\\"
                and counter + 1 < len(sed_string)
                and sed_string[counter + 1] == delim
            ):
                sed_string = sed_string[:counter] + sed_string[counter + 1 :]

            elif sed_string[counter] == delim:
                replace_with = sed_string[start:counter]
                counter += 1
                break

            counter += 1
        else:
            return replace, sed_string[start:], ""

        flags = ""
        if counter < len(sed_string):
            flags = sed_string[counter:]
        return replace, replace_with, flags.lower()


def sed(fix, text):
    x, y, z = seperate_sed(text)
    if not x:
        return {"text": "You're trying to replace... nothing with something?"}
    try:
        if infinite_checker(x):
            return {"text": "Nice try -_-"}

        if "i" in z and "g" in z:
            fix = re.sub(x, y, fix, flags=re.I).strip()
        elif "i" in z:
            fix = re.sub(x, y, fix, count=1, flags=re.I).strip()
        elif "g" in z:
            fix = re.sub(x, y, fix).strip()
        else:
            fix = re.sub(x, y, fix, count=1).strip()
    except sre_constants.error as xc:
        return {"text": str(xc)}
    if len(text) >= 4096:
        {"text": "The result of the sed command was too long for telegram!"}
    return {"text": fix}


def yt_search(query: str, limit: int):
    try:
        v = vs(query, limit=limit).result()["result"]
    except (IndexError, KeyError, TypeError):
        return {"error": "No songs found!"}
    return v
