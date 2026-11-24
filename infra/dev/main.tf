module "messaging" {
  source = "../modules/messaging"

  environment       = "dev"
  topic_name        = "urbanmove-events"
  max_receive_count = 3

  consumers = {
    history = {
      event_types = [] # Recibe todos los eventos del sistema para auditoria e historial
    }
    analytics-ingest = {
      event_types = [] # Recibe todos los eventos para volcarlos a S3 raw/
    }
    maintenance-detector = {
      event_types = [
        "RideFinished",
        "VehicleBatteryLow",
        "IncidentReported",
      ]
    }
    availability-sync = {
      event_types = [
        "VehiclePurchased",
        "VehicleReserved",
        "ReservationCancelled",
        "ReservationExpired",
        "RideStarted",
        "RideFinished",
        "VehicleWithdrawnForMaintenance",
        "VehicleReturnedToService",
        "VehicleRetired",
      ]
    }
  }
}

module "storage" {
  source = "../modules/storage"

  environment          = "dev"
  datalake_bucket_name = var.datalake_bucket_name
  force_destroy        = true
}
