from fastapi.responses import JSONResponse


def success_response(data, status_code=200):
    return JSONResponse(content={"success": True, "data": data}, status_code=status_code)

def error_response(message, status_code=400):
    return JSONResponse(content={"success": False, "error": message}, status_code=status_code)