#!/bin/bash

# log flood scenario for SRE machine test.
# 2000 requests to the application health endpoint.

REQUESTS="${1:-2000}"

echo "Starting controlled log flood: $REQUESTS requests"

for ((i=1; i<=REQUESTS; i++)); do
    curl -s \
      -H "Host: sre-app.local" \
      http://localhost/health > /dev/null

    if (( i % 500 == 0 )); then
        echo "$i requests completed"
    fi
done

echo "Log flood completed."
