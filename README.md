# tft-team-builder-INT2211
A web application project for INT2211

[![License is GPL-3.0](https://img.shields.io/github/license/duongoku/tft-team-builder-INT2211)](./LICENSE)

- [tft-team-builder-INT2211](#tft-team-builder-INT2211)
    - [Prerequisites](#prerequisites)
    - [Preparation](#preparation)
    - [Deployment](#deployment)
    - [Side Note](#side-note)

## Prerequisites
- [Python >=3.8](https://www.python.org/downloads/)
- [MySQL Server](https://dev.mysql.com/doc/mysql-installation-excerpt/5.7/en/general-installation-issues.html)
- [MySQL Workbench](https://dev.mysql.com/downloads/workbench/)

## Preparation
- Install necessary python modules with `pip install -r requirements.txt`
- Import database into MySQL with `mysql -u {yourusername} -p tft < tft.sql`
- Fill USER, PASSWORD, PORT inside query_mysql.py

## Deployment
- `set FLASK_APP=server.py`
- `flask run`

## Side Note
- Champions and Items images are taken from [here](https://developer.riotgames.com/docs/tft#static-data_current-set)