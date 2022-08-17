# Fetch python slim image
FROM python:3.10.4-slim AS base

# Install necessary packages
RUN apt-get update \
    && apt-get install git -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*


# ENV VARS
ENV FLASK_APP=seurch/app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV PYTHONPATH=/app
ENV FLASK_RUN_PORT 5001

# Expose Flask port
EXPOSE 5001

# Specify the working directory within the container
WORKDIR /app

# Copy all the necessary files and folders to /app
COPY . /app

# Install packages
RUN pip3 install -r requirements.txt

# Initialise git otherwise the app won't start because of the status endpoint
RUN git config --global user.email "dev@insg.ai" \
    && git config --global user.name "Dev" \
    && cd /app \
    && git init \
    && git add setup.py \
    && git commit -m 'Inital commit'

# Generate the config file
RUN jinja2 seurch/config/config.yml.j2 seurch/config/config.docker.yml > seurch/config/config.yml

# Local debugging
FROM base AS debug
# Get debugpy
RUN pip3 install debugpy
# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# "Prod" image
FROM base AS production
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
