from .base import BaseMessage


# TODO: event -> заполнение формы:
# actions:
# 1. Заполнить данные в первый раз
# 2. Изменить форму ? (подумать над реализацией)

# TODO: переименовать FormMessage
class FormMessage(BaseMessage):
    action: str
    user_id: int
    name: str
    age: int
    gender: str
    description: str
    filter_by_age: str
    filter_by_gender: str
    filter_by_description: str

class RecommendMessage(BaseMessage):
    action: str
    user_id: int