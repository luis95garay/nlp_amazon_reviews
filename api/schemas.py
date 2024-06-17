from pydantic import BaseModel


class Review(BaseModel):
    text: str = 'It is the worst product I have ever bought'
