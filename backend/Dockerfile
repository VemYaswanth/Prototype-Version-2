FROM python:3.11-slim

WORKDIR /app

# Copy backend code
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["sh", "-c", "python init_db.py && gunicorn run:app -c gunicorn.conf.py"]

RUN python -c "from sqlalchemy import create_engine; engine=create_engine('postgresql+psycopg2://postgres:postgres@db:5432/securitydb'); engine.execute('CREATE TABLE IF NOT EXISTS test(id SERIAL PRIMARY KEY);')" || true
