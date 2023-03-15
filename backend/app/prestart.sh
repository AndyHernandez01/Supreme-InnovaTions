#! /usr/bin/env bash

# Let the DB start
python /app/app/backend_pre_start.py

# Run migrations
alembic upgrade head

# Create initial data in DB
#python /wds_api/wds_api/initial_data.py
