import streamlit as st
import os
from datetime import datetime
import openai

def ask_gpt(prompt,model,apikey):
    client = openai.OpenAI(api_key=apikey)
    response = client.chat.completions.create(model=model,messages=prompt)
    system_message = response.choices[0].message.content
    return system_message

def main():
    st.set_page_config(
        page_title="채팅 봇 프로그램",
        layout="wide"
    )
    st.header("채팅 봇 프로그램")
    st.markdown("---")
    
    flag_start = False

    if "chat" not in st.session_state:
        st.session_state["chat"] = []
    if "OPENAI_API" not in st.session_state:
        st.session_state["OPENAI_API"] = ""
    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role":"system","content":"You are a thoughtful assistant.Respond to all input in 25 words and answer in korea"}]
    if "check_reset" not in st.session_state:
        st.session_state["check_reset"] = False

    with st.expander("채팅 봇 프로그램에 관하여",expanded=True):
        st.write(
            """
            -채팅 봇 프로그램의 UI는 스트림릿을 활용했습니다. \n
            -STT(Speech-To-Text)는 OpenAI의 Whisper AI를 활용했습니다.\n
            -답변은 OpenAI의 GPT모델을 활용했습니다.\n
            -TTS(Text-To-Speech)는 구글의 Google Translate TTS를 활용했습니다.
            """
        )
        st.markdown("")
    with st.sidebar:
        st.session_state["OPENAI_API"] = st.text_input(label="OPENAI API 키",placeholder="Enter your API Key",value="",type="password")
        st.markdown("---")
        model = st.radio(label="GPT모델",options=["gpt-4","gpt-3.5-turbo"])
        st.markdown("---")
        if st.button(label="초기화"):
            st.session_state["chat"] = []
            st.session_state["messages"] = [{"role":"system","content":"You are a thoughtful assistant.Respond to all input in 25 words and answer in korea"}]
            st.session_state["check_reset"] = True
            
    col1,col2 = st.columns(2)
    with col1:
        st.header("질문하기")
        text = st.text_input(label="텍스트 입력 창",placeholder="텍스트를 입력해주세요")
        
        question = text
        now = datetime.now().strftime("%H:%M")
        st.session_state["chat"] = st.session_state["chat"]+[("user",now,question)]
        st.session_state["messages"] = st.session_state["messages"] + [{"role":"user","content":question}]
        st.session_state["check_reset"] = False
        if st.button("텍스트 입력 후 클릭"):
            flag_start =True
    with col2:
        st.header("질문/답변")
        if flag_start :
            response = ask_gpt(st.session_state["messages"],model,st.session_state["OPENAI_API"])
            st.session_state["messages"] = st.session_state["messages"] + [{"role":"system","content":response}]
            now = datetime.now().strftime("%H:%M")
            st.session_state["chat"] = st.session_state["chat"] + [("bot",now,response)]

            for sender, time, message in st.session_state["chat"]:

                if sender == "user":

                    st.write(f'<div style="display:flex;align-items:center;"><div style="background-color:#007AFF;color:white;border-radius:12px;padding:8px 12px;margin-right:8px;">{message}</div><div style="font-size:0.8rem;color:gray;">{time}</div></div>', unsafe_allow_html=True)

                    st.write("")

                else:

                    st.write(f'<div style="display:flex;align-items:center;justify-content:flex-end;"><div style="background-color:lightgray;border-radius:12px;padding:8px 12px;margin-left:8px;">{message}</div><div style="font-size:0.8rem;color:gray;">{time}</div></div>', unsafe_allow_html=True)

                    st.write("")
if __name__ =="__main__":
    main()
