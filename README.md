[![CI/CD](https://github.com/IU-Capstone-Project-2024/Team-44/actions/workflows/main.yml/badge.svg)](https://github.com/IU-Capstone-Project-2024/Team-44/actions/workflows/main.yml)

# Team-44
# StudyBoost

Our project is an integrated study tool designed to assist Innopolis University students in organizing their study materials, managing their time effectively, and enhancing their learning efficiency. Available a web platform that provides functionalities such as automatic quiz generation from notes, note summarization

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Features](#features)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)


## Installation

```bash

docker-compose up -d --build

```

Check the `http://localhost:8000/`

### Usage

Backend:

```bash
# Clone the repository
git clone https://github.com/IU-Capstone-Project-2024/Team-44.git

# Navigate to the project directory
cd Team-44/rag_backend

# Install dependencies
pip install -r requirements.txt

# Create .env file with following content:
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
EMAIL_HOST_USER=<your email>
EMAIL_HOST_PASSWORD=<your password from https://myaccount.google.com/apppasswords>

# Migrate
python manage.py migrate

# Run the server
python manage.py runserver

# (Optional) Testing
python manage.py test   # you can specify modules which you want to test
```

## API Endpoints

### 1. Sign Up

**Endpoint:** `POST /authentication/api/signup/`

**Description:** Sign up a new user and send a verification link to the provided email.

**Request:**

- Headers: `Content-Type: application/json`
- Body: `{
    "username": "string",
    "email": "email",
    "first_name": "string",
    "last_name": "string",
    "telegram_id": "string",
    "password": "string"
}`

**Response:**

- `201 Created` - User created and email verification sent
- `400 Bad Request` - The request body is invalid or incomplete.

### 2. Verify Email

**Endpoint:** `GET /authentication/api/email-verify/{uid}/{token}/`

**Description:** Verify the user's email address using the provided uid and token.

**Request:**

- Path Parameters: `uid` - The unique identifier of the user, `token` - The token sent to the user's email.

**Response:**

- `200 OK` - Email has been verified.
- `400 Bad Request` - The provided uid or token is invalid.

### 3. Sign In

**Endpoint:** `POST /authentication/api/signin/`

**Description:** Log in to the application. The user must have verified their email to use this endpoint.

**Request:**

- Headers: `Content-Type: application/json`
- Body: `{ "username": "string", "password": "string" }`

**Response:**

- `200 OK` - User authenticated with return of corresponding message.
- `400 Bad Request` - The provided credentials are incorrect or user didn't verified his email.

### 4. Sign Out

**Endpoint:** `GET /authentication/api/signout/`

**Description:** Log out from the website.

**Request:**

- Headers: `Cookie: SessionID=<session_id>`
- Body: Empty

**Response:**

- `204 No Content` - User logged out.
- `403 Forbidden` - The provided session ID is invalid or has expired.

### 5. Generate Quiz

**Endpoint:** `POST /quiz/`

**Description:** Generate a quiz based on the provided text.

**Request:**

- Headers: `Content-Type: application/json`, `Cookie: SessionID=<session_id>`
- Body: `{ "text": "string" }`

**Response:**

Returns the generated quiz in JSON format.

- `400 Bad Request` - The request body is invalid or incomplete.
- `403 Fobidden` - The session ID is invalid or has expired.

### 6. Generate Summary

**Endpoint:** `POST /summary/`

**Description:** Generate a summary based on the provided query.

**Request:**

- Headers: `Content-Type: application/json`, `Cookie: SessionID=<session_id>`
- Body: `{ "query": "string" }`

**Response:**

Returns the generated summary in JSON format.

- `400 Bad Request` - The request body is invalid or incomplete.
- `403 Fobidden` - The session ID is invalid or has expired.

## Contributing

Thank you for considering contributing to our project! To contribute, follow these steps:

1. **Fork** the repository to your GitHub account.
2. **Create** a new branch from `main` for your feature or fix:
   ```bash
   git checkout -b feature/your-feature
3. Commit your changes to the branch:
    ```bash
    git commit -m 'Add some feature'

4. Push your branch to your fork:
    ```bash
     git push origin feature/your-feature
5. **Open a pull request (PR) on GitHub:**
    - **Title**: Provide a clear and descriptive title for your pull request.
    - **Description**: Include a detailed description of the changes you have made and why they are valuable.
    - **Related Issues**: Mention any related issues by using keywords like `Fixes #issue-number` in the PR description.
    
    Your pull request will undergo review, where feedback may be provided for further improvements. Thank you for your contribution!

## Features  

List of the main features of the project.

- **Quiz Generation**: Automatically create quizzes from student notes to help reinforce knowledge and improve retention.
- **Note Summarization**: Compress lengthy notes into concise summaries, making it easier to review key concepts.

## License

This project is licensed under the GNU General Public License version 3.0 (GPL-3.0).

See the [LICENSE](LICENSE) file for details.


## Acknowledgements

We would like to thank our beta testers for their feedback and suggestions:
 
- Dias Usenov
- Arsenii Pavlov
