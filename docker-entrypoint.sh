#!/usr/bin/env sh
# docker-entrypoint.sh – initialise the database then start the Flask server
set -e

echo "Initialising database…"
python - <<'EOF'
import sys
sys.path.insert(0, "")
from backend.server import init_db
init_db()
print("Database ready.")
EOF

echo "Starting Face-Recon backend on 0.0.0.0:5000…"
exec python -m flask --app backend.server run --host=0.0.0.0 --port=5000
