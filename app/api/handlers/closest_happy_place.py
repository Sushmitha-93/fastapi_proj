from fastapi import APIRouter, Depends
from app.models.userModel import User
from app.api.auth.user_deps import get_current_user
from app.services.usermood_service import UserMoodService
from app.core.config import settings
import numpy as np
from scipy.spatial import KDTree
import googlemaps


closest_happy_place = APIRouter()
gmaps = googlemaps.Client(settings.MAPS_API_KEY)


def get_distance(location1: tuple[float, float], location2: tuple[float, float]) -> float:
    # Calculate the distance between the two locations
    print(location1, location2)
    distance = gmaps.distance_matrix(location1, location2)[
        'rows'][0]['elements'][0]['distance']['value']
    distance_miles = distance * 0.000621371  # Convert meters to miles
    return distance_miles


def get_nearest_location(user_location, locations) -> tuple[float, float]:
    # Create a KDTree from the list of locations
    tree = KDTree(locations)
    # Query KDTree
    distance, index = tree.query(user_location)
    nearest_location = locations[index]
    return nearest_location.tolist()


def get_nearby_place_placeid(latitude: float, longitude: float) -> str:
    places_result = gmaps.places_nearby(
        location=(latitude, longitude),
        radius=20,  # Adjust the radius as needed
        type='point_of_interest'  # Specify the type of place to search for
    )
    return places_result['results'][0]['place_id'] if places_result else None


def reverse_geocode(latitude: float, longitude: float, result_type: str) -> str:
    # Perform a reverse geocoding request to get the location details
    reverse_geocode_result = gmaps.reverse_geocode(
        (latitude, longitude), result_type=result_type)

    return reverse_geocode_result[0]['place_id'] if reverse_geocode_result else None


def get_place_details(latitude: float, longitude: float,):

    place_id = reverse_geocode(latitude, longitude, 'point_of_interest')
    if (place_id is None):
        place_id = get_nearby_place_placeid(latitude, longitude)
    elif (place_id is None):
        place_id = reverse_geocode(latitude, longitude)

    place_details = gmaps.place(place_id=place_id)

    return {'name': place_details['result']['name'], 'address': place_details['result']['formatted_address']}


@closest_happy_place.get('/{lat}/{long}', summary="Returns the closest happy place to the user")
async def get_closest_happy_place(lat: str, long: str, current_user: User = Depends(get_current_user)):
    query_response = await UserMoodService.get_closest_happy_place(user=current_user, lat=lat, long=long)
    locations = np.array([item["location"] for item in query_response])

    user_location = [float(lat), float(long)]

    nearest_location = get_nearest_location(user_location, locations)

    distance = get_distance(tuple(user_location), tuple(nearest_location))

    place_details = get_place_details(nearest_location[0], nearest_location[1])

    return ({"nearestLocation": nearest_location,
             "distance": distance,
             "name": place_details['name'],
             "address": place_details['address']})
