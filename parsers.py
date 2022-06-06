import aiohttp
from bs4 import BeautifulSoup
from aiohttp.web import json_response

from config import IMDB_API


async def imdb_search(query):
    """
    Search for a movie on IMDB
    """
    url = "https://api.themoviedb.org/3/search/multi"
    params = {
        "api_key": IMDB_API,
        "query": query,
        "language": "en-US",
        "include_adult": "true"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            resp = await resp.json()
            return resp.get("results")


async def google_search(query):
    """
    Search Google
    """
    url = "https://www.google.com/search"
    params = {
        "q": query,
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, allow_redirects=True, headers=headers) as resp:
            return await parse_google_response(await resp.text())


async def parse_google_response(response: str):
    soup = BeautifulSoup(response, "html.parser")
    titles = soup.find_all("h3", attrs={"class": "LC20lb"})

    descriptions = soup.find_all("div", attrs={"class": "VwiC3b"})
    cites = soup.find_all("cite", attrs={"class": "iUh30"})
    results = []
    for title, description, cite in zip(titles, descriptions, cites):
        results.append(
            {
                "title": title.text,
                "cite": cite.text,
                "description": description.text,
                "url": title.findParent("a", href=True)["href"]
            }
        )
    return {"success": True, "results": results}


async def parse_youtube_results(response):
    data = []
    estimatedResults = 0
    for result in response.get("contents", {}).get("twoColumnSearchResultsRenderer", {}).get("primaryContents", {}).get("sectionListRenderer", {}).get("contents", [])[0].get("itemSectionRenderer", {}).get("contents", []):
        if result.get("videoRenderer", {}):
            estimatedResults += 1
            data.append(
                {
                    "title": result.get("videoRenderer", {}).get("title", {}).get("runs", [{}])[0].get("text", ""),
                    "url": "https://www.youtube.com/watch?v=" + result.get("videoRenderer", {}).get("videoId", ""),
                    "description": ''.join([x.get("text", "") for x in result.get("videoRenderer", {}).get("detailedMetadataSnippets", [{}])[0].get("snippetText", {}).get("runs", [{}])]),
                    "thumbnail": result.get("videoRenderer", {}).get("thumbnail", {}).get("thumbnails", [{}])[0].get("url", ""),
                    "published": result.get("videoRenderer", {}).get("publishedTimeText", {}).get("simpleText", ""),
                    "channel": result.get("videoRenderer", {}).get("ownerText", {}).get("runs", [{}])[0].get("text", ""),
                    "channelUrl": "https://www.youtube.com/channel/" + result.get("videoRenderer", {}).get("ownerText", {}).get("runs", [{}])[0].get("navigationEndpoint", {}).get("browseEndpoint", {}).get("browseEndpointId", ""),
                    "channelThumbnail": "https://i.ytimg.com/vi/" + result.get("videoRenderer", {}).get("videoId", "") + "/hqdefault.jpg",
                    "duration": result.get("videoRenderer", {}).get("lengthText", {}).get("simpleText", ""),
                    "viewCount": result.get("videoRenderer", {}).get("viewCountText", {}).get("simpleText", ""),
                    "id": result.get("videoRenderer", {}).get("videoId", ""),
                }
            )
    return {"success": True, "results": data, "estimatedResults": estimatedResults}


async def goeval(code: str):
    """
    Evaluate code in Go
    """
    url = "https://go.dev/_/compile?"
    params = {"version": 2, "body": code, "withVet": True}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, params=params) as resp:
            resp = await resp.json()
            return {"success": True, "output": resp}


async def youtube_search(query: str):
    """
    Search YouTube
    """
    url = "https://www.youtube.com/youtubei/v1/search"
    params = {
        "key": "AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8",
        "prettyPrint": "false",
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
    }
    data = {
        'context': {
            'client': {
                'clientName': 'WEB',
                'clientVersion': '2.20220602.00.00',
                "newVisitorCookie": True,
            },
            "user": {
                "lockedSafetyMode": False,
            }
        },
        'query': query,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, params=params, headers=headers, json=data) as resp:
            return await parse_youtube_results(await resp.json())


async def write_error(error):
    """
    write error response
    """
    return json_response({"error": error, "success": False}, status=500, reason=error)


async def translate(query: str, language: str = "en-US", source_language: str = "en-US"):
    """
    Translate query
    """
    url = "https://translate.googleapis.com/translate_a/single"
    params = {
        "client": "gtx",
        "sl": source_language,
        "tl": language,
        "dt": "t",
        "q": query,
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            resp = await resp.json()
            result = {
                "translation": resp[0][0][0],
                "detectedLanguage": resp[2],
                "text": query,
                "success": True,
            }
            return result

