def ResponseModel(data, message, code):
    return {
        "data": "" if not data else data,
        "code": code,
        "message": message,
    }
