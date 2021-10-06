class ErrorCode:
    NotFound = 404
    Success = 200
    Created = 201
    InternalServerError = 500
    Unauthorized = 401
    InvalidRequestData = 1000
    NotEnough = 1001
    DuplicateItem = 1002


class ErrorMessage:
    NotFound = "Not Found Data"
    Success = "Success"
    Created = "Created"
    InternalServerError = "Internal Server Error"
    Unauthorized = "Unauthorized"
    InvalidRequestData = "Invalid Request Data. You must pass enough data"
    NotEnough = "There is not enough quantity for this item"
    DuplicateItem = "Duplicate Item. Can not insert again!"