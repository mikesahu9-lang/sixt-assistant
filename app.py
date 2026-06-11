import streamlit as st
from rag_core import ask_sixt_assistant

st.title("Sixt Rental Assistant")
st.caption("Answers based on Sixt documentation")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about Sixt rentals..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        answer, sources = ask_sixt_assistant(prompt)
        st.markdown(answer)
        with st.expander("Sources used"):
            for s in sources:
                st.caption(s)

    st.session_state.messages.append({"role": "assistant", "content": answer})
