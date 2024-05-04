from openai import OpenAI
import streamlit as st

import instructor
from pydantic import BaseModel

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="123",
)

# # Enables `response_model`
# client = instructor.patch(client=client)


# class UserDetail(BaseModel):
#     name: str
#     age: int
#     job: str


if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {
            "role": "system",
            "content": """You are a helpful assistant. If you do not know the answer, reply I don't know 
                don't make things up.""",
        }
    ]

st.title("Ibrahim Image processing ")
for message in st.session_state.messages:
    st.chat_message(message["role"]).markdown(message["content"])

prompt = st.chat_input("Pass your input here")
image_input = st.text_input("Image URL")
if prompt:
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = client.chat.completions.create(
        max_tokens=-1,
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": image_input
                    },
                    {"type": "text", "text": prompt},
                ],
            }
        ],
        stream=True,
    )

    with st.chat_message("ai"):
        completed_message = ""
        message = st.empty()
        # Streaming the response out
        for chunk in response:
            # If the value is not none print it out
            if chunk.choices[0].delta.content is not None:
                completed_message += chunk.choices[0].delta.content
                message.markdown(completed_message)
            # print(chunk.choices[0].delta.content, flush=True, end="")

    st.session_state.messages.append(
        {"role": "assistant", "content": completed_message}
    )
