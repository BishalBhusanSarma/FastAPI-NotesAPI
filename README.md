# Notes API

A REST API for user registration, JWT-based authentication, token refresh, and private note management. Built with FastAPI and PostgreSQL.

## Features

- Register and authenticate users
- Argon2 password hashing
- JWT access and refresh tokens
- Create, read, update, and delete notes
- Notes are scoped to the authenticated user

## Tech stack

Python, FastAPI, PostgreSQL, Psycopg, Pydantic, Passlib/Argon2, and `python-jose`.

## Run locally

1. Create and activate a virtual environment.

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies.

   ```bash
   pip install -r requirements.txt
   ```

3. Create a PostgreSQL database, then load the schema.

   ```bash
   psql -d notes_db -f schema.sql
   ```

4. Copy the environment template and add your local values.

   ```bash
   cp .env.example .env
   ```

5. Start the server.

   ```bash
   uvicorn main:app --reload
   ```



## Environment variables

| Variable | Description |
| --- | --- |
| `DATABASE_URL` | PostgreSQL connection string |
| `SECRET_KEY` | Long, random key used to sign JWTs |
| `ALGORITHM` | JWT algorithm, for example `HS256` |
| `ACCESS_TOKEN_EXP` | Access-token lifetime in minutes |
| `REFRESH_TOKEN_EXP` | Refresh-token lifetime in days |



## API endpoints

| Method | Endpoint | Authentication | Purpose |
| --- | --- | --- | --- |
| POST | `/notesapi/register_user` | No | Register a user |
| POST | `/notesapi/login` | No | Get access and refresh tokens |
| POST | `/notesapi/refresh` | No | Exchange a refresh token for an access token |
| POST | `/notesapi/create_note` | Bearer token | Create a note |
| GET | `/notesapi/show_notes` | Bearer token | List the current user's notes |
| PUT | `/notesapi/update_notes` | Bearer token | Update one of the user's notes |
| DELETE | `/notesapi/delete_note?note_id={id}` | Bearer token | Delete one of the user's notes |

Use the access token returned by `/notesapi/login` as `Authorization: Bearer <access_token>` for protected routes.

## Example note payload

```json
{
  "title": "First note",
  "content": "My note content"
}
```
