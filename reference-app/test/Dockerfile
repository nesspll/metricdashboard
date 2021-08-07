FROM python:3.7-slim

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./
EXPOSE 8080
# Install production dependencies.

RUN apt-get update && \
    pip install --upgrade pip && \
    pip install prometheus_flask_exporter && \
    pip install -r requirements.txt

CMD [ "uwsgi", "--socket", "0.0.0.0:8080", \
               "--uid", "uwsgi", \
               "--plugins", "python", \
               "--protocol", "uwsgi", \
               "--wsgi", "main:app" ]