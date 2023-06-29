# errors.py
# Relative Path: insight/api/schemas/errors.py
from pydantic import BaseModel

# HTTP Error Handling Class
class HTTPError(BaseModel):
    detail: str