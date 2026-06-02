def success_response(
    message,
    data=None
):

    response = {
        "message": message
    }

    if data is not None:

        response["data"] = data

    return response


def error_response(message: str):
    return {
        "message": message
    }