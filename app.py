import os
from datetime import datetime
import requests
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from functools import wraps
from models import Actor, Movie

db = SQLAlchemy()

def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth_header = request.headers.get('Authorization', None)
            if not auth_header:
                return jsonify({'error': 'Authorization header is missing'}), 401

            parts = auth_header.split()
            if parts[0].lower() != 'bearer':
                return jsonify({'error': 'Authorization header must start with Bearer'}), 401
            elif len(parts) == 1:
                return jsonify({'error': 'Token not found'}), 401
            elif len(parts) > 2:
                return jsonify({'error': 'Authorization header must be Bearer token'}), 401

            token = parts[1]

            try:
                response = requests.get(f'https://{os.getenv("AUTH0_DOMAIN")}/userinfo', headers={'Authorization': f'Bearer {token}'})
                response.raise_for_status()
                user_info = response.json()
                user_permissions = user_info.get('permissions', [])

                if permission not in user_permissions:
                    return jsonify({'error': 'Permission not found'}), 403
            except requests.exceptions.HTTPError as err:
                return jsonify({'error': 'Invalid token'}), 401
            except requests.exceptions.RequestException as e:
                return jsonify({'error': 'Invalid token'}), 401

            return f(*args, **kwargs)
        return decorated_function
    return requires_auth_decorator

def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///casting_agency.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['AUTH0_DOMAIN'] = os.getenv('AUTH0_DOMAIN')
    app.config['API_KEY'] = os.getenv('API_KEY')

    db.init_app(app)

    with app.app_context():
        db.create_all()

    @app.route('/actors', methods=['GET'])
    def get_actors():
        actors = Actor.query.all()
        return jsonify([actor.to_dict() for actor in actors])

    @app.route('/movies', methods=['GET'])
    def get_movies():
        movies = Movie.query.all()
        return jsonify([movie.to_dict() for movie in movies])

    @app.route('/actors', methods=['POST'])
    @requires_auth('create:actor')
    def add_actor():
        data = request.get_json()
        actor = Actor(name=data['name'], age=data['age'], gender=data['gender'])
        db.session.add(actor)
        db.session.commit()
        return jsonify(actor.to_dict()), 201

    @app.route('/movies', methods=['POST'])
    @requires_auth('create:movie')
    def add_movie():
        data = request.get_json()
        movie = Movie(title=data['title'], release_date=datetime.strptime(data['release_date'], '%Y-%m-%d'))
        db.session.add(movie)
        db.session.commit()
        return jsonify(movie.to_dict()), 201

    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(id):
        actor = Actor.query.get_or_404(id)
        db.session.delete(actor)
        db.session.commit()
        return jsonify({'success': True}), 200

    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(id):
        movie = Movie.query.get_or_404(id)
        db.session.delete(movie)
        db.session.commit()
        return jsonify({'success': True}), 200

    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('update:actor')
    def update_actor(id):
        data = request.get_json()
        actor = Actor.query.get_or_404(id)
        if 'name' in data:
            actor.name = data['name']
        if 'age' in data:
            actor.age = data['age']
        if 'gender' in data:
            actor.gender = data['gender']
        db.session.commit()
        return jsonify(actor.to_dict()), 200

    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('update:movie')
    def update_movie(id):
        data = request.get_json()
        movie = Movie.query.get_or_404(id)
        if 'title' in data:
            movie.title = data['title']
        if 'release_date' in data:
            movie.release_date = datetime.strptime(data['release_date'], '%Y-%m-%d')
        db.session.commit()
        return jsonify(movie.to_dict()), 200

    @app.errorhandler(400)
    def bad_request_error(error):
        return jsonify({'error': 'Bad Request', 'message': str(error)}), 400

    @app.errorhandler(401)
    def unauthorized_error(error):
        return jsonify({'error': 'Unauthorized', 'message': str(error)}), 401

    @app.errorhandler(403)
    def forbidden_error(error):
        return jsonify({'error': 'Forbidden', 'message': str(error)}), 403

    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({'error': 'Not Found', 'message': str(error)}), 404

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
