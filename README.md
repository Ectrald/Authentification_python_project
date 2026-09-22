# Email-Based Authentication Service

A FastAPI authentication service with one-time email verification. A user registers with an email address, receives a verification link by mail, and is automatically authorized after following that link.

## Features

- Registration with email-format validation and duplicate checks
- Verification email with a single-use, expiring link
- Clicking the link verifies the email and issues a JWT access token
- Resend endpoint for the verification email
- Password login for verified accounts
- Protected user endpoint (`GET /users/me`)

## Tech Stack

- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- bcrypt
- PyJWT
- aiosmtplib

## Project Structure

```
app/
  core/             # security, email sending, exception handling
  db/               # database engine and session
  domains/
    users/          # user model, schema, CRUD, errors
    tokens/         # verification tokens, schema, CRUD, errors
  routers/          # auth and users endpoints
alembic/            # database migrations
Dockerfile
docker-compose.yml
```

## Running with Docker

The `docker-compose.yml` brings up a Postgres database and the application, runs the migrations, and starts the server.

```
docker compose up --build
```

API documentation (Swagger UI) is available at:

```
http://localhost:8000/docs
```


## Configuration

Copy `.env.example` to `.env` and fill in the values. The available variables:

| Variable | Purpose |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string (`postgresql+psycopg2://user:pass@host:5432/db`) |
| `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` | Used by the Postgres container only |
| `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, `SMTP_FROM` | SMTP server and sender account |
| `FRONTEND_URL` | Base URL the verification link points to |
| `TOKEN_EXPIRE_MINUTES` | Verification token lifetime |
| `JWT_SECRET_KEY`, `JWT_ALGORITHM`, `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT signing and lifetime |

For Gmail, `SMTP_PASSWORD` must be an app password, not the account password. Generate it in the Google account settings (two-factor authentication has to be enabled) at `https://myaccount.google.com/apppasswords`.

## How It Works

1. `POST /register` with `username`, `password` and `email`. The email address is validated, and a verification token is stored. The token is emailed only after a successful SMTP send; if the email cannot be delivered, the request fails with `502` and the user is not stored in the database.
2. The user follows the link from the email. It points to `FRONTEND_URL/verify?token=...`.
3. The verification page calls `POST /verify-email` with the token. If the token is valid and unused, the account is marked as verified and the response contains an `access_token`, which means the user is signed in.
4. The `access_token` is passed as `Authorization: Bearer <token>` for authenticated requests such as `GET /users/me`.

There is no frontend in this repository. The verification link points to `FRONTEND_URL`, which may not be running. Until a frontend is available, verification can be done directly through Swagger: copy the token from the link and send `POST /verify-email` with `{"token": "..."}` as the body.

## API Endpoints

| Method | Path | Body | Result |
|---|---|---|---|
| `POST` | `/register` | `{"username", "password", "email"}` | `201` — user saved, verification email sent |
| `POST` | `/verify-email` | `{"token"}` | `200` — email verified, returns `access_token` |
| `POST` | `/resend-verification` | `{"email"}` | `200` — new verification email sent |
| `POST` | `/token` | form `username`/`email` + `password` | `200` — returns `access_token` (verified accounts only) |
| `GET` | `/users/me` | Bearer token | `200` — current user |

Key error responses: `400` for already registered emails or usernames and for used or expired tokens, `401` for wrong credentials or an invalid token, `403` when logging in with an unverified email, `502` when the verification email could not be sent.

## Demonstration

Verification email as sent from the SMTP server:

![Отправленное](demonstration/Отправленное.jpg)

The same email as received in the recipient's inbox:

![Принятое](demonstration/Принятое.jpg)

Authorize dialog in Swagger UI:

![Авторизация](demonstration/Авторизация.jpg)

Authenticated request to `GET /users/me`:

![Подтверждение авторизации](demonstration/Подтверждение%20авторизации.jpg)
