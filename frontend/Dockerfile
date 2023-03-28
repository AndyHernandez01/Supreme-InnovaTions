FROM python:3.9-slim

WORKDIR /app/

COPY /app/requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt

EXPOSE 8501

COPY . /app

ENTRYPOINT ["streamlit", "run"]
CMD["./app/strlit.py"]
