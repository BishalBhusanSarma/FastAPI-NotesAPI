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

## Test the API with Postman

### 1. Set the base URL

Create a Postman environment and add a variable named `base_url`.

| Environment | `base_url` value |
| --- | --- |
| Local | `http://127.0.0.1:8000` |
| Deployed | `https://your-render-service.onrender.com` |

Also add empty variables named `access_token`, `refresh_token`, and `note_id`. Use `{{base_url}}` in every request URL below.

### 2. Register a user

Create a request with these settings:

```text
POST {{base_url}}/notesapi/register_user
```

Select **Body** → **raw** → **JSON**, then send:

```json
{
  "name": "Bishal",
  "username": "bishal",
  "email": "bishal@example.com",
  "h_pwd": "a-strong-password"
}
```

You should receive a `User created` response and an ID. Use a unique username and email each time you register.

### 3. Log in and save tokens

Create this request:

```text
POST {{base_url}}/notesapi/login
```

Select **Body** → **x-www-form-urlencoded** and add:

| Key | Value |
| --- | --- |
| `username` | `bishal` or `bishal@example.com` |
| `password` | `a-strong-password` |

The response contains `access_token` and `refresh_token`. In the request's **Tests** tab, add this script to save them automatically:

```javascript
const response = pm.response.json();
pm.environment.set("access_token", response.access_token);
pm.environment.set("refresh_token", response.refresh_token);
```

After sending, check that the Postman environment contains both token values.

### 4. Authorize protected requests

For each request below, open the **Authorization** tab and set:

```text
Type: Bearer Token
Token: {{access_token}}
```

Do not send the token as a request body value. It is sent in the `Authorization` header.

### 5. Create a note

```text
POST {{base_url}}/notesapi/create_note
```

Set Bearer Token authorization. Select **Body** → **raw** → **JSON**:

```json
{
  "title": "First note",
  "content": "My note content"
}
```

The response includes the note ID. Save it as the Postman `note_id` environment variable.

### 6. List the current user's notes

```text
GET {{base_url}}/notesapi/show_notes
```

Set Bearer Token authorization. This is a `GET` request and has no body. It returns only notes belonging to the authenticated user.

### 7. Update a note

```text
PUT {{base_url}}/notesapi/update_notes
```

Set Bearer Token authorization. Select **Body** → **raw** → **JSON**:

```json
{
  "id": {{note_id}},
  "title": "Updated title",
  "content": "Updated note content"
}
```

### 8. Delete a note

```text
DELETE {{base_url}}/notesapi/delete_note?note_id={{note_id}}
```

Set Bearer Token authorization. No request body is required.

### 9. Refresh an expired access token

```text
POST {{base_url}}/notesapi/refresh
```

This endpoint does not use the Authorization header. Select **Body** → **raw** → **JSON**:

```json
{
  "refresh_token": "{{refresh_token}}"
}
```

Copy the returned `new_access_token` into `access_token`, then use it for protected requests.

## Example note payload

```json
{
  "title": "First note",
  "content": "My note content"
}
```
