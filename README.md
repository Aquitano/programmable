# Programmable

Programmable is a small Django social app for sharing short posts, following other users, and keeping a lightweight profile.

## Stack

- Python
- Django
- SQLite for local development
- Pillow for profile images
- Python-Markdown for post formatting

## Notes

A tracked `db.sqlite3` file is still present in the repository. That is fine for a classroom exercise, but it is not something I would keep in a real app with user data. If this project is going anywhere public, remove the database from version control and rotate any credentials that may have lived in it.
