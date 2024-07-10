import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain.chains import LLMChain
from prompt import prompt_template
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_anthropic import ChatAnthropic
def setup_conversation():
    
    msgs = StreamlitChatMessageHistory()
    memory = ConversationBufferMemory(chat_memory=msgs, return_messages=True, memory_key="chat_history")

    prompt = ChatPromptTemplate(
        messages=[
            SystemMessagePromptTemplate.from_template(prompt_template),
            MessagesPlaceholder(variable_name="chat_history"),
            HumanMessagePromptTemplate.from_template("{human_input}"),
        ]
    )
    
    llm = ChatAnthropic(model='claude-3-5-sonnet-20240620',temperature=0)
    # llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")
    conversation = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=True,
        memory=memory
    )
    return conversation

def handle_user_input(user_input):
    conversation = setup_conversation()
    response = conversation.predict(human_input=user_input)
    return response