FROM python:3.10-slim-bullseye as base

ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1


FROM base AS deps

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -U pipenv \
    && apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/*

RUN --mount=type=bind,source=Pipfile,target=Pipfile \
    pipenv lock \
    && pipenv requirements > requirements.txt \
    && python -m venv /venv \
    && . /venv/bin/activate \
    && pip install -r requirements.txt


FROM base AS runtime

RUN useradd --create-home appuser

USER appuser

WORKDIR /home/appuser

COPY --from=deps --chown=appuser:appuser /venv /venv

ENV PATH="/venv/bin:$PATH"

COPY --chown=appuser:appuser . .

RUN chmod +x docker-entrypoint.sh

ENTRYPOINT ["/home/appuser/docker-entrypoint.sh"]

CMD ["python", "main.py"]

VOLUME /home/appuser/uploads
