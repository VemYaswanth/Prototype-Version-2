FROM python:3.10

# Set work directory
WORKDIR /app

# Copy the entire folder into the container
COPY . /app

# Install dependencies only if requirements.txt exists
RUN if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

# Run the generator
CMD ["python", "auto_data_generator.py"]
