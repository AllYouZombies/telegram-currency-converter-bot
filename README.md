# Kapusta Telegram bot

Multifunctional Telegram bot.  

> **It's not about purpose of the bot, but about the way it's made.**

You can use it as a template for your own bots.  
It's easy to add new commands and features.

I didn't want to use any frameworks like Flask or Django.
So I made it from scratch using only [python-telegram-bot](https://python-telegram-bot.org/) library.

Since no frameworks are used, the bot turned out to be as fast as possible.

---

## Quick start

```shell
git clone https://gitlab.anttek.io/kapusta/telegram-bot.git kapusta-telegram-bot
cd kapusta-telegram-bot
cp .env.example .env
# Fill .env with your data
docker compose up -d --build
```

## Features implemented

- [x] [Localization](docs/localization.md)
- [x] Polling mode
- [x] Latest async Telegram API support
- [x] Database support
- [x] Async tasks using [Celery](https://docs.celeryproject.org/en/stable/)
- [x] Docker, Docker Compose and Docker Swarm support

## Features to be implemented

- [ ] Fully asynchronous mode
- [ ] Webhook mode
- [ ] Telegram payments
- [ ] Database migrations management
- [ ] Caching using [Redis](https://redis.io/)
- [ ] [Logging](https://docs.python.org/3/library/logging.html)
- [ ] [Testing](https://docs.python.org/3/library/unittest.html)
- [ ] [CI/CD](https://en.wikipedia.org/wiki/CI/CD)
- [ ] Kubernetes deployment
