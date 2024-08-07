# Casting Agency

## Motivation
The Casting Agency project simplifies and streamlines the process of managing movies and actors.

## API URL
- **API URL:** [your-deployed-url]

## Project Dependencies
- Flask
- Flask-SQLAlchemy
- Flask-Cors
- requests


## Setup Instructions
1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd <repo-directory>

## run the app
pip install -r requirements.txt

export FLASK_APP=app.py
export FLASK_ENV=development  # Enables debug mode
flask run


# Roles and Permissions

 - Casting Assistant
    - Permissions:
        read:actors
        read:movies
    - Capabilities:
        View: Access to view the list of actors and movies.
        Endpoints Accessible:
            GET /actors - Retrieve all actors.
            GET /movies - Retrieve all movies.

 - Casting Director
    - Permissions:
        create:actor
        delete:actor
        update:actor
        create:movie
        delete:movie
        update:movie
        read:actors
        read:movies

    - Capabilities:
        View: Access to view the list of actors and movies (same as Casting Assistant).
        Add: Create new actors and movies.
        Delete: Remove existing actors and movies.
        Modify: Update information for actors and movies.
        Endpoints Accessible:
            GET /actors - Retrieve all actors.
            GET /movies - Retrieve all movies.
            POST /actors - Add a new actor.
            POST /movies - Add a new movie.
            PATCH /actors/<id> - Update an existing actor.
            PATCH /movies/<id> - Update an existing movie.
            DELETE /actors/<id> - Delete an actor.
            DELETE /movies/<id> - Delete a movie.

   - Executive Producer
         same as Casting Director.

## API Endpoints
 - Actors:
    GET /actors: Retrieve a list of all actors.
    POST /actors: Add a new actor (requires create:actor permission).
    DELETE /actors/<id>: Delete an actor by ID (requires delete:actor permission).
    PATCH /actors/<id>: Update an actor by ID (requires update:actor permission).

 - Movies
    GET /movies: Retrieve a list of all movies.
    POST /movies: Add a new movie (requires create:movie permission).
    DELETE /movies/<id>: Delete a movie by ID (requires delete:movie permission).
    PATCH /movies/<id>: Update a movie by ID (requires update:movie permission).

## Error Handling
    - 400 Bad Request: 
        The request was invalid or cannot be processed.
    - 401 Unauthorized: 
        Authentication is required or the token is invalid/expired.
    - 403 Forbidden: 
        The authenticated user does not have the required permissions.
    - 404 Not Found: 
        The requested resource was not found.
# Capstone
