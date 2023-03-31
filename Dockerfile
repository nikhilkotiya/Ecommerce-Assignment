From python:3.8-slim-buster
ENV PYHTONUNBUFFERED=1
WORKDIR /django
COPY requirements.txt requirements.txt 
RUN pip install -r requirements.txt
# CMD ["python3","manage.py","runserver","0.0.0.0:8000"]