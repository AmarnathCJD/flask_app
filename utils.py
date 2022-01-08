from bs4 import BeautifulSoup
from requests import get, post


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


def stripe_check(cc_num, exp_mo, exp_year, cvv):
    url = "https://api.stripe.com/v1/payment_methods?type=card&card[number]={}&card[cvc]={}&card[exp_month]={}&card[exp_year]={}&billing_details[name]=qaa&billing_details[email]=amarnathcharichilil%40gmail.com&billing_details[address][country]=US&billing_details[address][postal_code]=10800&guid=ce5b0c34-b48f-44d4-a209-ee6f5b7ac1cf0ca195&muid=aec6dc80-792a-414b-84f8-77d506cfe99ebba8a2&sid=72db390b-035f-4038-a2cb-322e52220087141c48&key=pk_live_90yYxj8Ba8Lo2pzYSgH0FDOF&payment_user_agent=stripe.js%2Fe99643aff%3B+stripe-js-v3%2Fe99643aff%3B+checkout".format(
        cc_num, cvv, exp_mo, exp_year
    )
    with post(url) as p:
        print(p.json())
        payment = "https://api.stripe.com/v1/payment_pages/cs_live_b1xQfzEHKCQUBveaBHegBeikCWg1PEa9dTJT6ZDupqd7G4MHDbOW0FA8kR/confirm?eid=NA&payment_method={}&expected_amount=1300&expected_payment_method_type=card&key=pk_live_90yYxj8Ba8Lo2pzYSgH0FDOF".format(
            p.json()["id"]
        )
        return post(payment).json()


def paste(text):
    url = "https://nekobin.com/api/documents"
    r = post(url, json={"content": text})
    print(r.json())
    try:
        return r.json()
    except:
        return {"error": "nekobin host down"}
