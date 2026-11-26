
from sqlalchemy import (
    String,
    Integer,
    Float,
    ForeignKey,
    CheckConstraint,
    Index,
    func
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.database import Base


# Author model
class Author(Base):
    __tablename__ = "author"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    recipes: Mapped[list["Recipe"]] = relationship(back_populates="author")

    __table_args__ = (
        CheckConstraint("length(trim(name)) > 0"),
    )


# Category model
class Category(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    recipes: Mapped[list["Recipe"]] = relationship(back_populates="category")

    __table_args__ = (
        CheckConstraint("length(trim(name)) > 0"),
    )


# Ingredient model
class Ingredient(Base):
    __tablename__ = "ingredient"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    recipe_ingredients: Mapped[list["RecipeIngredient"]] = relationship(
        back_populates="ingredient"
    )

    __table_args__ = (
        CheckConstraint("length(trim(name)) > 0"),
    )


# Recipe model
class Recipe(Base):
    __tablename__ = "recipe"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    instructions: Mapped[str] = mapped_column(nullable=False)
    preparation_time: Mapped[int] = mapped_column(Integer, nullable=False)
    servings: Mapped[int] = mapped_column(Integer, nullable=False)

    author_id: Mapped[int] = mapped_column(
        ForeignKey("author.id", ondelete="RESTRICT"),
        nullable=False
    )

    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("category.id", ondelete="SET NULL"),
        nullable=True
    )

    # New field - added through the second Alembic migration
    difficulty: Mapped[str] = mapped_column(String(10), nullable=False)

    author: Mapped["Author"] = relationship(back_populates="recipes")
    category: Mapped["Category | None"] = relationship(back_populates="recipes")

    recipe_ingredients: Mapped[list["RecipeIngredient"]] = relationship(
        back_populates="recipe",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    __table_args__ = (
        CheckConstraint("length(trim(title)) > 0"),
        CheckConstraint("length(trim(instructions)) > 0"),
        CheckConstraint("preparation_time > 0"),
        CheckConstraint("servings > 0"),
        CheckConstraint("difficulty IN ('easy', 'medium', 'hard')"),
    )


# RecipeIngredient model
class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredient"

    recipe_id: Mapped[int] = mapped_column(
        ForeignKey("recipe.id", ondelete="CASCADE"),
        primary_key=True
    )

    ingredient_id: Mapped[int] = mapped_column(
        ForeignKey("ingredient.id", ondelete="RESTRICT"),
        primary_key=True
    )

    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str] = mapped_column(String(10), nullable=False)

    recipe: Mapped["Recipe"] = relationship(back_populates="recipe_ingredients")
    ingredient: Mapped["Ingredient"] = relationship(
        back_populates="recipe_ingredients"
    )

    __table_args__ = (
        CheckConstraint("quantity > 0"),
        CheckConstraint("unit IN ('g', 'ml', 'pcs')"),
    )


# Functional indexes
Index(
    "uq_category_name_normalized",
    func.lower(func.trim(Category.name)),
    unique=True
)

Index(
    "uq_ingredient_name_normalized",
    func.lower(func.trim(Ingredient.name)),
    unique=True
)

Index(
    "uq_recipe_author_title_normalized",
    Recipe.author_id,
    func.lower(func.trim(Recipe.title)),
    unique=True
)
