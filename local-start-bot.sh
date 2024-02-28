#!/bin/sh

wait_database()
{
  HOST=$1
  PORT=$2

  echo "Waiting for database..."
  echo "$HOST"
  echo "$PORT"
  while ! nc -z "$HOST" "$PORT"; do
    sleep 0.1
  done

  echo "database started"
}

wait_database "$PG_HOST" "$PG_PORT"

make local-migration-up
python ./run_bot.py .env