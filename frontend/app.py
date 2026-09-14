import streamlit as st

from api_client import query_backend

st.set_page_config(page_title="Drug Leaflet Assistant", page_icon="💊")
st.title("💊 Drug Leaflet Assistant")
st.caption("Ask questions about drug dosage, warnings, interactions, and more — answers are grounded in official package inserts.")

# Keep chat history across reruns using Streamlit's session state.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render past messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if message.get("sources"):
            with st.expander("Sources"):
                for source in message["sources"]:
                    drug = source["drug"].replace("_", " ").title()
                    section = source["section"].title()
                    st.markdown(f"- **{drug}** — {section}")

# Chat input
question = st.chat_input("Ask a question about a drug...")

if question:
    # Show the user's question immediately
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    # Get and show the assistant's answer
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                result = query_backend(question)
                answer = result["answer"]
                sources = result["sources"]

                st.markdown(answer)
                if sources:
                    with st.expander("Sources"):
                        for source in sources:
                            drug = source["drug"].replace("_", " ").title()
                            section = source["section"].title()
                            st.markdown(f"- **{drug}** — {section}")

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources,
                })

            except Exception as e:
                error_msg = "Sorry, something went wrong reaching the assistant. Please make sure the backend server is running and try again."
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg, "sources": []})