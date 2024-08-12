FROM python:3.11

WORKDIR /flask_app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1

# Expose the port the app runs on
EXPOSE 5000

# Command to run the application
CMD [ "gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "app:app" ]

