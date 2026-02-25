import sys
import os

# Add the project root to sys.path to resolve 'src' modules when running via `streamlit run`
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import streamlit as st
from src.services.qa import QAService
from src.services.ingestion import IngestionService

st.set_page_config(page_title="Document Retrieval", layout="wide")

st.title("📚 LangChain Document Retrieval System")

# Initialize services
@st.cache_resource
def get_qa_service(api_key):
    if not api_key and not os.getenv("OPENROUTER_API_KEY"):
        return None
    return QAService()

@st.cache_resource
def get_ingestion_service(api_key):
    if not api_key and not os.getenv("OPENROUTER_API_KEY"):
        return None
    return IngestionService()

# (Services will be initialized below after key is captured)

# Sidebar for settings and ingestion
with st.sidebar:
    st.header("⚙️ Settings")
    
    api_key = st.text_input("OpenRouter API Key", type="password", value=os.getenv("OPENROUTER_API_KEY", ""))
    if api_key:
        os.environ["OPENROUTER_API_KEY"] = api_key
        
    qa_service = get_qa_service(api_key)
    ingestion_service = get_ingestion_service(api_key)
            
    st.divider()
    
    st.header("Upload Documents")
    uploaded_files = st.file_uploader("Choose files", accept_multiple_files=True, type=['pdf', 'txt', 'md', 'docx'])
    
    if st.button("Ingest Documents"):
        if not uploaded_files:
            st.warning("Please upload at least one file.")
        else:
            with st.spinner("Ingesting documents..."):
                # Save uploaded files temporarily
                temp_dir = "./data/documents"
                os.makedirs(temp_dir, exist_ok=True)
                
                for file in uploaded_files:
                    path = os.path.join(temp_dir, file.name)
                    with open(path, "wb") as f:
                        f.write(file.getbuffer())
                
                # Ingest
                result = ingestion_service.ingest_directory(temp_dir)
                st.success(f"Successfully processed {result['chunks_added']} chunks from {len(uploaded_files)} files!")

# Main chat interface
if not api_key:
    st.info("Please enter your OpenRouter API key in the sidebar to start asking questions.")
else:
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("Ask a question about your documents:"):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = qa_service.ask_question(prompt)
                    answer = response["answer"]
                    sources = response.get("sources", [])
                    
                    st.markdown(answer)
                    
                    if sources:
                        with st.expander("View Sources"):
                            for idx, source in enumerate(sources):
                                st.markdown(f"**Source {idx + 1}:** {source['source']} (Page: {source.get('page', 'N/A')})")
                                st.markdown(f"> {source['snippet']}")
                                
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                except Exception as e:
                    st.error(f"Error generating answer: {str(e)}")
                    
