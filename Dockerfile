FROM python:3.9

COPY requirements.txt requirements.txt
COPY streamlit_app.py streamlit_app.py

RUN pip install -r requirements.txt
EXPOSE 80 8080
CMD ["streamlit", "run", "streamlit_app.py", "--server.port", "80"]