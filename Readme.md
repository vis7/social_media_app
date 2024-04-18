# Social Media App

## Overview

Social Media app with basic authentication and friend request feature.

## Features

List of key features provided by Social Media App.

### User Login/Signup
- Users can login with their email and password (email should be case insensitive).
- Users can signup with their email only (no OTP verification required, valid email format is sufficient).

### Search
- User can serch other Users (using exact email or part of username)

### Friend Request
- send/accept/reject friend requests.
- list friends (list of users who have accepted friend request)
- List pending friend requests (received friend request).
- Users cannot send more than 3 friend requests within a minute.

## Requirements

- Python (>= 3.10)
- Django (>= 5.0.4)
- Django Rest Framework (>= 3.15.1)

Other dependency can be found in requirements.txt

## Setup

Instructions for setting up and Social Media App. It include both the setup with and without Docker.

### Setup Without Docker

1. **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd <project_directory>
    ```

2. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Apply migrations:**

    ```bash
    python manage.py migrate
    ```

4. **Run the development server:**

    ```bash
    python manage.py runserver
    ```


### Setup With Docker

1. **Clone the repository:**

    ```bash
    git clone <repository_url>
    cd <project_directory>
    ```

2. **Build the Docker image:**

    ```bash
    docker build -t django-app .
    ```

3. **Run the Docker container:**

    ```bash
    docker run -p 8000:8000 django-app
    ```


## Configuration

Add .env file along with below settings and add it parallel to settins.py
```
SECRET_KEY='django-insecure-7sxch!f7g%nuf^yrvz5&1fl32++w!8o1*3cu3t8+hl+$z)e=)c'
DEBUG=True
```

## Usage

Import Postman Collection and Enviornment from `postman` folder. Now you are ready to run APIs.


## License

MIT License

