
from pydantic import BaseModel, ConfigDict, Field, EmailStr
from typing import Optional
from enum import Enum


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


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None


class AuthorResponse(AuthorBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# Category schemas
class CategoryBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)


class CategoryResponse(CategoryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# Ingredient schemas
class IngredientBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class IngredientCreate(IngredientBase):
    pass


class IngredientUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)


class IngredientResponse(IngredientBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# Recipe ingredient schemas
class RecipeIngredientCreate(BaseModel):
    ingredient_id: int
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
    servings: int = Field(gt=0)
    author_id: int
    category_id: Optional[int] = None


class RecipeCreate(RecipeBase):
    pass


class RecipeUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    instructions: Optional[str] = Field(default=None, min_length=1)
    preparation_time: Optional[int] = Field(default=None, gt=0)
    servings: Optional[int] = Field(default=None, gt=0)
    category_id: Optional[int] = None


class RecipeResponse(RecipeBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# Recipe with ingredients
class RecipeDetailsResponse(RecipeResponse):
    ingredients: list[RecipeIngredientResponse] = []


# Recipe with recalculated servings
class RecipeScaledResponse(RecipeResponse):
    requested_servings: int
    ingredients: list[RecipeIngredientResponse]
