FROM bitnami/python

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

EXPOSE 50002
CMD ["python3", "/app/server.py"]
