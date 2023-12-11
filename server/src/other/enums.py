from enum import Enum


class TimeInterval(Enum):
    one_min = "1 min"
    five_mins = "5 mins"
    one_hour = "1 hour"
    five_hours = "5 hours"
    twelve_hours = "12 hours"
    one_day = "1 day"


class TaskStatus(Enum):
    active = "Active"
    disabled = "Disabled"


class UnloaderServiceType(Enum):
    fortochki = "FORTOCHKI"
    starco = "STARCO"


class CallRequestStatus(str, Enum):
    PRODUCT = "Продукты"
    # рассрочка
    INSTALLMENT = "Рассрочка"


class FormApplicationStatus(str, Enum):
    NEW = "Новый"
    PROGRESS = "В прогрессе"
    COMPLETED = "Завершен"


class OrderStatus(str, Enum):
    NEW = "new"
    PAID = "paid"
    AWAITING = "awaiting"
    CANCELED = "canceled"
    ACCEPTED = "accepted"


class DocumentType(str, Enum):
    INVOICE = "invoice"


class DayOfWeek(str, Enum):
    MONDAY = "Понедельник"
    TUESDAY = "Вторник"
    WEDNESDAY = "Среда"
    THURSDAY = "Четверг"
    FRIDAY = "Пятница"
    SATURDAY = "Суббота"
    SUNDAY = "Воскресенье"


class ProductType(str, Enum):
    RIMS = "rims"
    TIRES = "tires"
    ACCESSORY = "accessory"


class ProductColor(str, Enum):
    GRAY = "gray"
    BLACK = "black"
    WHITE = "white"


class RimType(str, Enum):
    # Литой
    ALLOY = 0
    # Литые
    FLOW_FORMING = 1
    # Ковыный
    FORGED = 2
    MAKET = 3
