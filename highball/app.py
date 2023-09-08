import streamlit as st
import openai
import os
# OpenAI API 키 설정 (실제 키로 교체해야 함)
#api_key = "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"

# OpenAI API 키 설정
openai.api_key = os.getenv("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")

# Streamlit 앱 설정
st.title("GPT-3.5 Turbo 챗봇")

# 사용자 입력 받기
user_input = st.text_input("당신의 질문을 입력하세요:")

if user_input:
    # GPT-3.5 Turbo 모델에게 질문 전송
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "너는 그날에 기분따라 하이볼을 추천해주는 하이볼 추천 봇이야. 너는 상대방과 대화 이후 하이볼 메뉴이름을 말해주고 그에 관련된 레시피를 알려줘야해 질문자는 레몬,산토리위스키, 진저에일만 가지고있어 그에따라 추천을해줘 "
            },
            {
                "role": "assistant",
                "content": "안녕, 나는 AI 하이볼 머신이야."
            },
            {
                "role": "user",
                "content": user_input
            }
        ],
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # 모델의 응답 출력
    st.write(response['choices'][0]['message']['content'])
