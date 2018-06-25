# Distributions of height for the different positions in the 2018 FIFA World Cup

Copyright 2018 Denis Meyer
Data: Copyright 2018 FIFA

This is the source code in case you don't want to use the jupyter notebook.

## Prerequisites

* Python 3
* Windows
  * Install NSIS - http://nsis.sourceforge.net
  * Add Python to PATH variable in environment
  * Add NSIS to PATH variable in environment

## Usage

* Start shell
  * Windows
    * Start shell as administrator
    * `Set-ExecutionPolicy Unrestricted -Force`
* Create a virtual environment
  * `python -m venv venv`
* Activate the virtual environment
  * Mac/Linux
    * `source venv/bin/activate`
  * Windows
    * `.\venv\scripts\activate`
* Install the required libraries
  * `pip install -r requirements.txt`
* Run the app
  * `python -m fbs run`
