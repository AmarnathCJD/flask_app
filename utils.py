import json
import random
import re
import sre_constants

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


def worldpay(cc, mo, yr, cvv):
    r = post(
        "https://api.worldpay.com/v1/tokens",
        json={
            "reusable": False,
            "paymentMethod": {
                "type": "Card",
                "name": "Jenna M Ortega",
                "expiryMonth": mo,
                "expiryYear": yr,
                "cardNumber": cc,
                "cvc": cvv,
            },
            "clientKey": "L_C_11b32364-dca9-4f76-8ae6-4f42cca470ca",
        },
    ).json()
    print(r)
    if r.get("httpStatusCode") and r["httpStatusCode"] == 400:
        return {"error": "Invaid payment details"}
    check_api = "https://brewyork.co.uk/?wc-ajax=checkout"
    headers = {
        "authority": "brewyork.co.uk",
        "method": "POST",
        "path": "/?wc-ajax=checkout",
        "scheme": "https",
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "cookie": "gcl_au=1.1.721725957.1641706988; _gid=GA1.3.227382362.1641706989; _fbp=fb.2.1641706988933.1018948041; age_gate=18; mailchimp_landing_site=https%3A%2F%2Fbrewyork.co.uk%2Fshop%2F; woocommerce_items_in_cart=1; wp_woocommerce_session_e8af323805a4e9c3c4bb5c5adce7d325=b2bc7ee44fa2e690b024263916262f61%7C%7C1641879813%7C%7C1641876213%7C%7Cf9c347ea0c9a28d39aa49732829869ef; _ga=GA1.3.766310529.1641706988; mailchimp.cart.current_email=amarnathc@outlook.in; mailchimp_user_email=amarnathc%40outlook.in; _ga_EK76J8LVMM=GS1.1.1641706987.1.1.1641707185.0; woocommerce_cart_hash=c3b485e2e731863751b1e69d29b2d262; _gali=place_order",
        "origin": "https://brewyork.co.uk",
        "referer": "https://brewyork.co.uk/checkout/",
        "sec-ch-ua": '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Linux"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",
        "x-requested-with": "XMLHttpRequest",
    }

    payload = {
        "billing_first_name": "Jenna M",
        "billing_last_name": "Ortega",
        "billing_company": "",
        "billing_country": "GB",
        "billing_address_1": "326 Garratt Ln",
        "billing_address_2": "",
        "billing_city": "London",
        "billing_state": "SW18 4EJ",
        "billing_postcode": "SW18 4EJ",
        "billing_phone": "+44 20 8001 4628",
        "billing_email": "amarnathc@outlook.in",
        "account_password": "",
        "shipping_first_name": "",
        "shipping_last_name": "",
        "shipping_company": "",
        "shipping_country": "GB",
        "shipping_address_1": "",
        "shipping_address_2": "",
        "shipping_city": "",
        "shipping_state": "",
        "shipping_postcode": "",
        "order_comments": "",
        "shipping_method[0]": "flat_rate:11",
        "payment_method": "online_worldpay",
        "online_worldpay_payment_nonce": r["token"],
        "online_worldpay_payment_token_type": "",
        "wc_gc_cart_code": "",
        "woocommerce-process-checkout-nonce": "15700b877c",
        "_wp_http_referer": "/?wc-ajax=update_order_review",
    }

    data_2 = "billing_first_name=Jenna+M&billing_last_name=Ortega&billing_company=&billing_country=GB&billing_address_1=326+Garratt+Ln&billing_address_2=&billing_city=London&billing_state=SW18+4EJ&billing_postcode=SW18+4EJ&billing_phone=+%2B44+20+8001+4628&billing_email=amarnathc%40outlook.in&account_password=&shipping_first_name=&shipping_last_name=&shipping_company=&shipping_country=GB&shipping_address_1=&shipping_address_2=&shipping_city=&shipping_state=&shipping_postcode=&order_comments=&shipping_method%5B0%5D=flat_rate%3A11&payment_method=online_worldpay&online_worldpay_payment_token_type=&wc_gc_cart_code=&woocommerce-process-checkout-nonce=15700b877c&_wp_http_referer=%2F%3Fwc-ajax%3Dupdate_order_review&online_worldpay_payment_nonce={}".format(
        r["token"]
    )
    req = post(
        check_api,
        json=payload,
        headers=headers,
        data=data_2,
        params={"wc-ajax": "checkout"},
    )
    return json.dumps(req.text)


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
