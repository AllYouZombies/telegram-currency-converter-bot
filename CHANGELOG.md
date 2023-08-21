# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

<!-- insertion marker -->
## Unreleased

<small>[Compare with latest](https://gitlab.anttek.io/kapusta/telegram-bot/compare/0.1.2...HEAD)</small>

### Added

- Added needs: ['build'] to image push stage ([e213064](https://gitlab.anttek.io/kapusta/telegram-bot/commit/e213064ba1f5ba566fb497b927d89a6670f05047) by Рустам Астафеев).
- Added comment to celery service, it runs both worker and beat ([593a338](https://gitlab.anttek.io/kapusta/telegram-bot/commit/593a33811f86a2089f7f1bc060a26bb018ecfb27) by Рустам Астафеев).
- Added empty Celery Beat schedule setting ([d1aa644](https://gitlab.anttek.io/kapusta/telegram-bot/commit/d1aa6447428794582b231c197a42742a8ea41e63) by Рустам Астафеев).

### Fixed

- Fixed wrong service name ([2ef3f17](https://gitlab.anttek.io/kapusta/telegram-bot/commit/2ef3f171ee6670da1d6615caa6d287b302c99716) by Рустам Астафеев).
- Fixed syntax error: unexpected end of file (expecting "fi") ([2e3ba03](https://gitlab.anttek.io/kapusta/telegram-bot/commit/2e3ba03ddbeace3d84a8a2b37274e7ecaa384779) by Рустам Астафеев).
- Fixed celery container new name ([4e7cdd4](https://gitlab.anttek.io/kapusta/telegram-bot/commit/4e7cdd4734c47516de29635181e082dbcdbe2398) by Рустам Астафеев).
- Fixed Celery autodiscover_tasks() can't discover tasks ([6bff463](https://gitlab.anttek.io/kapusta/telegram-bot/commit/6bff463545d90daba7fef531fdd784c5a0060401) by Рустам Астафеев).

### Changed

- Changed gitlab pipeline: split build and push phases ([361c659](https://gitlab.anttek.io/kapusta/telegram-bot/commit/361c6596873062c8a41f7becc31711cfc3c2e157) by Рустам Астафеев).
- Changed Celery container command to start with Beat ([8a0867a](https://gitlab.anttek.io/kapusta/telegram-bot/commit/8a0867a5455d099e6a32de058bdece7cf8c6af74) by Рустам Астафеев).
- Changed sessionmaker to async_sessionmaker Added pool_pre_ping=True to engine Removed for loop on top of session_scope() ([34aaeb7](https://gitlab.anttek.io/kapusta/telegram-bot/commit/34aaeb7307d939fdeffcc6ae0b5ef4614a1df625) by Рустам Астафеев).

### Removed

- Removed build stages split ([cebbc9b](https://gitlab.anttek.io/kapusta/telegram-bot/commit/cebbc9b8bd9ddd197bcbeb4844976e313f10b49a) by Рустам Астафеев).
- Removed unused libs from requirements ([a690fb6](https://gitlab.anttek.io/kapusta/telegram-bot/commit/a690fb66548b8a001e33533c1a428013e8c660c7) by Рустам Астафеев).

<!-- insertion marker -->
## [0.1.2](https://gitlab.anttek.io/kapusta/telegram-bot/tags/0.1.2) - 2023-08-18

<small>[Compare with 0.1.1](https://gitlab.anttek.io/kapusta/telegram-bot/compare/0.1.1...0.1.2)</small>

### Fixed

- Fixed db session breaking down. Need to monitor from now ([138eba7](https://gitlab.anttek.io/kapusta/telegram-bot/commit/138eba7dda9e37c2ab7248d6099ea2d68f76f72e) by Рустам Астафеев).
- Fixed user lang don't updated ([3c24730](https://gitlab.anttek.io/kapusta/telegram-bot/commit/3c24730921727470c3ab5cf6241ae33088e8d3aa) by Рустам Астафеев).
- Fixed compose syntax ([4b1ea11](https://gitlab.anttek.io/kapusta/telegram-bot/commit/4b1ea118e55e32ac2e142ca3079a26e10130ba0f) by Рустам Астафеев).

### Removed

- Removed environment definition as it's not usable with bot ([036c31e](https://gitlab.anttek.io/kapusta/telegram-bot/commit/036c31edad8eea860ad307eb3c175327587befce) by Рустам Астафеев).

## [0.1.1](https://gitlab.anttek.io/kapusta/telegram-bot/tags/0.1.1) - 2023-08-18

<small>[Compare with 0.1.0](https://gitlab.anttek.io/kapusta/telegram-bot/compare/0.1.0...0.1.1)</small>

### Added

- Added .gitlab-ci.yml ([408d7b1](https://gitlab.anttek.io/kapusta/telegram-bot/commit/408d7b1960ced1e20aa5f10dd9d4d7a10cfe2fba) by Рустам Астафеев).
- Added 2 separators in README.md ([83b2b77](https://gitlab.anttek.io/kapusta/telegram-bot/commit/83b2b778c834479a8b0e883b51e868d347b32f97) by Рустам Астафеев).
- Added CONTRIBUTING.md, CODE_OF_CONDUCT.md ([4fb7c33](https://gitlab.anttek.io/kapusta/telegram-bot/commit/4fb7c332b02ac56b3cf5e347962618203ffb5838) by Рустам Астафеев).
- Added CHANGELOG.md ([0f289a7](https://gitlab.anttek.io/kapusta/telegram-bot/commit/0f289a74bd94a232d7a6176bab6a02c2727b341f) by Рустам Астафеев).

### Changed

- Changed image url to gitlab registry ([403ed91](https://gitlab.anttek.io/kapusta/telegram-bot/commit/403ed919159c303f0c734d640ed969ca83f6f1f8) by Рустам Астафеев).

## [0.1.0](https://gitlab.anttek.io/kapusta/telegram-bot/tags/0.1.0) - 2023-08-17

<small>[Compare with first commit](https://gitlab.anttek.io/kapusta/telegram-bot/compare/ed5bc98d3974de5b1d8f4e4a1128f14b9dee8d4f...0.1.0)</small>

### Added

- Added LICENSE ([883c19a](https://gitlab.anttek.io/kapusta/telegram-bot/commit/883c19abc3b9b64747be5103ba07aed20e65ca9e) by Рустам Астафеев).

