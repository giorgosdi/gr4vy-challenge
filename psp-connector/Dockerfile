FROM python:3.9-bullseye
COPY . .
RUN pip install -r requirements.txt
ARG port redi_url
ENV HTTP_PORT=$port REDIS_URL=$redis_url
EXPOSE 5003
ENTRYPOINT ["python", "main.py"]
