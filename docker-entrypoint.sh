#!/bin/sh

alembic upgrade head || exit 1

exec "$@"
