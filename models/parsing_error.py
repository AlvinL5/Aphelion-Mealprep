from pydantic import BaseModel

class ParsingError(BaseModel):
    message: str