"""GraphQL API schema and resolvers."""
import graphene
from graphene import ObjectType, String, Int, Float, DateTime, List
from ..services.trip_service import TripService

class TaxiTripType(ObjectType):
    """GraphQL type for taxi trips."""
    id = Int()
    vendor_id = String()
    pickup_datetime = DateTime()
    dropoff_datetime = DateTime()
    passenger_count = Int()
    pickup_longitude = Float()
    pickup_latitude = Float()
    dropoff_longitude = Float()
    dropoff_latitude = Float()
    trip_duration = Int()

class Query(ObjectType):
    """GraphQL query definitions."""
    trips = List(TaxiTripType, 
                start_date=DateTime(), 
                end_date=DateTime(),
                limit=Int(default_value=100))
    
    def resolve_trips(self, info, start_date=None, end_date=None, limit=100):
        service = TripService(info.context["db"])
        return service.get_trips(start_date, end_date, limit)

schema = graphene.Schema(query=Query)