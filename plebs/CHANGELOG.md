# CHANGELOG

## [1.4.0] - 2019-04-05
### Added
- `--bdays` flag added to `export pdf` command. Creates a PDF with ONLY the birthday page.
- `publish pdf` now published the birthday page too.

### Changed
- BDay Page
    - Month names are now bolded
    - Use `~~~` around month names instead of dashes. Prettier. ;)

### Fixed
- Sort order of names on the birthday page was random. Fixed each month to order each members name by bday day.
- Added ability to adjust month placement on Bday page so that any month list does not overlap another.
  - Adjusted October. It was too close to December.

## [1.3.0] - 2018-11-13
### Added
- `publish app` command. Will publish the Web App.

### Changed
- Factored out FTP code from `commands/publish.py` to `lib/publisher.py`
- Re-wrote `publish` commands to use `publisher.py`
- Changed options in config file for "publish" section. Updated `example.yml`

### Fixed
- `config.py` - Use `os.path.join` in `path()` instead of assuming `/`

### Removed
- `static/directory.json.example` (Don't feel like maintaining it)

## [1.2.1] - 2018-11-12
### Changed
- Renamed the CLI from `directory/directory.py` to `plebs/cli.py`

## [1.2.0] - 2018-11-05
### Added
- `import vcf` command
    - Ported `bin/vcf2plebeians.py` to `VCFParser.py` class
- `publish photo` command

## [1.1.0] - 2018-10-31
### Fixed
- Saving `directory.json` no longer adds a space after each comma 

### Added
- `publish` command
    - data
    - pdf
- Requires a config file (defaults to `$HOME/.config/plebeians.yml`)
    - Example in `directory/config/example.yml`

### Changed
- Re-worked several commands / classes to work with config file instead
  of using hard-coded values
