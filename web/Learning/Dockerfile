FROM bitnami/python

WORKDIR /app

COPY flag.txt .
COPY requirements.txt .

RUN pip install gunicorn
RUN pip install -r requirements.txt

# Copy challenges files at last to avoid update and install requirements on each modification
COPY ./app .

EXPOSE 8000
# CMD ["python3", "app.py"]
CMD ["gunicorn", "--workers=4", "--bind", "0.0.0.0:8000", "app:app"]
