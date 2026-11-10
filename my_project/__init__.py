from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from my_project.utils.config import load_config

db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__)

    cfg = load_config()
    app.config.update(cfg)

    if test_config:
        app.config.update(test_config)

    db.init_app(app)

    from my_project.auth.route import register_routes
    register_routes(app)

    @app.route('/', methods=['GET'])
    @app.route('/api', methods=['GET'])
    @app.route('/api/', methods=['GET'])
    def index():
        return jsonify({
            'app': app.config.get('APP_NAME'),
            'status': 'running',
            'message': 'Smart Parking Backend REST API',
            'endpoints': {
                'retail_chains': '/api/retail-chains',
                'parking_stations': '/api/parking-stations',
                'health': '/api/health'
            }
        }), 200

    @app.route('/api/health', methods=['GET'])
    def health_check():
        return jsonify({
            'status': 'healthy',
            'app': app.config.get('APP_NAME'),
            'message': 'Smart Parking Backend is up and running'
        }), 200

    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({'error': 'Not Found', 'message': str(error)}), 404

    @app.errorhandler(400)
    def bad_request_error(error):
        return jsonify({'error': 'Bad Request', 'message': str(error)}), 400

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal Server Error', 'message': str(error)}), 500

    return app
