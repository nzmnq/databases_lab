from flask import Flask
from .retail_chain_route import retail_chains_bp
from .parking_station_route import parking_stations_bp
from .parking_zone_route import parking_zones_bp
from .spot_type_route import spot_types_bp
from .parking_spot_route import parking_spots_bp
from .client_route import clients_bp
from .client_individual_route import client_individuals_bp
from .client_enterprise_route import client_enterprises_bp
from .regular_card_route import regular_cards_bp
from .vehicle_route import vehicles_bp
from .parking_reservation_route import parking_reservations_bp
from .parking_session_route import parking_sessions_bp
from .parking_ticket_route import parking_tickets_bp
from .station_maintenance_route import station_maintenances_bp
from .reservation_delete_log_route import reservation_delete_logs_bp
from .stored_programs_route import stored_programs_bp

def register_routes(app: Flask):
    app.register_blueprint(retail_chains_bp)
    app.register_blueprint(parking_stations_bp)
    app.register_blueprint(parking_zones_bp)
    app.register_blueprint(spot_types_bp)
    app.register_blueprint(parking_spots_bp)
    app.register_blueprint(clients_bp)
    app.register_blueprint(client_individuals_bp)
    app.register_blueprint(client_enterprises_bp)
    app.register_blueprint(regular_cards_bp)
    app.register_blueprint(vehicles_bp)
    app.register_blueprint(parking_reservations_bp)
    app.register_blueprint(parking_sessions_bp)
    app.register_blueprint(parking_tickets_bp)
    app.register_blueprint(station_maintenances_bp)
    app.register_blueprint(reservation_delete_logs_bp)
    app.register_blueprint(stored_programs_bp)

__all__ = [
    'register_routes',
    'retail_chains_bp',
    'parking_stations_bp',
    'parking_zones_bp',
    'spot_types_bp',
    'parking_spots_bp',
    'clients_bp',
    'client_individuals_bp',
    'client_enterprises_bp',
    'regular_cards_bp',
    'vehicles_bp',
    'parking_reservations_bp',
    'parking_sessions_bp',
    'parking_tickets_bp',
    'station_maintenances_bp',
    'reservation_delete_logs_bp',
    'stored_programs_bp',
]
