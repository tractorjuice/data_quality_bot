#Importing required packages
import streamlit as st
import openai

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
#MODEL = "gpt-3"
#MODEL = "gpt-3.5-turbo"
#MODEL = "gpt-3.5-turbo-0613"
#MODEL = "gpt-3.5-turbo-16k"
#MODEL = "gpt-3.5-turbo-16k-0613"
#MODEL = "gpt-4"
MODEL = "gpt-4-0613"
#MODEL = "gpt-4-32k-0613"

st.set_page_config(page_title="Data Quality Bot")
st.sidebar.title("Learn about Data Quality")
st.sidebar.divider()
st.sidebar.markdown("Developed by Mark Craddock](https://twitter.com/mcraddock)", unsafe_allow_html=True)
st.sidebar.markdown("Current Version: 0.2.0")
st.sidebar.markdown("Using GPT-4 API")
st.sidebar.divider()

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = MODEL

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
            "role": "system",
            "content": f"""
             Interact with Data Quality Bot, your personal guide to learning and creating a strategy for data quality.
             Learn about data quality for strategic planning and decision-making by choosing to 'Learn' about data quality, or 'Vocabulary' and I will provide a list of common terms and their definitions. or 'Create' your own data quality strategy with step-by-step guidance.
             If you need assistance, type 'Help' for support. Begin your data quality journey now!
             """
        })
    st.session_state.messages.append(   
        {
            "role": "user",
            "content": "Help?"
        })
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": """
            I'm here to help you learn about data quality. Here are some options for getting started:
            1. Learn: To learn about the components and concepts of a data quality, type "Learn".
            2. Vocabulary: To get a list of common quality terms and their definitions, type "Vocabulary".
            3. Create: To create your own data quality strategy with step-by-step guidance, type "Create".
            If you have any specific questions or need clarification on any aspect of data quality, feel free to ask.
            """
        })

for message in st.session_state.messages:
    if message["role"] in ["user", "assistant"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
