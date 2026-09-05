from uuid import uuid4

from fastapi import APIRouter, HTTPException
from app.schemas.categories import CategorySchema, CategoryCreateSchema, CategoryUpdateSchema
from starlette import status

router = APIRouter(prefix="/categories")


categories: list[CategorySchema] = []

@router.get("")
def get_categories() -> list[CategorySchema]:
    return categories


@router.post("", status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreateSchema) -> CategorySchema:
    new_category = CategorySchema(id=str(uuid4()), name=payload.name)
    categories.append(new_category)
    return new_category


@router.patch("/{id}")
def edit_category(id: str, payload: CategoryUpdateSchema) -> CategorySchema:
    category = None
    for i in categories:
        if id == i.id:
            category = i
            break
    if category is not None:
        if payload.name is not None:
            category.name = payload.name
        return category
    else:
        raise HTTPException(status_code=404, detail="Задача не найдена")