#!/bin/bash

dotenvx run -- .venv/bin/python scripts/fetch_time_series.py --symbol USD/JPY --interval 5min --size 672
dotenvx run -- .venv/bin/python scripts/fetch_time_series.py --symbol USD/JPY --interval 15min --size 672
dotenvx run -- .venv/bin/python scripts/fetch_time_series.py --symbol USD/JPY --interval 1h --size 720
dotenvx run -- .venv/bin/python scripts/fetch_time_series.py --symbol USD/JPY --interval 4h --size 360
dotenvx run -- .venv/bin/python scripts/fetch_time_series.py --symbol USD/JPY --interval 1day --size 360