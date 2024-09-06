from sqlmodel import Field, SQLModel


class CategoryBase(SQLModel):
    title: str
    description: str


class Category(CategoryBase, table=True):
    id: int = Field(primary_key=True)
