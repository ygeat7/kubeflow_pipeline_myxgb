FROM python:3.8
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY . /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN mkdir model
ENTRYPOINT ["python", "test_eval.py"]
