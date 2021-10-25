#! /usr/bin/env bash

# Let the DB start
python /app/app/backend_pre_start.py
# Run migrations
alembic upgrade head
# Create initial data in DB
python /app/app/initial_data.py

#if [ -e /opt/homebrew/bin/python3 ]
#then
#    # Let the DB start
#    /opt/homebrew/bin/python3 /app/app/backend_pre_start.py
#    # Run migrations
#    alembic upgrade head
#    # Create initial data in DB
#    /opt/homebrew/bin/python3 /app/app/initial_data.py
#else
#    python /app/app/backend_pre_start.py
#    alembic upgrade head
#    python /app/app/initial_data.py
#fi

