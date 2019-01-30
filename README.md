# SpaceX Tickets

Simple Django web service used to book space-x trips.
Developed using PyCharm, Python 3, Django, Bootstrap and JQuery.

## Requirements
0. **python3** (3.5 and 3.6 tested)
1. **pip3** >= 10.0.1
3. **sqlite3** (standard db)
4. bash (to run the scripts)
5. cron (or any other kind of scheduler)
6. **pandoc**, **texlive** and **lmodern** (to compile the documentation)

## Compiling the documentation
**NOTE:** the documentation is in **Italian** only.

0. Install the requirements, in Debian and derivatives:
    ```bash
    apt-get install pandoc texlive lmodern
    ```
1. Use pandoc:
    ```bash
    pandoc input.md -o output.pdf
    ```
2. In alternative you can use the `markdown` command which will generate an html file or compile it online using [Dillinger.io](https://dillinger.io/).


## Automatic Installation (using setup.sh)
0. Run `setup.sh`
**NOTE**: this will install **virtualenv** in your pip environment.
1. Your root login is `root@localhost` the password is `hunter2`.
2. You should setup the cron-job for the cleanup of unfinished orders (see Additional Configurations below)

## Manual Installation (without venv)
0. Install the requirements, on Debian and derivatives:
    ```bash
    sudo apt-get install python3 python3-pip
    ```
2. Install the python requirements
    ```bash
    pip install -r requirements.txt
    ```
2. Compile the locales by running:
    ```bash
    ./manage.py compilemessages
    ```
3. Tweak the db settings in `spacextickets/spacextickets/settings.py`, if needed.
4. Create the DB schema by manually running:
    ```bash
    ./manage.py migrate
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

## Running the project 
0. Activate the **virtualenv** (if installed with `setup.sh`)
   ```bash
   source venv/bin/activate
   ```
1. Run the server using
    ```bash
    ./manage.py runserver host:port
    ```
2. Browse `host:port`

## License
This project is licensed under the VRLFSC version 1.1.
You can find the full license under the file LICENSE.txt

## Authors
* [Jacopo Scannella](https://github.com/antipatico) - _paranoid_
* [Alessio Lei](https://github.com/AlessioLei94) - _actually has a life_

