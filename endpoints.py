from aiohttp.web import RouteTableDef, json_response

from parsers import google_search, imdb_search, translate, write_error, youtube_search

routes = RouteTableDef()


@routes.get("/google")
async def _google_search(request):
    query = request.query.get("query") or request.query.get("q")
    if not query:
        return await write_error("No query provided")
    results = await google_search(query)
    return json_response(results)


@routes.get("/imdb")
async def _imdb_search(request):
    query = request.query.get("q") or request.query.get("query")
    if not query:
        return await write_error("No query provided")
    results = await imdb_search(query)
    return json_response(results)


@routes.get("/youtube")
async def _youtube_search(request):
    query = request.query.get("query") or request.query.get("q")
    if not query:
        return await write_error("No query provided")
    results = await youtube_search(query)
    return json_response(results)


@routes.get("/translate")
async def _google_translate(request):
    text = request.query.get("text") or request.query.get("q")
    if not text:
        return await write_error("No 'text' provided")
    lang = request.query.get("lang") or request.query.get("l")
    if not lang:
        return await write_error("No 'lang' provided")
    src = request.query.get("src") or request.query.get("s")
    if not src:
        src = "en-US"
    results = await translate(text, lang, source_language=src)
    return json_response(results)


@routes.post("/paste")
async def _paste_nekobin(request):
    return json_response({"error": "not implemented"})


@routes.get("/")
async def _root(request):
    return json_response(
        {
            "endpoints": {
                "google": "/google",
                "imdb": "/imdb",
                "youtube": "/youtube",
                "translate": "/translate",
                "paste": "/paste",
            },
            "message": "welcome to the api",
        }
    )
