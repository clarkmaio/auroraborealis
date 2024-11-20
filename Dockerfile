FROM python:3.10-slim

COPY . /app/
WORKDIR /app

RUN pip install -r requirements.txt

# export pythonpath
ENV PYTHONPATH=/app

EXPOSE 8001

# Start dashboard
CMD ["panel", "serve", "src/dashboard/start.py", "--address", "0.0.0.0","--port", "8001", "--allow-websocket-origin", "*"]