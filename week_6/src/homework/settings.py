import faust


class TaxiRide_Schema(faust.Record, validation=True):
    pu_location_id: str
