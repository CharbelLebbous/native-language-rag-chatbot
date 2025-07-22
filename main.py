# main.py

# ✅ Streamlit for the simple web UI
import streamlit as st

# ✅ Your local modules for indexing and querying
from ingestion import build_index
from query_engine import query_index

# ✅ Page title
st.title("📚 Native Language Q&A - RAG++ with Summaries & Entities, with Chat Memory")

# ✅ Initialize session state for index build flag
if "index_built" not in st.session_state:
    st.session_state.index_built = False

# ✅ Initialize session state for storing conversation history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ✅ User input for the folder containing documents
folder_path = st.text_input("Enter folder path with documents:")

# ✅ If user clicks Build Index button, run indexing pipeline
if st.button("Build Index"):
    if folder_path:
        build_index(folder_path)
        st.session_state.index_built = True
        st.success("✅ Index built successfully.")
    else:
        st.warning("Please enter a valid folder path.")

# ✅ If index is built, allow the user to ask questions
if st.session_state.index_built:
    question = st.text_input("Ask your question:")

    # ✅ If user clicks Get Answer and has typed a question
    if st.button("Get Answer") and question:
        # Call the query function with the question and chat history
        answer, sources = query_index(
            question,
            chat_history=st.session_state.chat_history
        )

        # ✅ Save this turn (question + answer) in session history
        st.session_state.chat_history.append({"role": "user", "content": question})
        st.session_state.chat_history.append({"role": "assistant", "content": answer})

        # ✅ Display the answer
        st.markdown("### Answer")
        st.write(answer)

        # ✅ Display source metadata for transparency
        st.markdown("---")
        st.markdown("### Retrieved Context Metadata")
        if sources:
            for src in sources:
                st.write(f"- 📄 File: {src['file_name']}")
                st.write(f"  📂 Folder: {src['folder_name']}")
                st.write(f"  🛣️ Path: {src['folder_path']}")
                st.write(f"  📑 Page: {src['page_number']}")
                st.write(f"  📝 Summary: {src['summary'][:200]}...")
                st.write(f"  🔍 Entities: {src['entities']}")
                st.write("---")
        else:
            st.write("No metadata available for retrieved context.")
