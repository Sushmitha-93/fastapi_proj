from app.schemas.usermood_schema import CreateMoodSchema, MoodSchemaOut
from app.models.usermood_model import UserMood
from app.models.userModel import User


class UserMoodService:
    @staticmethod
    async def create_user_mood(user: User, data: CreateMoodSchema):
        new_usermood = UserMood(
            user=user,
            mood=data.mood,
            location=data.location
        )
        await new_usermood.insert()
        return MoodSchemaOut(
            mood=new_usermood.mood,
            location=new_usermood.location,
            date=new_usermood.date,
            userid=new_usermood.user.userid
        )

    @staticmethod
    async def get_closest_happy_place(user: User, lat: str, long: str):
        locations = await UserMood.find((UserMood.user.id == user.id), {"location": {"$ne": [float(lat), float(long)]}}).sort(-UserMood.date).aggregate([{
            "$group": {
                "_id": "$location",
                "latest_mood": {"$first": "$mood"},
                "latest_date": {"$first": "$date"}
            }
        }, {
            "$match": {
                "latest_mood": "happy"
            }
        },
            {
            "$project": {
                "_id": 0,
                "location": "$_id",
                "last_visited": "$latest_date"
            }
        }]).to_list()
        return locations

    @staticmethod
    async def get_user_mood_frequency(user: User):
        mood_frequency = await UserMood.find(UserMood.user.id == user.id).aggregate([{
            "$group": {
                "_id": "$mood",
                "count": {"$sum": 1}
            }
        }, {
            "$project": {
                "_id": 0,
                "mood": "$_id",
                "count": "$count"
            }
        }]).to_list()
        return mood_frequency
