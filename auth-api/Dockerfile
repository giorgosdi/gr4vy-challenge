FROM python:3.9-bullseye
COPY . .
RUN pip install -r requirements.txt
ARG port secret
ENV HTTP_PORT=$port JWT_SECRET=$secret
EXPOSE 5001
ENTRYPOINT ["python", "main.py"]
