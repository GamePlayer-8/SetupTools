<p align="center">
  <b>Build software in Github Actions easily.</b>
</p>

<p><hr></p>

# How-to

 * The script `setuptools.py` is an ultimate thing for Github Actions to automatically build everything and upload it as branch or release.
 * It has auto - versioning module and so on.
 * Repository is being used by YAML config file in `.github/workflows/SetupTools.yml`.
 * To configure runtime you need to make `SetupTools` text file and insert the runtime arguments.
 * To get all available arguments, use `python setuptools.py`.
 * Script only requires `python`, `git`, `wget`, `curl`. By default it can install all packages (excluding `python`).
 * No third-party container and stuff required.

# Getting Help | Copyright | etc

On [HELP.md](HELP.md) is everything needed about it ^.
