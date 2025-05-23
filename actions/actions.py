from typing import Any, Text, Dict, List
import json, re
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from rasa_sdk.events import SlotSet


class ActionProvideFoodInfo(Action):

    # Trả về tên của action, dùng tên này để gọi đúng action tương ứng khi dự đoán
    # Ni là type hint -> hàm sẽ trả về 1 giá trị kiểu text
    def name(self) -> Text:
        return "action_provide_food_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        food_name = next(tracker.get_latest_entity_values("food_name"), None)
        if not food_name:
            dispatcher.utter_message(
                text="Bạn muốn hỏi thông tin về món gì vậy?")
            return []

        # Load data tu JSON
        with open("actions/data/foods.json", "r", encoding="utf-8") as f:
            foods = json.load(f)

        for food in foods:
            if food_name.lower().strip() in food["name"].lower():
                msg = f"🍽 {food['name']}\n"
                msg += f"{food['description']}. Địa chỉ nằm ở: {', '.join(food['addresses'])}. Giá trung bình ở đà nẵng là {food['average_price']}k bạn nhé💰!"
                dispatcher.utter_message(text=msg)
                return []

        dispatcher.utter_message(
            text=f"Xin lỗi, mình chưa có thông tin về món {food_name}. Mình sẽ gắng cập nhật thông tin để giải đáp thắc mắc cho bạn nhé!")
        return []


class ActionListManyFoods(Action):
    def name(self) -> Text:
        return "action_list_many_foods"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        shown_foods_indices = tracker.get_slot("shown_foods_indices")

        with open("actions/data/foods.json", "r", encoding="utf-8") as f:
            foods = json.load(f)

        if not shown_foods_indices:
            shown_foods_indices = []

        foods_per_page = 7

        if len(shown_foods_indices) >= len(foods):
            dispatcher.utter_message(
                text="Mình đã giới thiệu hết các món ăn đặc sản của Đà Nẵng rồi. Bạn muốn biết thêm thông tin gì khác không?")
            return [SlotSet("shown_foods_indices", [])]  # Reset lại slot

        remaining_indices = [i for i in range(
            len(foods)) if i not in shown_foods_indices]
        num_to_show = min(foods_per_page, len(remaining_indices))
        indices_to_show = remaining_indices[:num_to_show]

        # Update danh sách các món đã hiển thị
        shown_foods_indices.extend(indices_to_show)

        response = "\n"
        for idx in indices_to_show:
            response += f"{foods[idx]['name']}; "
        response += "\nBạn muốn biết thêm thông tin chi tiết về món nào? Hãy nhắn tên món ăn để mình giới thiệu nhé!"

        dispatcher.utter_message(text=response)

        # Lưu lại danh sách các món đã hiển thị
        return [SlotSet("shown_foods_indices", shown_foods_indices)]


class ActionProvideFoodPrice(Action):
    def name(self) -> Text:
        return "action_provide_food_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        food_name = next(tracker.get_latest_entity_values("food_name"), None)
        if not food_name:
            dispatcher.utter_message(text="Bạn muốn hỏi giá món gì vậy?")
            return []

        with open("actions/data/foods.json", "r", encoding="utf-8") as f:
            foods = json.load(f)

        for food in foods:
            if food_name.lower().strip() in food["name"].lower():
                dispatcher.utter_message(
                    text=f"💰 Món {food['name']} có giá trung bình khoảng {food['average_price']}k bạn nhé!")
                return []

        dispatcher.utter_message(
            text=f"Xin lỗi, mình chưa có thông tin giá của món {food_name}.")
        return []


class ActionProvideFoodLocation(Action):

    def name(self) -> Text:
        return "action_provide_food_location"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        food_name = next(tracker.get_latest_entity_values("food_name"), None)
        if not food_name:
            dispatcher.utter_message(
                text="Bạn muốn tìm địa điểm của món nào vậy?")
            return []

        with open("actions/data/foods.json", "r", encoding="utf-8") as f:
            foods = json.load(f)

        for food in foods:
            if food_name.lower().strip() in food["name"].lower():
                dispatcher.utter_message(
                    text=f"📍Bạn có thể thưởng thức {food['name']} tại: {', '.join(food['addresses'])}.")
                return []

        dispatcher.utter_message(
            text=f"Xin lỗi, mình chưa biết địa điểm bán món {food_name} rồi :(")
        return []


class ActionProvideHotelInfo(Action):

    def name(self) -> Text:
        return "action_provide_hotel_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        hotel_name = next(tracker.get_latest_entity_values("hotel_name"), None)
        if not hotel_name:
            dispatcher.utter_message(
                text="Bạn muốn hỏi thông tin về khách sạn nào vậy?")
            return []

        with open("actions/data/hotels.json", "r", encoding="utf-8") as f:
            hotels = json.load(f)

        for hotel in hotels:
            if hotel_name.lower().strip() in hotel["name"].lower():
                msg = f"🏨 {hotel['name']}\n"
                msg += f"{hotel['description']}. \nĐịa chỉ nằm ở: {hotel['address']}. \nĐược đánh giá {hotel['rated']} sao và có giá thấp nhất ở đà nẵng là {hotel['cheapest_price']}k/đêm bạn nhé💰!"
                dispatcher.utter_message(text=msg)
                return []

        dispatcher.utter_message(
            text=f"Xin lỗi, mình chưa có thông tin về khách sạn {hotel_name}. Mình sẽ gắng cập nhật thông tin để giải đáp thắc mắc cho bạn nhé!")
        return []


class ActionListManyHotels(Action):
    def name(self) -> Text:
        return "action_list_many_hotels"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        shown_hotels_indices = tracker.get_slot("shown_hotels_indices")

        with open("actions/data/hotels.json", "r", encoding="utf-8") as f:
            hotels = json.load(f)

        if not shown_hotels_indices:
            shown_hotels_indices = []

        hotels_per_page = 7

        if len(shown_hotels_indices) >= len(hotels):
            dispatcher.utter_message(
                text="Mình đã giới thiệu hết các khách sạn nổi tiếng của Đà Nẵng rồi. Bạn muốn biết thêm thông tin gì khác không?")
            return [SlotSet("shown_hotels_indices", [])]  # Reset lại slot

        remaining_indices = [i for i in range(
            len(hotels)) if i not in shown_hotels_indices]
        num_to_show = min(hotels_per_page, len(remaining_indices))
        indices_to_show = remaining_indices[:num_to_show]

        # Update danh sách các khách sạn đã hiển thị
        shown_hotels_indices.extend(indices_to_show)

        response = "\n"
        for idx in indices_to_show:
            response += f"{hotels[idx]['name']} - {hotels[idx]['rated']}⭐; "
        response += "\nBạn muốn biết thêm thông tin chi tiết về khách sạn nào? Hãy nhắn tên khách sạn để mình giới thiệu nhé!"

        dispatcher.utter_message(text=response)

        # Lưu lại danh sách các khách sạn đã hiển thị
        return [SlotSet("shown_hotels_indices", shown_hotels_indices)]


class ActionProvideHotelPrice(Action):
    def name(self) -> Text:
        return "action_provide_hotel_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        hotel_name = next(tracker.get_latest_entity_values("hotel_name"), None)
        if not hotel_name:
            dispatcher.utter_message(
                text="Bạn muốn hỏi giá khách sạn nào vậy?")
            return []

        with open("actions/data/hotels.json", "r", encoding="utf-8") as f:
            hotels = json.load(f)

        for hotel in hotels:
            if hotel_name.lower().strip() in hotel["name"].lower():
                dispatcher.utter_message(
                    text=f"💰 Khách sạn {hotel['name']} có giá thấp nhất khoảng {hotel['cheapest_price']}k/đêm bạn nhé!")
                return []

        dispatcher.utter_message(
            text=f"Xin lỗi, mình chưa có thông tin giá của khách sạn {hotel_name}.")
        return []


class ActionProvideHotelLocation(Action):

    def name(self) -> Text:
        return "action_provide_hotel_location"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        hotel_name = next(tracker.get_latest_entity_values("hotel_name"), None)
        if not hotel_name:
            dispatcher.utter_message(
                text="Bạn muốn tìm địa điểm của khách sạn nào vậy?")
            return []

        with open("actions/data/hotels.json", "r", encoding="utf-8") as f:
            hotels = json.load(f)

        for hotel in hotels:
            if hotel_name.lower().strip() in hotel["name"].lower():
                dispatcher.utter_message(
                    text=f"📍Bạn có thể nghỉ ngơi tại {hotel['name']} ở: {hotel['address']}.")
                return []

        dispatcher.utter_message(
            text=f"Xin lỗi, mình chưa biết địa điểm của khách sạn {hotel_name} rồi :(")
        return []


# tours
class ActionProvideTourInfo(Action):
    def name(self) -> Text:
        return "action_provide_tour_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        tour_name = next(tracker.get_latest_entity_values("tour_name"), None)
        if not tour_name:
            dispatcher.utter_message(
                text="Bạn muốn hỏi thông tin về tour nào vậy?")
            return []

        # Load data tu JSON
        with open("actions/data/tours.json", "r", encoding="utf-8") as f:
            tours = json.load(f)

        for tour in tours:
            if tour_name.lower().strip() in tour["name"].lower():
                msg = f"🏖 {tour['name']}\n"
                msg += f"{tour['description']}"
                dispatcher.utter_message(text=msg)
                return []

        dispatcher.utter_message(
            text=f"Xin lỗi, mình chưa có thông tin về tour {tour_name}. Mình sẽ gắng cập nhật thông tin để giải đáp thắc mắc cho bạn nhé!")
        return []


class ActionListManyTours(Action):
    def name(self) -> Text:
        return "action_list_many_tours"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        shown_tours_indices = tracker.get_slot("shown_tours_indices")

        with open("actions/data/tours.json", "r", encoding="utf-8") as f:
            tours = json.load(f)

        if not shown_tours_indices:
            shown_tours_indices = []

        tours_per_page = 7

        if len(shown_tours_indices) >= len(tours):
            dispatcher.utter_message(
                text="Mình đã giới thiệu hết các tour nổi tiếng của Đà Nẵng rồi. Bạn muốn biết thêm thông tin gì khác không?")
            return [SlotSet("shown_tours_indices", [])]

        remaining_indices = [i for i in range(
            len(tours)) if i not in shown_tours_indices]
        num_to_show = min(tours_per_page, len(remaining_indices))
        indices_to_show = remaining_indices[:num_to_show]

        shown_tours_indices.extend(indices_to_show)

        response = "\n"
        for idx in indices_to_show:
            response += f"{tours[idx]['name']}-{tours[idx]['rated']}⭐; "
        response += "\nBạn muốn biết thêm thông tin chi tiết về tour nào? Hãy nhắn tên tour để mình giới thiệu nhé!"

        dispatcher.utter_message(text=response)

        return [SlotSet("shown_tours_indices", shown_tours_indices)]


class ActionProvideTourPrice(Action):
    def name(self) -> Text:
        return "action_provide_tour_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        tour_name = next(tracker.get_latest_entity_values("tour_name"), None)
        if not tour_name:
            dispatcher.utter_message(text="Bạn muốn hỏi giá tour nào vậy?")
            return []

        with open("actions/data/tours.json", "r", encoding="utf-8") as f:
            tours = json.load(f)

        for tour in tours:
            if tour_name.lower().strip() in tour["name"].lower():
                dispatcher.utter_message(
                    text=f"💰 Tour {tour['name']} có giá khoảng {tour['price']}k bạn nhé")
                return []

        dispatcher.utter_message(
            text=f"Xin lỗi, mình chưa có thông tin giá của tour {tour_name}.")
        return []


class ActionProvideTourReview(Action):

    def name(self) -> Text:
        return "action_provide_tour_review"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        tour_name = next(tracker.get_latest_entity_values("tour_name"), None)
        if not tour_name:
            dispatcher.utter_message(
                text="Bạn muốn hỏi đánh giá của tour nào vậy?")
            return []

        with open("actions/data/tours.json", "r", encoding="utf-8") as f:
            tours = json.load(f)

        for tour in tours:
            if tour_name.lower().strip() in tour["name"].lower():
                dispatcher.utter_message(
                    text=f"⭐ Tour {tour['name']} được đánh giá {tour['rated']} sao.\nĐánh giá của khách hàng là: {tour['customer_review']}.")
                return []

        dispatcher.utter_message(
            text=f"Xin lỗi, mình chưa biết đánh giá của tour {tour_name} rồi :(")
        return []


# Transportation
class ActionProvideTransportationInfo(Action):
    def name(self) -> Text:
        return "action_provide_transportation_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        transportation_name = next(
            tracker.get_latest_entity_values("transportation_name"), None)
        if not transportation_name:
            dispatcher.utter_message(
                text="Bạn muốn hỏi thông tin về hãng xe nào vậy?")
            return []

        # Load data tu JSON
        with open("actions/data/transportation.json", "r", encoding="utf-8") as f:
            transportations = json.load(f)

        for transportation in transportations:
            if transportation_name.lower().strip() in transportation["name"].lower():
                msg = f"🏖 {transportation['name']}\n"
                msg += f"{transportation['description']}. Hãng có địa chỉ ở {transportation['office']}. Tuyến đi chính là {transportation['popular_routes'][0]}. Thể loại phổ biến nhất của hãng này là {transportation['type'][0]} Nếu bạn thích, hãy gọi ngay đến hotline {transportation['hotline']}"
                dispatcher.utter_message(text=msg)
                return []

        dispatcher.utter_message(
            text=f"Xin lỗi, mình chưa có thông tin về {transportation_name}. Mình sẽ gắng cập nhật thông tin để giải đáp thắc mắc cho bạn nhé!")
        return []


class ActionListManyTransportations(Action):
    def name(self) -> Text:
        return "action_list_transportation_providers"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        shown_transportation_indices = tracker.get_slot(
            "shown_transportation_indices")

        with open("actions/data/transportation.json", "r", encoding="utf-8") as f:
            transportations = json.load(f)

        if not shown_transportation_indices:
            shown_transportation_indices = []

        transportations_per_page = 3

        if len(shown_transportation_indices) >= len(transportations):
            dispatcher.utter_message(
                text="Mình đã giới thiệu hết các phương tiện nổi tiếng của Đà Nẵng rồi. Bạn muốn biết thêm thông tin gì khác không?")
            return [SlotSet("shown_transportation_indices", [])]

        remaining_indices = [i for i in range(
            len(transportations)) if i not in shown_transportation_indices]
        num_to_show = min(transportations_per_page, len(remaining_indices))
        indices_to_show = remaining_indices[:num_to_show]

        shown_transportation_indices.extend(indices_to_show)

        response = "\n"
        for idx in indices_to_show:
            response += f"{transportations[idx]['name']}-{transportations[idx]['hotline']}; "
        response += "\nBạn muốn biết thêm thông tin chi tiết về phương tiện nào? Hãy nhắn tên phương tiện để mình giới thiệu nhé!"

        dispatcher.utter_message(text=response)

        return [SlotSet("shown_transportation_indices", shown_transportation_indices)]


class ActionProvideTransportationRoutes(Action):
    def name(self) -> Text:
        return "action_provide_transportation_routes"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        transportation_name = next(
            tracker.get_latest_entity_values("transportation_name"), None)
        if not transportation_name:
            dispatcher.utter_message(
                text="Bạn muốn biết các tuyến đường phương của hãng xe nào vậy?")
            return []

        with open("actions/data/transportation.json", "r", encoding="utf-8") as f:
            transportations = json.load(f)

        for transportation in transportations:
            if transportation_name.lower().strip() in transportation["name"].lower():
                dispatcher.utter_message(
                    text=f"{transportation['name']} có các tuyến đường {transportation['popular_routes']} bạn nhé")
                return []

        dispatcher.utter_message(
            text=f"Xin lỗi, mình chưa có thông tin về {transportation_name}.")
        return []


class ActionProvideTransportationOffice(Action):
    def name(self) -> Text:
        return "action_provide_transportation_office"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        transportation_name = next(
            tracker.get_latest_entity_values("transportation_name"), None)
        if not transportation_name:
            dispatcher.utter_message(
                text="Bạn muốn hỏi văn phòng của hãng xe nào vậy?")
            return []

        with open("actions/data/transportation.json", "r", encoding="utf-8") as f:
            transportations = json.load(f)

        for transportation in transportations:
            if transportation_name.lower().strip() in transportation["name"].lower():
                dispatcher.utter_message(
                    text=f"{transportation['name']} có văn phòng nằm ở {transportation['office']} nhé")
                return []

        dispatcher.utter_message(
            text=f"Xin lỗi, mình chưa có thông tin về {transportation_name}.")
        return []


class ActionProvideTransportationHotline(Action):
    def name(self) -> Text:
        return "action_provide_transportation_hotline"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        transportation_name = next(
            tracker.get_latest_entity_values("transportation_name"), None)
        if not transportation_name:
            dispatcher.utter_message(
                text="Bạn muốn hỏi hotline của hãng xe nào vậy?")
            return []

        with open("actions/data/transportation.json", "r", encoding="utf-8") as f:
            transportations = json.load(f)

        for transportation in transportations:
            if transportation_name.lower().strip() in transportation["name"].lower():
                dispatcher.utter_message(
                    text=f"Hotline của {transportation['name']} là {transportation['hotline']} nhé")
                return []

        dispatcher.utter_message(
            text=f"Xin lỗi, mình chưa có thông tin về {transportation_name}.")
        return []

# travel expenses

# def normalize_group(text: str) -> str:
#     return re.sub(r"[()]", "", text).strip().lower()

class ActionProvideTravelExpensesWithComposition(Action):
    def name(self) -> Text:
        return "action_provide_travel_expenses_with_composition"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Lấy giá trị của expenses_composition từ tracker
        expenses_composition = next(
            tracker.get_latest_entity_values("expenses_composition"), None)
        
        # dispatcher.utter_message(text=f"Entity đây: {expenses_composition}")
        
        if not expenses_composition:
            dispatcher.utter_message(
                text="Bạn muốn hỏi chi phí du lịch cho nhóm nào vậy? Ví dụ: Một mình, Cặp đôi, Gia đình, Nhóm bạn.")
            return []
        # Đọc dữ liệu từ tệp JSON
        try:
            with open("cleaned_travel.json", "r", encoding="utf-8") as f:
                travel_expenses = json.load(f)
        except FileNotFoundError:
            dispatcher.utter_message(
                text="Xin lỗi, mình không thể truy cập dữ liệu chi phí du lịch ngay bây giờ.")
            return []

        # Lọc danh sách dựa trên expenses_composition
        filtered_expenses = [
            expense for expense in travel_expenses
            if expense.get("group composition", "").lower() == expenses_composition.lower()
        ]

        # Kiểm tra nếu không có kết quả phù hợp
        if not filtered_expenses:
            dispatcher.utter_message(
                text=f"Xin lỗi, mình không tìm thấy thông tin chi phí cho nhóm {expenses_composition}.")
            return []

        # Tạo thông điệp trả lời
        response = f"Chi phí du lịch cho nhóm {expenses_composition}:\n"
        for expense in filtered_expenses:
            response += (
                f"- {expense.get('number_of_days', 'Không rõ thời gian')}, "
                f"{expense.get('type_of_tour', 'Không rõ loại tour')}, "
                f"thời gian: {expense.get('time', 'Không rõ thời gian')}, "
                f"chi phí ước tính: {expense.get('estimated_total_cost', 'Không rõ')} VND.\n"
            )

        # Gửi thông điệp đến người dùng
        dispatcher.utter_message(text=response)
        dispatcher.utter_message(text=f"{expenses_composition}, bạn muốn đi trong bao lâu?")
        return []
    

class ActionProvideTravelExpensesByTime(Action):
    def name(self) -> Text:
        return "action_provide_travel_expenses_by_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Lấy giá trị của time từ tracker
        time = next(tracker.get_latest_entity_values("time"), None)
        if not time:
            dispatcher.utter_message(
                text="Bạn muốn hỏi chi phí du lịch vào thời gian nào? Ví dụ: Mùa cao điểm, Mùa thấp điểm, Mùa thường.")
            return []

        # Đọc dữ liệu từ tệp JSON
        try:
            with open("actions/data/travel_expenses.json", "r", encoding="utf-8") as f:
                travel_expenses = json.load(f)
        except FileNotFoundError:
            dispatcher.utter_message(
                text="Xin lỗi, mình không thể truy cập dữ liệu chi phí du lịch ngay bây giờ.")
            return []

        # Lọc danh sách dựa trên thời gian
        filtered_expenses = [
            expense for expense in travel_expenses
            if expense.get("time", "").lower() == time.lower()
        ]

        # Kiểm tra nếu không có kết quả phù hợp
        if not filtered_expenses:
            dispatcher.utter_message(
                text=f"Xin lỗi, mình không tìm thấy thông tin chi phí cho thời gian {time}.")
            return []

        # Tạo thông điệp trả lời
        response = f"Chi phí du lịch vào {time}:\n"
        for expense in filtered_expenses:
            response += (
                f"- {expense.get('number_of_days', 'Không rõ thời gian')}, "
                f"{expense.get('type_of_tour', 'Không rõ loại tour')}, "
                f"nhóm: {expense.get('group composition', 'Không rõ nhóm')}, "
                f"chi phí ước tính: {expense.get('estimated_total_cost', 'Không rõ')} VND.\n"
            )

        # Gửi thông điệp đến người dùng
        dispatcher.utter_message(text=response)
        return []
    

class ActionProvideTravelExpensesByDuration(Action):
    def name(self) -> Text:
        return "action_provide_travel_expenses_by_duration"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Lấy giá trị của number_of_days từ tracker
        number_of_days = next(
            tracker.get_latest_entity_values("number_of_days"), None)
        if not number_of_days:
            dispatcher.utter_message(
                text="Bạn muốn hỏi chi phí du lịch kéo dài bao nhiêu ngày? Ví dụ: 2 ngày 1 đêm, 1 tuần, 1 tháng.")
            return []

        # Đọc dữ liệu từ tệp JSON
        try:
            with open("actions/data/travel_expenses.json", "r", encoding="utf-8") as f:
                travel_expenses = json.load(f)
        except FileNotFoundError:
            dispatcher.utter_message(
                text="Xin lỗi, mình không thể truy cập dữ liệu chi phí du lịch ngay bây giờ.")
            return []

        # Lọc danh sách dựa trên số ngày
        filtered_expenses = [
            expense for expense in travel_expenses
            if expense.get("number_of_days", "").lower() == number_of_days.lower()
        ]

        # Kiểm tra nếu không có kết quả phù hợp
        if not filtered_expenses:
            dispatcher.utter_message(
                text=f"Xin lỗi, mình không tìm thấy thông tin chi phí cho chuyến đi kéo dài {number_of_days}.")
            return []

        # Tạo thông điệp trả lời
        response = f"Chi phí du lịch kéo dài {number_of_days}:\n"
        for expense in filtered_expenses:
            response += (
                f"- {expense.get('type_of_tour', 'Không rõ loại tour')}, "
                f"nhóm: {expense.get('group composition', 'Không rõ nhóm')}, "
                f"thời gian: {expense.get('time', 'Không rõ thời gian')}, "
                f"chi phí ước tính: {expense.get('estimated_total_cost', 'Không rõ')} VND.\n"
            )

        # Gửi thông điệp đến người dùng
        dispatcher.utter_message(text=response)
        return []


class ActionProvideTravelExpensesCombined(Action):
    def name(self) -> Text:
        return "action_provide_travel_expenses_combined"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Lấy giá trị từ các slots
        expenses_composition = tracker.get_slot("expenses_composition")
        time = tracker.get_slot("time")
        number_of_days = tracker.get_slot("number_of_days")
        type_of_tour = tracker.get_slot("type_of_tour")

        # dispatcher.utter_message(
        #     text=f"Yêu cầu: {expenses_composition}, {time}, {number_of_days}, {type_of_tour}")

        # Đọc dữ liệu từ tệp JSON
        try:
            with open("cleaned_travel.json", "r", encoding="utf-8") as f:
                travel_expenses = json.load(f)
        except FileNotFoundError:
            dispatcher.utter_message(
                text="Xin lỗi, mình không thể truy cập dữ liệu chi phí du lịch ngay bây giờ.")
            return []


        # Lọc danh sách dựa trên các tiêu chí
        filtered_expenses = [
            expense for expense in travel_expenses
            if (not expenses_composition or expense.get("group composition", "").lower() == expenses_composition.lower())
            and (not time or expense.get("time", "").lower() == time.lower())
            and (not number_of_days or expense.get("number_of_days", "").lower() == number_of_days.lower())
            and (not type_of_tour or expense.get("type_of_tour", "").lower() == type_of_tour.lower())
        ]

        # Kiểm tra nếu không có kết quả phù hợp
        if not filtered_expenses:
            dispatcher.utter_message(
                text="Xin lỗi, mình không tìm thấy thông tin chi phí phù hợp với yêu cầu của bạn.")
            return []

        # Tạo thông điệp trả lời
        response = "Chi phí du lịch phù hợp với yêu cầu của bạn:\n"
        for expense in filtered_expenses:
            response += (
                f"- {expense.get('number_of_days', 'Không rõ thời gian')}, "
                f"{expense.get('type_of_tour', 'Không rõ loại tour')}, "
                f"nhóm: {expense.get('group composition', 'Không rõ nhóm')}, "
                f"thời gian: {expense.get('time', 'Không rõ thời gian')}, "
                f"chi phí ước tính: {expense.get('estimated_total_cost', 'Không rõ')} VND.\n"
            )

        # Gửi thông điệp đến người dùng
        dispatcher.utter_message(text=response)
        return []


class ActionProvideTravelExpensesByTourType(Action):
    def name(self) -> Text:
        return "action_provide_travel_expenses_by_tour_type"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Lấy giá trị của type_of_tour từ tracker
        type_of_tour = next(
            tracker.get_latest_entity_values("type_of_tour"), None)
        if not type_of_tour:
            dispatcher.utter_message(
                text="Bạn muốn hỏi chi phí du lịch cho loại tour nào? Ví dụ: Tiết kiệm/Trung bình, Cao cấp/Sang trọng, Giá rẻ/Bình dân.")
            return []

        # Đọc dữ liệu từ tệp JSON
        try:
            with open("actions/data/travel_expenses.json", "r", encoding="utf-8") as f:
                travel_expenses = json.load(f)
        except FileNotFoundError:
            dispatcher.utter_message(
                text="Xin lỗi, mình không thể truy cập dữ liệu chi phí du lịch ngay bây giờ.")
            return []

        # Lọc danh sách dựa trên loại tour
        filtered_expenses = [
            expense for expense in travel_expenses
            if expense.get("type_of_tour", "").lower() == type_of_tour.lower()
        ]

        # Kiểm tra nếu không có kết quả phù hợp
        if not filtered_expenses:
            dispatcher.utter_message(
                text=f"Xin lỗi, mình không tìm thấy thông tin chi phí cho loại tour {type_of_tour}.")
            return []

        # Tạo thông điệp trả lời
        response = f"Chi phí du lịch cho loại tour {type_of_tour}:\n"
        for expense in filtered_expenses:
            response += (
                f"- {expense.get('number_of_days', 'Không rõ thời gian')}, "
                f"nhóm: {expense.get('group composition', 'Không rõ nhóm')}, "
                f"thời gian: {expense.get('time', 'Không rõ thời gian')}, "
                f"chi phí ước tính: {expense.get('estimated_total_cost', 'Không rõ')} VND.\n"
            )

        # Gửi thông điệp đến người dùng
        dispatcher.utter_message(text=response)
        return []
