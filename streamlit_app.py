from PIL import Image

import streamlit as st
import requests

def load_image(image_file):
	img = Image.open(image_file)
	return img

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
request_body = st.text_area("request body(json format)")

if "Template" in category:  # use user input
    request_host = st.text_input("request host")
    request_port = st.number_input("request port")
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
        st.image(load_image(image_file), width=250)

elif category == "Text Task Template":
    st.text_area(label="text query")

if st.button("predict"):
    response = requests.post(
        f"{request_host}:{request_port}",
        request_header=request_header,
        data=request_body,
    )
