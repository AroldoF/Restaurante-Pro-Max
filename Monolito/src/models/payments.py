from sqlmodel import SQLModel, Field, Relationship


class Payment(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
