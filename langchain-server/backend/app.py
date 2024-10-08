from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    HarmBlockThreshold,
    HarmCategory
)
from backend.template import prompt,SongGenerationPromptTemplate
# from langchain.globals import (
#     set_debug,
#     set_verbose
# )
# set_verbose(True)
# set_debug(True)
from langchain.schema import (
    HumanMessage,
    SystemMessage,
    AIMessage
)
from langchain_core.output_parsers import (
    StrOutputParser,
    JsonOutputParser,
    BaseCumulativeTransformOutputParser
)
from langchain_core.chat_history import(
    BaseChatMessageHistory,
    InMemoryChatMessageHistory
)
from langchain_core.runnables.history import RunnableWithMessageHistory
from dotenv import load_dotenv
load_dotenv()
llm=ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    safety_settings={
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_TOXICITY: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_DANGEROUS:HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HARASSMENT:HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_SEXUAL:HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_VIOLENCE:HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    },
    temperature=1,
    top_p=0.85,
    convert_system_message_to_human=True,
    max_retries=2,
    stream=True
)
store={}
def get_session_history(session_id:str)->BaseChatMessageHistory:
    if session_id not in store:
        store[session_id]=InMemoryChatMessageHistory()
    return store[session_id]
output_chain=prompt|llm
memorymodel=RunnableWithMessageHistory(output_chain,get_session_history)

def give_output(sessionId:str,human_message):

    config={"configurable":{"session_id":sessionId}}
    response=memorymodel.invoke([HumanMessage(content=human_message)],config=config)
    print(store)
    return response.content

def suggest_songs(conversation):
    
    messages = [
        (
            "system",
            """You are given the conversation of a user and a Mental Wellness AI,
Based on this conversation you should suggest some songs to users with a brief reason of why he should listen that song
As an output, only give me song and reason nothing else.
If you can't find a conversation please leave a message saying "Sorry, you must do a conversation before clicking on Suggest Songs button.""",
        ),
        ("human", conversation),
    ]
    result=llm.invoke(messages)
    return result.content

def suggest_podcast(conversation):
    messages = [
    (
        "system",
        """You are given the conversation of a user and a Mental Wellness AI,
    Based on this conversation you should suggest some podcasts to users with a brief reason of why he should listen that song
    As an output, only give me song and reason nothing else.
    If you can't find a conversation please leave a message saying "Sorry, you must do a conversation before clicking on Suggest Podcast button.""",
    ),
    ("human", conversation),
    ]
    result=llm.invoke(messages)
    return result.content

def suggest_online_resources(conversation):
    messages = [
    (
        "system",
        """You are given the conversation of a user and a Mental Wellness AI,
    Based on this conversation you should suggest some online resources like books, websites to users with a brief reason of why he should refer there
    As an output, only give me those online resources and reason nothing else.
    If you can't find a conversation please leave a message saying "Sorry, you must do a conversation before clicking on Suggest Podcast button.""",
    ),
    ("human", conversation),
    ]
    result=llm.invoke(messages)
    return result.content
