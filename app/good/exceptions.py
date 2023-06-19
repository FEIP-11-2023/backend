from app.exceptions import ExceptionDescribed


class RemainderCannotBeNegative(ExceptionDescribed):
    code = "GO-0001"
    status_code = 400
    description = {
        "en": "Remainder must be non-negative",
        "ru": "Остаток должен быть неотрицательным",
    }


class DeltaCannotBeNegative(ExceptionDescribed):
    code = "GO-0002"
    status_code = 400
    description = {
        "en": "Delta must be non-negative",
        "ru": "Изменение должно быть неотрицательным",
    }


class EntityNotFound(ExceptionDescribed):
    def __init__(self, id: str):
        self.code = "GO-0003"
        self.status_code = 404
        self.description = {
            "en": f'Enity with id "{id}" not found',
            "ru": f'Сущность с id "{id}" не найдена',
        }


class EntityAlreadyExists(ExceptionDescribed):
    code = "GO-0004"
    status_code = 400
    description = {"en": "Entity already exists", "ru": "Сущность уже существует"}
