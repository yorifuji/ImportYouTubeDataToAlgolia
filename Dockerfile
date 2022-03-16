FROM python:3-alpine
WORKDIR /app
COPY import_youtube_data_to_algolia.py .env requirements.txt /app
RUN pip install -r requirements.txt
ENTRYPOINT [ "python", "import_youtube_data_to_algolia.py" ]
