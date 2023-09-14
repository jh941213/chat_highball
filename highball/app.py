import openai
import streamlit as st
from streamlit_chat import message
import base64
import serial

# Raspberry Pi Pico와 연결
#ser = serial.Serial('/dev/cu.usbmodem1301', 9600)



def extract_recipe_and_message(output):
    recipe_start = output.find("재료:")
    message_start = output.find("오늘의 메시지:")
    
    if recipe_start != -1 and message_start != -1:
        recipe = output[recipe_start:message_start].strip()
        message = output[message_start:].strip()
        print("------------")
        print(recipe)
        print("------------")
        print(message)
        print("------------")
        return recipe, message
    else:
        return None, None


# API 키는 외부에 노출되지 않도록 조심하세요
openai.api_key = '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'

def generate_response(user_input, past_conversations):
    conversation = [
        {
            "role": "system",
            "content": "너는 그날에 기분따라 하이볼을 추천해주는 하이볼 추천 봇이야. 너는 상대방에게 기분을 물어보고, 하이볼 레시피를 알려주고 반드시 정량ml를 기입해서 위스키양과 재료의 양을 꼭 출력시켜주고 그사람에게 희망의 메시지까지 따로 출력해줘"
        },
        {
            "role": "system",
            "content": "너는 상대방에게 기분을 물어보고 오늘 하루에 대해 물어봐줘"
        },
        {
            "role": "system",
            "content": "자연스러운 대화를 2~3회 이어서 해주고 하이볼을 추천해드릴까요 물어봐줘"
        },
        {
            "role": "system",
            "content": "상대방이 응답을 하면, 그날의 기분에 맞는 하이볼 레시피를 출력해줘 그날의 하이볼이름과 꼭 정량대로ml 표시해서, 반드시 '재료:'하고 재료들을 추출해줘. 하이볼의 위스키는 상대방이 입력한 위스키나, 너가아는 위스키를 토대로 만들어줘"
        },
        {
            "role": "system",
            "content": "레시피를 출력한 이후, 그사람에게 오늘의메시지로 그 기분에 맞는 한마디를 출력해줘"
        },
        {
            "role": "system",
            "content": "반드시 결과를 출력할때 재료: 하고 출력하고 오늘의메시지: 하고 출력해줘야해"
        },
    ]
    
    conversation.extend(past_conversations)
    
    conversation.append(
        {
            "role": "user",
            "content": user_input
        }
    )
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        temperature=0.1,
        max_tokens=512,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    message = response['choices'][0]['message']['content']
    return message

def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
    
st.header("🥂백종원이 추천해주는 오늘의 하이볼")
st.markdown("[My blogl](https://velog.io/@jh1213)")

if 'conversations' not in st.session_state:
    st.session_state['conversations'] = []

with st.form('form', clear_on_submit=True):
    user_input = st.text_input('You: ', '', key='input')
    submitted = st.form_submit_button('Send')

if submitted and user_input:
    output = generate_response(user_input, st.session_state['conversations'])
    new_message = {
        "role": "user",
        "content": user_input
    }
    st.session_state.conversations.append(new_message)
    
    new_message = {
        "role": "assistant",
        "content": output
    }
    st.session_state.conversations.append(new_message)

    recipe, message = extract_recipe_and_message(output)
    
    if recipe and message:
        print(recipe)
        send_to_pico(recipe)
        print(message)
        send_to_pico(message)

if st.session_state['conversations']:
    for message in st.session_state['conversations']:
        if message['role'] == 'user':
            image_base64 = get_image_base64("/Users/jaehyun/Desktop/09_ccc/hol.png")
            flex_direction = "row-reverse"
            text_margin = "margin-right: 10px;"
        else:
            image_base64 = get_image_base64("/Users/jaehyun/Desktop/09_ccc/Baek.jpeg")
            flex_direction = "row"
            text_margin = "margin-left: 10px;"
        
        st.markdown(f'''
        <div style="display: flex; align-items: center; flex-direction: {flex_direction}; padding: 10px; margin: 5px;">
            <img src="data:image/png;base64,{image_base64}" style="width: 60px; height: 60px; border-radius: 30%;">
            <div style="font-size: 16px; color: #ffffff; background-color: #4a4a4a; padding: 5px; border-radius: 10px; {text_margin}">{message["content"]}</div>
        </div>
        ''', unsafe_allow_html=True)

