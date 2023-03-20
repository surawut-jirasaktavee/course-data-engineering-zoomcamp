import faust
from settings import TaxiRide_Schema


app = faust.App("pu_location_count", broker="kafka://localhost:9092")
topic = app.topic("rides_json", value_type=TaxiRide_Schema)

vendor_rides = app.Table("pu_location_count", default=int)


@app.agent(topic)
async def process(stream):
    async for event in stream.group_by(TaxiRide_Schema.pu_location_id):
        vendor_rides[event.pu_location_id] += 1
        print(vendor_rides.items())


if __name__ == "__main__":
    app.main()
