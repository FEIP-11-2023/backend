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
