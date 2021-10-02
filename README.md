# Qlik community blog posts scraper

---

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

_Download metadata and links for all Qlik community blog posts into a Sqlite database and make it explorable through Datasette, deploy with Docker_

* Find out the most viewed or liked blog post
* Trending writers
* Explore through SQL-queries

## Installation and usage
### Installation

- Create a virtual environment with Python 3.5 or above
- Activate virtualenv and install `requirements.txt`
- Run `python program.py` in order to create `qlik_posts.db`

### Usage
- Create Docker image `datasette package --install datasette-vega qlik_posts.db -t datasette_qlikposts`
- Run container `docker run -d --rm -p 8081:8001 --name datasette_qlik datasette_qlikposts`
- Explore data at `http://localhost:8081/`
