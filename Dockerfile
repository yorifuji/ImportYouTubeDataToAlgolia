FROM python:3-alpine
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY app.py /app
COPY .env /app
ENTRYPOINT [ "python", "app.py" ]
