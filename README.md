# Python TodoX
A todo app built with FastAPI, SQLite, and HTMX.

> :warning: **NOT SECURE**

This is a sample project to test out bulding apps with HTMX and Python.

## The Stack
- Python
- FastAPI
- Jinja Templates
- Jinja Fragments
- SQLite (no ORM)
- HTMX

## The Findings
- HTMX and Jinja templates with fragments work well together. Jinja without fragements is a bit of a pain.
- FastAPI works as expected.
- The SQLite3 lib in the Python stdlib works great in an async context as long as you use one connection per request lifecycle. Not sure about the performance implications of doing this.

## How to run it
1. Ensure you have python 3.12 or later
2. Clone this repo
3. `cd` into the directory
4. run `pipenv install` to install dependencies
5. run `pipenv init_db` to create the todo table
5. run `pipenv dev` to start the application