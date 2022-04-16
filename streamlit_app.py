from PIL import Image

import streamlit as st
import requests
import json

def load_image(image_file):
	img = Image.open(image_file)
	return img

def validte_json_content(value: str, target:str):
    try:
        value = json.loads(value)
    except:
        st.error(f'check {target} value!')

    return value

st.title("AI service Laboratory")

with st.sidebar:
    category = st.selectbox(
        "Select Service Type",
        (
            "OCR",
            "Translation",
            "Speech-To-Text",
            "Conversation",
            "NLP",
            "Image Task Template",
            "Text Task Template",
        ),
    )

st.subheader(f"Service Type: {category}")

if "Template" in category:  # use user input
    request_host = st.text_input("request host")
    request_port = st.number_input("request port", format='%d', step=1)
    request_header = st.text_area("request header(json format)")
else:  # read config from yaml
    request_host = ""
    request_port = 8080
    request_header = {}

if category == "Image Task Template" or category == "OCR":
    image_file = st.file_uploader("Upload Images", type=["png", "jpg", "jpeg"])
    if image_file is not None:
        file_details = {
            "filename": image_file.name,
            "filetype": image_file.type,
            "filesize": image_file.size,
        }
        st.write(file_details)
        loaded_image = load_image(image_file)

        col1, col2, col3 = st.columns([1,1,1])
        with col1:
            if st.button('rotate 90'):
                loaded_image = loaded_image.rotate(-90)
        with col2:
            if st.button('rotate 180'):
                loaded_image = loaded_image.rotate(-180)
        with col3:
            if st.button('rotate 270'):
                loaded_image = loaded_image.rotate(-270)
        
        st.image(loaded_image, width=640)

request_body = st.text_area("request body(json format)")

if st.button("predict"):
    request_header = validte_json_content(request_header, 'request_header')
    request_body = validte_json_content(request_body, 'request_body')

    if request_header and request_body:
        response = requests.post(
            f"{request_host}:{request_port}",
            request_header=request_header,
            data=request_body,
        )
