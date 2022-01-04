from pydantic import BaseModel


class SimpleModel(BaseModel):
    no: int
    nm: str = ""
