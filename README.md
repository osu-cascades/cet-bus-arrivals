1. Install <https://github.com/rrruko/cet_bus> by cloning it and running `pip3 install .`.
2. `cd` into the repo directory, then
```
python3 -m venv venv
. venv/bin/activate
gunicorn app:app
```
