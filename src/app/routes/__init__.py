from .api import register_routes as route_api
from .pages import register_routes as route_pages

def register_routes(app, database, bcrypt):
	route_api(app, database, bcrypt)
	route_pages(app, database, bcrypt)