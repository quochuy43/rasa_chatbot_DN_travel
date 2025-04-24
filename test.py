import json 

with open("D:/VKU/Chuyên đề/rasa_chatbot_DN_travel/actions/data/tours.json", "r", encoding="utf-8") as f:
    data = json.load(f)

with open("D:/VKU/Chuyên đề/rasa_chatbot_DN_travel/data/lookups/tour_name.txt", "w", encoding="utf-8") as f:
    for item in data:
        f.write(item["name"] + "\n")

# Tao file food_name.txt