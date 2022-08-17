#!/bin/bash

jinja2 seurch/config/config.yml.j2 seurch/config/config.docker.yml > seurch/config/config.yml
aws --endpoint-url=http://localstack:4566 s3api create-bucket --bucket seurch-uat --profile local
aws --endpoint-url=http://localstack:4566 s3api create-bucket --bucket link-ingestion --profile local
# python3 seurch/seeds/seeds.py
python3 -m debugpy --listen 0.0.0.0:5678 -m flask run -h 0.0.0.0 -p 5001
