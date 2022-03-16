FROM python:3-alpine
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY import_youtube_data_to_algolia.py /app
COPY .env /app
ENTRYPOINT [ "python", "import_youtube_data_to_algolia.py" ]
