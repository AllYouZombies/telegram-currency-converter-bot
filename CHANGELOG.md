# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

<!-- insertion marker -->
## [1.1.2](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/tags/1.1.2) - 2023-08-21

<small>[Compare with 1.1.1](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/compare/1.1.1...1.1.2)</small>

### Added

- Added some improvements ([afdc7df](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/commit/afdc7dfeb3481a7ec95331ea1fd98d5eca634b96) by Рустам Астафеев).

## [1.1.1](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/tags/1.1.1) - 2023-08-21

<small>[Compare with 1.1.0](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/compare/1.1.0...1.1.1)</small>

### Added

- Added some improvements ([dc589d0](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/commit/dc589d077c7a7eacb9495ec2583148426ea1ffc1) by Рустам Астафеев).

## [1.1.0](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/tags/1.1.0) - 2023-08-21

<small>[Compare with 1.0.1](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/compare/1.0.1...1.1.0)</small>

### Added

- Added feature to get rates without query ([9162ee7](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/commit/9162ee75564e4bc4fd6b16674890fe777e972161) by Рустам Астафеев).

## [1.0.1](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/tags/1.0.1) - 2023-08-21

<small>[Compare with 1.0.0](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/compare/1.0.0...1.0.1)</small>

### Changed

- Changed: don't convert in description ([b21178b](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/commit/b21178bf4602c78698160cbd4727130a4398e67d) by Рустам Астафеев).

## [1.0.0](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/tags/1.0.0) - 2023-08-21

<small>[Compare with 0.2.4](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/compare/0.2.4...1.0.0)</small>

## [0.2.4](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/tags/0.2.4) - 2023-08-21

<small>[Compare with 0.2.3](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/compare/0.2.3...0.2.4)</small>

### Added

- Added needs: ['build'] to image push stage ([e213064](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/commit/e213064ba1f5ba566fb497b927d89a6670f05047) by Рустам Астафеев).

### Fixed

- Fixed wrong service name ([2ef3f17](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/commit/2ef3f171ee6670da1d6615caa6d287b302c99716) by Рустам Астафеев).
- Fixed syntax error: unexpected end of file (expecting "fi") ([2e3ba03](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/commit/2e3ba03ddbeace3d84a8a2b37274e7ecaa384779) by Рустам Астафеев).
- Fixed celery container new name ([4e7cdd4](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/commit/4e7cdd4734c47516de29635181e082dbcdbe2398) by Рустам Астафеев).

### Changed

- Changed text on start ([c6d40ee](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/commit/c6d40eecadbfa4eea9b15cc9a24f3ae98c048d1e) by Рустам Астафеев).
- Changed gitlab pipeline: split build and push phases ([361c659](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/commit/361c6596873062c8a41f7becc31711cfc3c2e157) by Рустам Астафеев).

### Removed

- Removed build stages split ([cebbc9b](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/commit/cebbc9b8bd9ddd197bcbeb4844976e313f10b49a) by Рустам Астафеев).

## [0.2.3](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/tags/0.2.3) - 2023-08-21

<small>[Compare with 0.2.2](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/compare/0.2.2...0.2.3)</small>

### Added

- Added text translation ([b81e820](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/commit/b81e82035b49b16fdcc39096836731512feec137) by Рустам Астафеев).

## [0.2.2](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/tags/0.2.2) - 2023-08-21

<small>[Compare with 0.2.1](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/compare/0.2.1...0.2.2)</small>

### Added

- Added user saving ([545b74e](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/commit/545b74e2333743993039775156f70847814ddbe4) by Рустам Астафеев).
- Added hello text with bot description ([e9210b4](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/commit/e9210b4cc4342fa611769ddab39d159f91bf11c2) by Рустам Астафеев).
- Added comment to celery service, it runs both worker and beat ([593a338](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/commit/593a33811f86a2089f7f1bc060a26bb018ecfb27) by Рустам Астафеев).
- Added empty Celery Beat schedule setting ([d1aa644](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/commit/d1aa6447428794582b231c197a42742a8ea41e63) by Рустам Астафеев).

## [0.2.1](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/tags/0.2.1) - 2023-08-18

<small>[Compare with 0.2.0](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/compare/0.2.0...0.2.1)</small>

### Added

- Added Celery Beat schedule to run periodic task ([7c6401b](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/commit/7c6401bb023bef3db0fb4692b747ccb013383e62) by Рустам Астафеев).

### Fixed

- Fixed image name ([2ffd579](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/commit/2ffd5792eb078db17ab0be6d883dcbd581da8468) by Рустам Астафеев).

### Changed

- Changed Celery container command to start with Beat ([8a0867a](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/commit/8a0867a5455d099e6a32de058bdece7cf8c6af74) by Рустам Астафеев).

## [0.2.0](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/tags/0.2.0) - 2023-08-18

<small>[Compare with 0.1.3](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/compare/0.1.3...0.2.0)</small>

### Fixed

- Fixed Celery autodiscover_tasks() can't discover tasks ([6bff463](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/commit/6bff463545d90daba7fef531fdd784c5a0060401) by Рустам Астафеев).

### Removed

- Removed unused stuff ([dfd51e8](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/commit/dfd51e805678a0b400bbb20bf14edadb85ee2932) by Рустам Астафеев).

## [0.1.3](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/tags/0.1.3) - 2023-08-18

<small>[Compare with 0.1.2](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/compare/0.1.2...0.1.3)</small>

### Changed

- Changed sessionmaker to async_sessionmaker Added pool_pre_ping=True to engine Removed for loop on top of session_scope() ([34aaeb7](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/commit/34aaeb7307d939fdeffcc6ae0b5ef4614a1df625) by Рустам Астафеев).

### Removed

- Removed unused libs from requirements ([a690fb6](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/commit/a690fb66548b8a001e33533c1a428013e8c660c7) by Рустам Астафеев).

## [0.1.2](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/tags/0.1.2) - 2023-08-18

<small>[Compare with 0.1.1](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/compare/0.1.1...0.1.2)</small>

### Fixed

- Fixed db session breaking down. Need to monitor from now ([138eba7](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/commit/138eba7dda9e37c2ab7248d6099ea2d68f76f72e) by Рустам Астафеев).
- Fixed user lang don't updated ([3c24730](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/commit/3c24730921727470c3ab5cf6241ae33088e8d3aa) by Рустам Астафеев).
- Fixed compose syntax ([4b1ea11](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/commit/4b1ea118e55e32ac2e142ca3079a26e10130ba0f) by Рустам Астафеев).

### Removed

- Removed environment definition as it's not usable with bot ([036c31e](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/commit/036c31edad8eea860ad307eb3c175327587befce) by Рустам Астафеев).

## [0.1.1](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/tags/0.1.1) - 2023-08-18

<small>[Compare with 0.1.0](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/compare/0.1.0...0.1.1)</small>

### Added

- Added .gitlab-ci.yml ([408d7b1](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/commit/408d7b1960ced1e20aa5f10dd9d4d7a10cfe2fba) by Рустам Астафеев).
- Added 2 separators in README.md ([83b2b77](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/commit/83b2b778c834479a8b0e883b51e868d347b32f97) by Рустам Астафеев).
- Added CONTRIBUTING.md, CODE_OF_CONDUCT.md ([4fb7c33](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/commit/4fb7c332b02ac56b3cf5e347962618203ffb5838) by Рустам Астафеев).
- Added CHANGELOG.md ([0f289a7](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/commit/0f289a74bd94a232d7a6176bab6a02c2727b341f) by Рустам Астафеев).

### Changed

- Changed image url to gitlab registry ([403ed91](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/commit/403ed919159c303f0c734d640ed969ca83f6f1f8) by Рустам Астафеев).

## [0.1.0](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/tags/0.1.0) - 2023-08-17

<small>[Compare with first commit](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/compare/ed5bc98d3974de5b1d8f4e4a1128f14b9dee8d4f...0.1.0)</small>

### Added

- Added LICENSE ([883c19a](https://gitlab.anttek.io/kapusta/telegram-currency-converter-bot/commit/883c19abc3b9b64747be5103ba07aed20e65ca9e) by Рустам Астафеев).

