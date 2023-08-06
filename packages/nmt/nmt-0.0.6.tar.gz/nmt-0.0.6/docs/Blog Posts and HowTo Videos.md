# Blog Posts and HowTo Videos

## 2021-01-02 Winnie

[raw 60+ minute video](https://tan.sfo2.digitaloceanspaces.com/videos/howto/howto-create-python-package-using-pyscaffold-2021-01-02.mp4) (needs editing)

### Create a Python Package

- Create `~/.pypirc` to hold your pypi.org credentials (tokens)
- Install `pyscaffold` (the `putup` command)
- Use `putup --gitlab {yourpackagename}` to create scaffolding code
- Copy over `setup.py`, `setup.cfg`, and `.gitlab-ci.yml` into your project directory
- Create `requirements.txt` and `test-requirements.txt` files in the project directory
- Create `environment.yml` duplicating those dependencies in requirements.txt that have conda packages
- Add your dependencies from `requirements.txt` and `test-requirements.txt` to `setup.cfg`
- Make sure all your python code is in the `src/` directory inside your project folder
- Always `git status`, `git add`, `git commit`, and `git push` new files each time you change anything
- Add 'before_script' to gitlab-ci with commands from your `README.md` installation instructions (`conda create`, `conda update`)
- Make sure imports in your modules use the fully qualified module name, e.g. `import yourpackage.utils`

### Configure Automagic Linting

- [Install Sublime Text](https://www.sublimetext.com/3)
- Within Sublime Text: Preferences->Package Control->Install Package->Sublime Linter
- Within Sublime Text: Preferences->Package Control->Install Package->Anaconda
- Within Sublime Text: Preferences->Package Settings->Anaconda->Settings-Default
- Within Sublime Text: Preferences->Package Settings->Anaconda->Settings--User : `"auto_formatting": true`
