from uuid import uuid4, UUID

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
    new_category = CategorySchema(id=uuid4(), name=payload.name)
    categories.append(new_category)
    return new_category


@router.patch("/{id}")
def edit_category(id: UUID, payload: CategoryUpdateSchema) -> CategorySchema:
    category = search_category(id)
    
    if category is not None:
        if payload.name is not None:
            category.name = payload.name
        return category
    else:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    
    
    
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(id: UUID):
    category = search_category(id)
    if category is None:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    categories.remove(category)


def search_category(id: UUID) -> CategorySchema | None:
    for i in categories:
        if id == i.id:
            return i
    return None