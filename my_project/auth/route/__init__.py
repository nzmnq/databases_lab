from flask import Flask
from .retail_chain_route import retail_chains_bp
from .parking_station_route import parking_stations_bp

def register_routes(app: Flask):
    app.register_blueprint(retail_chains_bp)
    app.register_blueprint(parking_stations_bp)

__all__ = ['register_routes', 'retail_chains_bp', 'parking_stations_bp']
