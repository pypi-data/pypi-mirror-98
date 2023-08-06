# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2021-03-12

### Added

- on Windows, `colorama` will be initialized from the start

### Changed

- **POTENTIALLY BREAKING:** `SanePrinter._print()` has a new signature: `_print(str, Iterable[int], bool)`. Keep in mind, that you shouldn't really use this method. Other methods are left unchanged

## [0.1.0] - 2021-03-11

### Added

- `SanePrinter` class to manage settings and output
- `out`, the main global instance of `SanePrinter`

### Removed

- unit tests; for now only doctests are used, the migration to pytest is planned for later

[Unreleased]: https://github.com/sane-out/python/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/sane-out/python/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/sane-out/python/compare/v0.0.1...v0.1.0
