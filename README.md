# SpaceX Tickets

Simple Django web service used to book space-x trips.
Developed using PyCharm and Python 3.

## Requirements
0. **python3** (3.5 and 3.6 tested)
0. **pip** >= 10.0.1
0. **sqlite3** (standard db)
0. bash (to run the scripts)
0. cron (or any other kind of scheduler)
0. **pandoc**, **texlive** and **lmodern** (to compile the documentation)

## Compiling the documentation
0. Install the requirements, in Debian and derivatives:
    ```bash
    apt-get install pandoc texlive lmodern
    ```
0. Use pandoc:
    ```bash
    pandoc input.md -o output.pdf
    ```
0. In alternative you can use the `markdown` command which will generate an html file or [Dillinger.io](https://dillinger.io/).


## Installation
0. Install the requirements, on Debian and derivatives:
    ```bash
    sudo apt-get install python3 python3-pip
    ```
0. Install the python requirements
    ```bash
    pip install -r requirements.txt
    ```
0. Compile the locales by running:
    ```bash
    ./manage.py compilemessages
    ```
0. Tweak the db settings in `spacextickets/spacextickets/settings.py`, if needed.
0. Create the DB schema by manually running:
    ```bash
    ./manage.py migrate
    ```
0. Run the server using
    ```bash
    ./manage.py runserver host:port
    ```
### Additional configurations
* Create a super-user account using the provided script:
    ```bash
    ./scripts/create-super-user.sh root@localhost password
    ```
    **Note:** it is possible to use `manage.py` to create the super user but it will ask for additional information.
* Populate the db using the script `scripts/populate-db.sh`
* Config the wsgi in `spacextickets/spacextickets/wsgi.py`
* Customize the script `clean-db.sh` and run it via a [cron job](https://debian-administration.org/article/56/Command_scheduling_with_cron) to remove the temporary orders regularly.
* Additional documentation can be found under the `doc` folder
## Authors
* [Jacopo Scannella](https://github.com/antipatico) - _paranoid_
* Alessio Lei - _actually has a life_
