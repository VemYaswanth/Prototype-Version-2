FROM python:3.11-slim

WORKDIR /app

# Copy backend code
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install docker


EXPOSE 8000

CMD ["sh", "-c", "python init_db.py && gunicorn run:app -c gunicorn.conf.py"]