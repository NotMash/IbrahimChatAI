import time

from openai import OpenAI
import streamlit as st


# display_question(questions[0][0], 0)
questions = [
    ("Good morning, are you well today?", "well_today"),
    ("Would you like a cup of tea?", "cup_of_tea"),
    ("Are you feeling hungry?", "feeling_hungry"),
    ("Do you need to access the restroom?", "access_restroom"),
    ("Are you comfortable with the seating arrangement?", "comfortable_seating"),
    ("Do you need assistance with technology or devices?", "tech_assistance"),
    ("Do you need help with any household tasks?", "household_tasks"),
    ("How are you feeling today?", "feeling_today"),
    ("Would you like to go outside?", "go_outside"),
    ("Would you like to play games?", "play_games"),
    ("Do you need assistance with mobility?", "mobility_assistance"),
    ("Would you like to rest for a while?", "rest_for_while"),
    ("Should I play some music?", "play_music"),
    ("Would you like me to adjust the sound levels for you?", "adjust_sound_levels"),
    ("Would you like me to adjust the lighting?", "adjust_lighting"),
    ("Are you thirsty?", "thirsty"),
    ("All questions answered. Processing responses", "")
]



client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="123",
)
def displayButtons(index):
    if st.session_state.responses[index] is None:
        col1, col2 = st.columns(2)

        with col1:
            st.empty()
            st.button('NO', on_click=lambda index=index: handle_response(index, False),
                                  key=f'no_button_{index}')
            # print("from display buttons", index)
        with col2:
            st.empty()
            st.button('YES', on_click=lambda index=index: handle_response(index, True),
                                   key=f'yes_button_{index}')

            # print("from display buttons", index)

def handle_response(index, response):

    st.session_state.responses[index] = response
    if index < len(questions):
        print("handling button clicked add to index", index)

        st.session_state.messages.append({"role": "assistant", "content": questions[index][0]})
    else:
        st.session_state.messages.append({"role": "assistant", "content": "All questions answered. Processing responses..."})
def process_responses():
    st.write("All questions answered. Processing responses...")

def main():
    st.title("MindStorm AI Chat")
    # Initialize session state to keep track of user responses
    if 'responses' not in st.session_state:
        st.session_state.responses = [None] * (1+len(questions))
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {
                "role": "system",
                "content": """You are a helpful assistant. If you do not know the answer, reply I don't know 
                    don't make things up.""",
            }

        ]
        st.session_state.messages.append({"role": "assistant", "content": questions[0][0]})

    count = 1

    for message in st.session_state.messages[1:]:
        # st.chat_message("MINDSTORM").markdown("HERERERE RERERE")
        st.chat_message(message["role"]).markdown(message["content"])
        if count < len(questions):
            # print("count iss", count)
            # print("question is ", questions[count][0])
            displayButtons(count)
            count += 1


    questionsDone()

    but = st.button("save")

    if but:
        st.write(st.session_state.messages)


# buttons for response
button_styles = """
    <style>
      
    .stButton > button {
        margin: 0 5px !important; /* Adjust margin to bring buttons closer together */
        padding: 0 50px !important; /* Adjust padding to make buttons smaller */
    }
    </style>
"""
st.markdown(button_styles, unsafe_allow_html=True)

def questionsDone():
    prompt = st.chat_input("Pass your input here")

    if prompt:
        st.chat_message("user").markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        response = client.chat.completions.create(
            model="llama.cpp/models/mistral-7b-instruct-v0.1.Q4_0.gguf",
            messages=st.session_state.messages,
            stream=True,
        )

        complete_response = ""
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    complete_response += chunk.choices[0].delta.content
                    message_placeholder.markdown(complete_response + "▌")
                    message_placeholder.markdown(complete_response)
        st.session_state.messages.append(
            {"role": "assistant", "content": complete_response}
        )


if __name__ == "__main__":
    main()