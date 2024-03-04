from agent.api import router
from ninja import NinjaAPI

api = NinjaAPI()

api.add_router("/agent/", router)