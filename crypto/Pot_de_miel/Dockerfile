FROM bitnami/python

WORKDIR /app
COPY server.py .
COPY flag.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 50001
CMD ["python3", "/app/server.py"]
