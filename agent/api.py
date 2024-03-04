from ninja import Router
from agent.service import AgentService
from agent.schema import ChatSchema

router = Router(tags=["Agent"])

#GETS
@router.post("")
def conversation(request, payload: ChatSchema):
    service = AgentService()
    return service.agent(payload)
    