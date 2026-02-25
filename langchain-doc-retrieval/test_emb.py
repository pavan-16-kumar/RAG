import os
from langchain_openai import OpenAIEmbeddings

key = os.getenv("OPENROUTER_API_KEY", "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")

emb = OpenAIEmbeddings(
    openai_api_key=key,
    openai_api_base="https://openrouter.ai/api/v1",
    model="openai/text-embedding-3-small"
)

try:
    res = emb.embed_query("hello world")
    print("Success, length:", len(res))
except Exception as e:
    print("Error:", repr(e))
