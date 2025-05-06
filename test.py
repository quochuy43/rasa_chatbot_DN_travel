import json
import re
import json 

# file_path = "D:/PYTHON/AI/RASA/started/my_first_chatbot - Copy/actions/data/transportation.json"

# # with open("D:/VKU/Chuyên đề/rasa_chatbot_DN_travel/actions/data/travel_expenses.json", "r", encoding="utf-8") as f:
# with open("cleaned_travel.json", "r", encoding="utf-8") as f:
#     data = json.load(f)

# unique_compositions = set()

# for item in data:
#     unique_compositions.add(str(item["group composition"]))

# with open("D:/VKU/Chuyên đề/rasa_chatbot_DN_travel/data/lookups/expenses_composition.txt", "w", encoding="utf-8") as f:
#     for composition in unique_compositions:
#         f.write(composition + "\n")


def remove_parentheses_and_commas_from_group_composition(data):
    for entry in data:
        # Loại bỏ các dấu ngoặc đơn ( và ) và dấu phẩy , trong 'group composition'
        entry["group composition"] = re.sub(
            r'[(),]', '', entry["group composition"]).strip()
    return data


def process_travel_data(input_file, output_file):
    # Đọc dữ liệu từ file JSON
    with open(input_file, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Xử lý dữ liệu
    cleaned_data = remove_parentheses_and_commas_from_group_composition(data)

    # Ghi kết quả vào file mới
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(cleaned_data, file, ensure_ascii=False, indent=4)


# Đọc và xử lý file travel.json
process_travel_data(
    'D:/VKU/Chuyên đề/rasa_chatbot_DN_travel/actions/data/travel_expenses.json', 'cleaned_travel.json')

print("Dữ liệu đã được xử lý và lưu vào file 'cleaned_travel.json'.")



# with open(file_path, "r", encoding="utf-8") as f:
#     data = json.load(f)

# for item in data:
#     if "amenities" in item:
#         del item["amenities"]

# with open(file_path, "w", encoding="utf-8") as f:
#     json.dump(data, f, indent=4, ensure_ascii=False)


# with open(file_path, "r", encoding="utf-8") as f:
#     data = json.load(f)

# with open("D:/PYTHON/AI/RASA/started/my_first_chatbot - Copy/data/lookups/transportation.txt", "w", encoding="utf-8") as f:
#     for item in data:
#         f.write(item["name"] + "\n")