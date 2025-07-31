# FastAPI Portfolio Project

This project is a FastAPI-based web application designed to manage a personal portfolio, including features for adding, updating, and retrieving educational experiences, certifications, and skills. **Now with JWT-based authentication!**

## 🔐 New! JWT Authentication

This project now includes a complete JWT (JSON Web Token) authentication system:

- **Secure Login**: Username/password authentication with JWT tokens
- **Protected Endpoints**: All CRUD operations require valid JWT tokens  
- **Token Expiration**: Configurable token expiration (default: 30 minutes)
- **Modern Security**: bcrypt password hashing, HS256 token signing

**Quick Start:**
```bash
# Start the server
python start_server.py

# Login to get JWT token
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# Use token for protected endpoints
curl -X GET "http://localhost:8000/auth/protected" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

📚 **See [JWT_AUTH.md](JWT_AUTH.md) for complete authentication documentation.**

## Table of Contents

- [🔐 JWT Authentication](#-new-jwt-authentication)
- [Features](#features)
- [Technologies](#technologies)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Models](#models)
- [Testing](#testing)
- [Environment Variables](#environment-variables)
- [Contributing](#contributing)
- [License](#license)

## Features

- **JWT Authentication**: Secure token-based authentication system
- Create, read, update, and delete educational experiences, certifications, and skills.
- Secure API access using API keys.
- Unit tests for ensuring application reliability.

## Technologies

- **Python** 3.12
- **FastAPI** for the web framework
- **MongoDB** for the database
- **Pydantic** for data validation
- **Poetry** for dependency management
- **pytest** for testing

## Installation

1. Clone the repository:

  ```bash
  git clone https://github.com/your_username/your_repo_name.git
  cd your_repo_name
  ```

2. Install dependencies using Poetry:

  ```bash
  poetry install
  ```

3. Set up your environment variables. You can create a `.env` file in the root directory with the following content:

  ```plaintext
  API_KEY=your_api_key
  ```

## Usage

To run the FastAPI application, use:

```bash
poetry run uvicorn main:app --reload
```

The application will be available at `http://127.0.0.1:8000`.

You can also access the interactive API documentation at `http://127.0.0.1:8000/docs`.

## API Endpoints

Here are some of the key API endpoints:

- **Create Person**: `POST /person/create`
- **Read Person**: `GET /person/read`
- **Update Person**: `PUT /person/update/{id}`
- **Delete Person**: `DELETE /person/delete/{id}`

For detailed information about each endpoint, refer to the [API documentation](http://127.0.0.1:8000/docs).

## Models

The application uses Pydantic models for data validation. Here are some of the key models:

- **Person**:
  ```python
  from pydantic import BaseModel

  class Person(BaseModel):
    name: str
    birthday: str
    position: str
    contact: Contact
    description: str
  ```

- **Education**:
  ```python
  from pydantic import BaseModel

  class Education(BaseModel):
    institution : str
    degree : str
    start : str
    end : str | None = None
    desc : str
  ```

- **Certificate**:
  ```python
  from pydantic import BaseModel

  class Certificate(BaseModel):
    name: str
    date: str
    desc: str
  ```

- **Skill**:
  ```python
  from pydantic import BaseModel

  class Skill(BaseModel):
    name: str
    level: SkillLevel
    tag: Tag
    level_name: str | None = None
  ```

## Testing

To run the tests, use:

```bash
poetry run pytest
```

Make sure your MongoDB service is running before executing the tests.

## Environment Variables

The following environment variables are required:

- `API_KEY`: Your API key for accessing the endpoints.

## Contributing

Contributions are welcome! If you'd like to contribute, please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

### Instructions for Customization
- Replace `your_username` and `your_repo_name` with your actual GitHub username and repository name.
- Add any additional features or API endpoints that are relevant to your project.
- Modify any sections to better fit your project's structure or requirements.

Feel free to let me know if you need any additional changes or specific sections! 🥰
