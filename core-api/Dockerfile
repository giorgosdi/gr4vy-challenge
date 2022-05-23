FROM python:3.9-bullseye
RUN curl -SsL https://packages.httpie.io/deb/KEY.gpg | apt-key add - && curl -SsL -o /etc/apt/sources.list.d/httpie.list https://packages.httpie.io/deb/httpie.list && apt update && apt install httpie -y
COPY . .
RUN pip install -r requirements.txt
ARG port secret redis
ENV HTTP_PORT=$port JWT_SECRET=$secret REDIS_URL=$redis
EXPOSE 5002
ENTRYPOINT ["python", "main.py"]
