import logging

from aiohttp.web import Application, run_app

from config import PORT
from endpoints import routes

app = Application()
app.add_routes(routes)
logging.info("starting server on port {}".format(PORT))
run_app(app, port=PORT)
