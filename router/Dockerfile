FROM python:3.9-bullseye
COPY . .
RUN pip install -r requirements.txt
ARG port
ENV HTTP_PORT=$port
EXPOSE 5000
ENTRYPOINT ["python", "main.py"]
