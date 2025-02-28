from .signing import register_routes as route_signing
from .tasks import register_routes as route_tasks

def register_routes(app, database, bcrypt):
	route_signing(app, database, bcrypt)
	route_tasks(app, database, bcrypt)