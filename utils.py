import json

from bs4 import BeautifulSoup
from requests import get


def imdb(q):
    r = get(f"https://www.imdb.com/find?q={q}&ref_=nv_sr_sm")
    soup = BeautifulSoup(r.content, "html.parser")
    div = soup.find_all("div", attrs={"class": "findSection"})
    movies = div[0].findAll("td", attrs={"class": "result_text"})
    id = movies[0].find("a", href=True)["href"].replace("title", "").replace("/", "")
    movie = f"https://m.imdb.com/title/{id}"
    r = get(movie)
    img = soup.find("meta", attrs={"property": "twitter:image"})
    img = img.get("content") if img else None
    rating = (
        soup.find(
            "span",
            attrs={"class": "AggregateRatingButton__RatingScore-sc-1ll29m0-1 iTLWoV"},
        )
    ).text or 0
    title = (soup.find("meta", attrs={"property": "twitter:title"})).get("content")
    desc = (soup.find("meta", attrs={"property": "twitter:description"})).get("content")
    genre = [x.text for x in soup.findAll("span", attrs={"class": "ipc-chip__text"})]
    js = json.dumps(
        {
            "title": title,
            "description": desc,
            "rating": rating,
            "poster": img,
            "genre": genre,
        }
    )
    return js
