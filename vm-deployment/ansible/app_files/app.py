from flask import Flask, request
from prometheus_client import start_http_server, Counter, Histogram
import time
import random
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('dummy_app')
logger.info(f"Python version: {sys.version}")
logger.info(f"Starting application...")

# Create app for monitoring demonstration
app = Flask(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter('request_count', 'Total number of requests', ['endpoint', 'method'])
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request latency in seconds', ['endpoint'])
ERROR_COUNT = Counter('error_count', 'Number of errors', ['endpoint', 'status_code'])

@app.before_request
def before_request():
    request.start_time = time.time()
    logger.debug(f"Request started: {request.method} {request.path}")

@app.after_request
def after_request(response):
    endpoint = request.path
    method = request.method
    
    # Record request count
    REQUEST_COUNT.labels(endpoint=endpoint, method=method).inc()
    
    # Record latency
    latency = time.time() - request.start_time
    REQUEST_LATENCY.labels(endpoint=endpoint).observe(latency)
    
    logger.debug(f"Request completed: {method} {endpoint} - Status: {response.status_code} - Latency: {latency:.4f}s")
    
    return response

@app.route('/')
def home():
    return 'Welcome to the Dummy App!'

@app.route('/api/data')
def get_data():
    # Simulate some processing time
    time.sleep(random.uniform(0.1, 0.5))
    
    # Simulate errors occasionally
    if random.random() < 0.1:  # 10% chance of error
        ERROR_COUNT.labels(endpoint='/api/data', status_code=500).inc()
        return 'Internal Server Error', 500
    
    return {
        'data': 'Sample data',
        'timestamp': time.time()
    }

if __name__ == '__main__':
    # Start Prometheus metrics server
    logger.info("Starting Prometheus metrics server on port 8000")
    start_http_server(8000)
    
    # Start Flask app
    logger.info("Starting Flask app on port 5000")
    app.run(host='0.0.0.0', port=5000)
