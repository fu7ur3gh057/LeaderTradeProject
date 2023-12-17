#!/bin/sh

# Until server folder created
until cd /app/server; do
  echo "Waiting for server volume..."
done

echo "Start LeaderTrade Scheduler"
# run a worker and beat
celery -A core worker --beat --scheduler django --loglevel=info
exec "$@"