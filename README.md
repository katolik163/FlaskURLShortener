# URL Shortener

A simple Flask link shortener application

## Screenshots

![Screenshot](screenshots/preview1.png)
![Screenshot](screenshots/preview2.png)
![Screenshot](screenshots/preview3.png)

## Installation

Clone the repo:

```
git clone https://github.com/katolik163/flaskurlshortener.git
cd flaskurlshortener
```

Create and activate virtual environment then install dependencies:

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Edit ```.flaskenv``` and ```config.py```

Create database:

```
flask db upgrade
```

Run application:

```
flask run
```