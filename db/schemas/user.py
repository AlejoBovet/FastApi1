def user_schema(user) -> dict:
    return {"id": str(user["_id"]),
            "name":user["name"],
            "last_name":user["last_name"],
            "age":user["age"],
            "email":user["email"],
            "password":user["password"]}


def users_schema(users) -> list:
    return [user_schema(user) for user in users]