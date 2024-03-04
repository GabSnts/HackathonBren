import langchain
from agent.utils import search_travily
from agent.models import Conversation
from agent.schema import ChatSchema
from langchain.agents import create_openai_functions_agent
from langchain.agents import AgentExecutor
from langchain_core.prompts import ChatPromptTemplate as cp
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langchain.prompts import MessagesPlaceholder

class AgentService:
    
    def agent(self, payload:ChatSchema):
        langchain.verbose = False

        llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key="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", temperature=0)
  
        prompt = cp.from_messages([("system", "You are a sales agent capable of suggesting and recommending product sales in an effective and engaging way."), 
                                   ("user", "{input}"),
                                    MessagesPlaceholder(variable_name="agent_scratchpad"),
                                   ])
            
        tools = search_travily()
        agent = create_openai_functions_agent(llm, tools, prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
        
        
        ai_response = agent_executor.invoke(
                                            {
                                                "chat_history": [
                                                    HumanMessage(content=Conversation.objects.filter().first().last_message_human),
                                                    AIMessage(content=Conversation.objects.filter().first().last_message_ai),
                                                ],
                                                "input": payload,
                                            }
                                        )    
        if not Conversation.objects.filter(last_message_human=payload.dict().get("message")).first():
            history = {"last_message_human": payload.dict().get("message"), "last_message_ai": ai_response.get("output")}
            Conversation.objects.create(**history)
                    
        
        return str(ai_response.get("output"))    
     