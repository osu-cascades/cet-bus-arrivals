This application intermittently polls bus data from a service over HTTP and displays info about current bus positions and stops on a map.

# Database setup

You need to install sqlite3 and initialize gtfs.db with recent GTFS data before running. For CET, you can go to [this URL](https://transitfeeds.com/p/cascades-east-transit/440) to download an archive of GTFS data represented in CSV format. You can then import the CSV files into an SQLite database using the `.import` command, like this:

```
$ mkdir gtfs
$ curl https://openmobilitydata-data.s3-us-west-1.amazonaws.com/public/feeds/cascades-east-transit/440/20200519/gtfs.zip -o gtfs/gtfs.zip
$ cd gtfs
$ unzip gtfs.zip
$ cd ..
$ sqlite3 gtfs.db
> .mode csv
> .import gtfs/calendar.txt
> .import gtfs/routes.txt
> .import gtfs/shapes.txt
> .import gtfs/stops.txt
> .import gtfs/stop_times.txt
> .import gtfs/trips.txt
```

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
