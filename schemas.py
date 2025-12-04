from pydantic import BaseModel


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    pass


class ComponentBase(BaseModel):
    name: str
    brand: str
    price: int
    category_id: int


class ComponentCreate(ComponentBase):
    pass


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class BuildBase(BaseModel):
    name: str
    user_id: int


class BuildCreate(BuildBase):
    pass
