import json

def get_data():
    with open("my_twitter_friend_data.json", "r") as read_file:
        received_data = json.load(read_file)
        return received_data

def update_data(updated_data):
    with open("my_twitter_friend_data.json", "w") as write_file:
        json.dump(updated_data, write_file)

data = get_data()
print(json.dumps(data, sort_keys=True, indent=4))


# alter data here
data["compliments"] = "empty"
data["encouragement"] = "empty"
data["fun_stories"] = "empty"

data["replies"] = [
    "Hey Buddy!!!",
    "What's up, friend!!!",
    "I miss you, pal!!!",
    "High five!!!",
    "You get down with your bad self!!!",
    "Boom, roasted!",
    "Yeet!",
    "I know, right!",
    "I heard that!",
    "That's how it's done!!!",
    "Ain't that the truth!",
    "This is AWESOME!",
    "I live for your tweets!!!",
    "Better than a jab in the eye...!",
    "Awesome sauce!",
    "Cool beans!",
    "YOLO!",


]
# ######################################################
update_data(data)