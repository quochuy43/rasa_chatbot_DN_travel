import json 

with open("D:/PYTHON/AI/RASA/started/my_first_chatbot/actions/data/foods.json", "r", encoding="utf-8") as f:
    data = json.load(f)

with open("D:/PYTHON/AI/RASA/started/my_first_chatbot/actions/data/lookups/food_name.txt", "w", encoding="utf-8") as f:
    for item in data:
        f.write(item["name"] + "\n")

# Tao file food_name.txt