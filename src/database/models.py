from sqlmodel import Field, SQLModel


class CategoryBase(SQLModel):
    pass


class Category(CategoryBase, table=True):
    id: int = Field(primary_key=True)
