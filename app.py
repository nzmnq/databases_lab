import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from my_project import create_app, db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            app.logger.warning(f"Could not initialize tables automatically: {e}")

    host = app.config.get('HOST', '127.0.0.1')
    port = app.config.get('PORT', 5000)
    debug = app.config.get('DEBUG', True)

    print(f" * Starting {app.config.get('APP_NAME')} on http://{host}:{port}")
    app.run(host=host, port=port, debug=debug)
