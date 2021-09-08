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
    soup = BeautifulSoup(r.content, "html.parser")
    img = soup.find("meta", attrs={"property": "twitter:image"})
    img = img.get("content") if img else None
    rating = soup.find(
        "span",
        attrs={"class": "AggregateRatingButton__RatingScore-sc-1ll29m0-1 iTLWoV"},
    )
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


def google_search(query, limit=5):
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
                "title": x.find("a", href=True)["href"],
                "url": x.find("h3").text if x.find("h3") else "undefined",
                "description": y.text,
            }
        )
    return results
