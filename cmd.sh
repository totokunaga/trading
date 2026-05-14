#!/bin/bash

dotenvx run -- .venv/bin/python scripts/fetch_time_series.py --symbol USD/JPY --interval 15min --size 1344
dotenvx run -- .venv/bin/python scripts/fetch_time_series.py --symbol USD/JPY --interval 1h --size 720
dotenvx run -- .venv/bin/python scripts/fetch_time_series.py --symbol USD/JPY --interval 4h --size 180
dotenvx run -- .venv/bin/python scripts/fetch_time_series.py --symbol USD/JPY --interval 1day --size 30