FROM bitnami/python

WORKDIR /app

COPY flag.txt .
COPY requirements.txt .

# Packages
RUN apt update
RUN apt install -y cron
RUN pip install -r requirements.txt
RUN pip install gunicorn

# Cron job
COPY clear_notes.sh .
COPY clearnotes-cron /etc/cron.d/clearnotes-cron
RUN chmod 0644 /etc/cron.d/clearnotes-cron
RUN crontab /etc/cron.d/clearnotes-cron
RUN touch /var/log/cron.log

# Copy challenges files at last to avoid update and install requirements on each modification
COPY ./app .

EXPOSE 8000
# CMD cron && python3 app.py
CMD cron && gunicorn --workers=4 --bind 0.0.0.0:8000 'app:app'