
# Usage:
#  make build: build docker image.
#  make run channel=<channel_id>: run docker image with channel id.

channel=

usage:
	@echo "Usage:"
	@echo " make build: build docker image."
	@echo " make run channel=<channel_id>: run docker image with channel id."

build:
	docker build -t import_youtube_data_to_algolia .

run:
	docker run --rm import_youtube_data_to_algolia $(channel)

clean:
	docker image rm import_youtube_data_to_algolia
