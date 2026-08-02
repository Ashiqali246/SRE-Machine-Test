from flask import Flask, jsonify, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time
import os

app = Flask(__name__)

REQUEST_COUNT = Counter(
    "sre_app_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint"]
)

REQUEST_LATENCY = Histogram(
    "sre_app_request_latency_seconds",
    "HTTP request latency",
    ["endpoint"]
)

@app.route("/")
def home():
    start = time.time()

    REQUEST_COUNT.labels(method="GET", endpoint="/").inc()

    response = {
        "application": "SRE Evaluation Microservice",
        "status": "running",
        "version": os.getenv("APP_VERSION", "1.0.0")
    }

    REQUEST_LATENCY.labels(endpoint="/").observe(time.time() - start)

    return jsonify(response)


@app.route("/health")
def health():
    REQUEST_COUNT.labels(method="GET", endpoint="/health").inc()

    return jsonify({
        "status": "healthy"
    }), 200


@app.route("/ready")
def ready():
    REQUEST_COUNT.labels(method="GET", endpoint="/ready").inc()

    return jsonify({
        "status": "ready"
    }), 200


@app.route("/metrics")
def metrics():
    return Response(
        generate_latest(),
        mimetype=CONTENT_TYPE_LATEST
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000
    )
