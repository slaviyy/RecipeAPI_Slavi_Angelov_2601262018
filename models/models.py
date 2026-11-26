
from enum import Enum
from typing import Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    EmailStr,
    field_validator
)


# Maximum number of servings
MAX_SERVINGS = 68


# Recipe difficulty
class Difficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


# Ingredient unit
class IngredientUnit(str, Enum):
    G = "g"
    ML = "ml"
    PCS = "pcs"


# Author schemas
class AuthorBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr

    @field_validator("name", mode="before")
    @classmethod
    def validate_name(cls, value):
        if isinstance(value, str):
            value = value.strip()
        return value

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, value):
        if isinstance(value, str):
            value = value.strip()
        return value


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None

    @field_validator("name", mode="before")
    @classmethod
    def validate_name(cls, value):
        if isinstance(value, str):
            value = value.strip()
        return value

    @field_validator("email", mode="before")
    @classmethod
    def normalize_email(cls, value):
        if isinstance(value, str):
            value = value.strip()
        return value


class AuthorResponse(AuthorBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# Category schemas
class CategoryBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)

    @field_validator("name", mode="before")
    @classmethod
    def validate_name(cls, value):
        if isinstance(value, str):
            value = value.strip()
        return value


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)

    @field_validator("name", mode="before")
    @classmethod
    def validate_name(cls, value):
        if isinstance(value, str):
            value = value.strip()
        return value


class CategoryResponse(CategoryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# Ingredient schemas
class IngredientBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)

    @field_validator("name", mode="before")
    @classmethod
    def validate_name(cls, value):
        if isinstance(value, str):
            value = value.strip()
        return value


class IngredientCreate(IngredientBase):
    pass


class IngredientUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)

    @field_validator("name", mode="before")
    @classmethod
    def validate_name(cls, value):
        if isinstance(value, str):
            value = value.strip()
        return value


class IngredientResponse(IngredientBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# Recipe ingredient schemas
class RecipeIngredientCreate(BaseModel):
    ingredient_id: int = Field(gt=0)
    quantity: float = Field(gt=0)
    unit: IngredientUnit


class RecipeIngredientUpdate(BaseModel):
    quantity: Optional[float] = Field(default=None, gt=0)
    unit: Optional[IngredientUnit] = None


class RecipeIngredientResponse(BaseModel):
    ingredient_id: int
    ingredient_name: str
    quantity: float
    unit: IngredientUnit


# Recipe schemas
class RecipeBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    instructions: str = Field(min_length=1)
    preparation_time: int = Field(gt=0)
    servings: int = Field(gt=0, le=MAX_SERVINGS)
    author_id: int = Field(gt=0)
    category_id: Optional[int] = Field(default=None, gt=0)
    difficulty: Difficulty

    @field_validator("title", "instructions", mode="before")
    @classmethod
    def validate_text(cls, value):
        if isinstance(value, str):
            value = value.strip()
        return value


class RecipeCreate(RecipeBase):
    pass


class RecipeUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    instructions: Optional[str] = Field(default=None, min_length=1)
    preparation_time: Optional[int] = Field(default=None, gt=0)
    servings: Optional[int] = Field(
        default=None,
        gt=0,
        le=MAX_SERVINGS
    )
    author_id: Optional[int] = Field(default=None, gt=0)
    category_id: Optional[int] = Field(default=None, gt=0)
    difficulty: Optional[Difficulty] = None

    @field_validator("title", "instructions", mode="before")
    @classmethod
    def validate_text(cls, value):
        if isinstance(value, str):
            value = value.strip()
        return value


class RecipeResponse(RecipeBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# Recipe with ingredients
class RecipeDetailsResponse(RecipeResponse):
    ingredients: list[RecipeIngredientResponse] = Field(
        default_factory=list
    )


# Recipe with recalculated servings
class RecipeScaledResponse(RecipeResponse):
    requested_servings: int = Field(
        gt=0,
        le=MAX_SERVINGS
    )
    ingredients: list[RecipeIngredientResponse] = Field(
        default_factory=list
    )
