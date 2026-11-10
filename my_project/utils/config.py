import os
import yaml

def load_config():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    config_path = os.path.join(base_dir, 'config', 'app.yml')

    config = {}
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f) or {}

    app_cfg = config.get('app', {})
    db_cfg = config.get('database', {})

    user = os.getenv('MYSQL_USER', db_cfg.get('user', 'root'))
    password = os.getenv('MYSQL_PASSWORD', db_cfg.get('password', ''))
    host = os.getenv('MYSQL_HOST', db_cfg.get('host', '127.0.0.1'))
    port = os.getenv('MYSQL_PORT', db_cfg.get('port', 3306))
    name = os.getenv('MYSQL_DB', db_cfg.get('name', 'smart_parking_db'))
    dialect = db_cfg.get('dialect', 'mysql+pymysql')

    use_sqlite = os.getenv('USE_SQLITE', 'false').lower() in ('true', '1', 'yes')
    if use_sqlite:
        db_uri = f"sqlite:///{os.path.join(base_dir, 'smart_parking.db')}"
    elif password:
        db_uri = f"{dialect}://{user}:{password}@{host}:{port}/{name}?charset=utf8mb4"
    else:
        db_uri = f"{dialect}://{user}@{host}:{port}/{name}?charset=utf8mb4"

    return {
        'APP_NAME': app_cfg.get('name', 'Smart Parking App'),
        'HOST': app_cfg.get('host', '127.0.0.1'),
        'PORT': int(app_cfg.get('port', 5000)),
        'DEBUG': app_cfg.get('debug', True),
        'SECRET_KEY': app_cfg.get('secret_key', 'dev-secret-key'),
        'SQLALCHEMY_DATABASE_URI': db_uri,
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SQLALCHEMY_ECHO': db_cfg.get('echo', False),
        'RAW_CONFIG': config
    }
