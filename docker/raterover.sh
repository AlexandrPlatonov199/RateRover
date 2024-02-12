#!/bin/bash

sleep 40

poetry run python -m raterover currency_course database migrations apply

poetry run python -m raterover currency_course run



