FROM python:3.8.10

WORKDIR /app

# Install application server
RUN pip install uwsgi==2.0.20

# Copy and install requirements
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copy codebase into container
COPY . .

# Collect static
RUN ./manage.py collectstatic

# Ops Parameters
ENV WORKERS=1
ENV PORT=8000
ENV PYTHONUNBUFFERED=1

CMD uwsgi --http :${PORT} --processes ${WORKERS} --static-map /static=/static --module pixax.wsgi:application
