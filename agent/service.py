import langchain
import os
from dotenv import load_dotenv
from agent.utils import search_travily
from agent.models import Conversation
from agent.schema import ChatSchema
from langchain.agents import AgentExecutor
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
from langchain.agents.format_scratchpad.openai_tools import (format_to_openai_tool_messages,)
from langchain_core.prompts import ChatPromptTemplate as cp
from langchain_core.messages import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langchain.prompts import MessagesPlaceholder

load_dotenv()
class AgentService:
    
    def agent(self, payload:ChatSchema):

        MEMORY_KEY = 'chat_history'
        
        langchain.verbose = False

        llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=os.getenv("OPEN_API_KEY"), temperature=0)
  
        prompt = cp.from_messages([("system", "You are a sales agent capable of suggesting and recommending product sales in an effective and engaging way."), 
                                    MessagesPlaceholder(variable_name=MEMORY_KEY),
                                   ("user", "{input}"),
                                    MessagesPlaceholder(variable_name="agent_scratchpad"),
                                   ])
        
        chat_history = []
            
        tools = search_travily()

        agent = (
                {
                    "input": lambda x: x["input"],
                    "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                        x["intermediate_steps"]
                    ),
                    "chat_history": lambda x: x["chat_history"],
                }
                | prompt
                | llm
                | OpenAIToolsAgentOutputParser()
            )
        
        
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
        
        
        if not Conversation.objects.all():
            ai_response = agent_executor.invoke({"input": payload.dict().get("message"), "chat_history": chat_history})
            chat_history.extend(
                    [
                        HumanMessage(content=payload.dict().get("message")),
                        AIMessage(content=ai_response["output"]),
                    ]
                    )
            
        else:
            ai_response = agent_executor.invoke({"input": Conversation.objects.filter().last().last_message_human, "chat_history": chat_history})
            chat_history.extend(
                                [
                                    HumanMessage(content=Conversation.objects.filter().last().last_message_human),
                                    AIMessage(content=ai_response["output"]),
                                ]
                                )
        
        ai_response = agent_executor.invoke({"input": payload.dict().get("message"), "chat_history": chat_history})
 
        if not Conversation.objects.filter(last_message_human=payload.dict().get("message")).first():
            history = {"last_message_human": payload.dict().get("message"), "last_message_ai": ai_response['output']}
            Conversation.objects.create(**history)
                    
        
        return str(ai_response['output'])    
     