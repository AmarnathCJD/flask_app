import logging
from endpoints import routes
from config import PORT
from aiohttp.web import Application, run_app


app = Application()
app.add_routes(routes)
logging.info("starting server on port {}".format(PORT))
run_app(app, port=PORT)
