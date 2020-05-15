This application intermittently polls bus data from a service over HTTP and displays info about current bus positions and stops on a map.

# Database setup

You need to initialize gtfs.db with recent GTFS data before running. For CET, you can go to [this URL](https://transitfeeds.com/p/cascades-east-transit/440) to download an archive of GTFS data represented in CSV format. You can then import the CSV files into an SQLite database using the `.import` command.

# Python dependencies

This application is intended to be run with python 3.7. You need to have the following python packages installed:
- flask

Alternatively, if you have nix installed, you can simply run `nix-shell shell.nix` to enter a shell with all required packages installed.

# Running

You have to specify the URL from which bus data will be acquired via an environment variable, like this:

```
$ export LOGGING_SERVICE_URL=http://localhost:5001
```

You can run the application with `flask run -p PORT`, where `PORT` is the port on which you want the application to serve the frontend.
