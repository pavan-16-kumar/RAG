from langchain_openai import ChatOpenAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from src.config.settings import settings
from src.config.prompts import QA_PROMPT
from src.core.vector_store import VectorStoreManager
from src.utils.logger import logger
import os

class QAService:
    """Service layer orchestrating the Retrieval-Augmented Generation (RAG) pipeline."""
    
    def __init__(self):
        self.vector_store_manager = VectorStoreManager()
        self.llm = ChatOpenAI(
            openai_api_key=settings.openrouter_api_key or os.getenv("OPENROUTER_API_KEY", "dummy"),
            openai_api_base=settings.openrouter_base_url,
            model_name=settings.openrouter_model_name,
            temperature=0, # Low temperature for more factual, document-based answers
            max_tokens=1000,
        )
        self._init_qa_chain()
        
    def _init_qa_chain(self):
        """Initializes the standard LangChain QA chain."""
        retriever = self.vector_store_manager.as_retriever(search_kwargs={"k": 6})
        
        # 1. Create a chain that combine retrieved chunks and sends them to the LLM
        combine_docs_chain = create_stuff_documents_chain(self.llm, QA_PROMPT)
        
        # 2. Add retrieval step to automatically feed relevant documents to the prompt
        self.qa_chain = create_retrieval_chain(retriever, combine_docs_chain)
        logger.info("Initialized RAG QA Chain with ChatOpenAI.")
        
    def ask_question(self, question: str) -> dict:
        """
        Processes a user question, retrieves relevant documents, and generates an answer.
        Returns both the final answer and the source contexts.
        """
        logger.info(f"QAService processing query: '{question}'")
        try:
            response = self.qa_chain.invoke({"input": question})
            
            # Extract source documents for citations
            sources = []
            for doc in response.get("context", []):
                source = doc.metadata.get("source", "Unknown")
                page = doc.metadata.get("page", "N/A")
                content_snippet = doc.page_content[:150] + "..."
                sources.append({
                    "source": source,
                    "page": page,
                    "snippet": content_snippet
                })
                
            logger.info("Query successfully answered by RAG chain.")
            
            return {
                "answer": response.get("answer", "No answer found."),
                "sources": sources
            }
        except Exception as e:
            logger.error(f"QAService encountered an error: {str(e)}")
            return {
                "answer": "An error occurred while attempting to generate an answer.",
                "sources": [],
                "error": str(e)
            }
