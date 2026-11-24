"""Catalogo oficial de eventos de dominio de UrbanMove."""

from enum import StrEnum


class EventType(StrEnum):
    """Eventos de dominio emitidos al bus SNS/SQS.

    Incluye los 13 eventos obligatorios del enunciado mas 3 eventos
    operacionales adicionales para incidencias, mantenimiento y bajas.
    """

    # --- 13 eventos obligatorios del enunciado ---
    USER_REGISTERED = "UserRegistered"
    VEHICLE_PURCHASED = "VehiclePurchased"
    VEHICLE_RESERVED = "VehicleReserved"
    RESERVATION_CANCELLED = "ReservationCancelled"
    RESERVATION_EXPIRED = "ReservationExpired"
    RIDE_STARTED = "RideStarted"
    RIDE_FINISHED = "RideFinished"
    VEHICLE_BATTERY_LOW = "VehicleBatteryLow"
    VEHICLE_WITHDRAWN_FOR_MAINTENANCE = "VehicleWithdrawnForMaintenance"
    VEHICLE_RETURNED_TO_SERVICE = "VehicleReturnedToService"
    DEMAND_HOTSPOT_DETECTED = "DemandHotspotDetected"
    RELOCATION_ORDER_CREATED = "RelocationOrderCreated"
    RELOCATION_ORDER_COMPLETED = "RelocationOrderCompleted"

    # --- 3 eventos operacionales adicionales ---
    MAINTENANCE_ORDER_CREATED = "MaintenanceOrderCreated"
    INCIDENT_REPORTED = "IncidentReported"
    VEHICLE_RETIRED = "VehicleRetired"
