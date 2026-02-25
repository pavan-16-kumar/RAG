from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

# Prompt for the Conversational RAG
qa_system_prompt = """You are an assistant for question-answering tasks. 
Use the following pieces of retrieved context to answer the question. 
If you don't know the answer, or if an explicit section (like an 'Abstract') isn't formally labeled, 
summarize the main introductory ideas present in the context to best answer the user's intent. 
Keep the answer clear and avoid explicitly stating that you couldn't find a labeled section unless absolutely necessary.

Context:
{context}

Answer:
"""

QA_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", qa_system_prompt),
        ("human", "{input}"),
    ]
)

# Prompt for rephrasing user queries based on chat history
history_system_prompt = """Given a chat history and the latest user question \
which might reference context in the chat history, formulate a standalone question \
which can be understood without the chat history. Do NOT answer the question, \
just reformulate it if needed and otherwise return it as is."""

HISTORY_AWARE_PROMPT = ChatPromptTemplate.from_messages(
    [
        ("system", history_system_prompt),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
    ]
)
