from uuid import uuid4, UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends
from app.schemas.categories import CategorySchema, CategoryCreateSchema, CategoryUpdateSchema
from starlette import status
from app.models.categories import CategoryORM
from app.db.database import get_db

router = APIRouter(prefix="/categories")


categories: list[CategorySchema] = []

@router.get("")
def get_categories(db: Session = Depends(get_db)) -> list[CategorySchema]:
    categories = db.scalars(select(CategoryORM)).all()
    return categories
    #return [CategorySchema.model_validate(cat) for cat in categories]


@router.post("", status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreateSchema, db: Session = Depends(get_db)) -> CategorySchema:
    new_category = CategoryORM(name=payload.name)
    db.add(new_category)
    db.commit()
    return new_category


@router.patch("/{id}")
def edit_category(id: UUID, payload: CategoryUpdateSchema, db: Session = Depends(get_db)) -> CategorySchema:
    
    category = db.get(CategoryORM, str(id))
    if category is None:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    
    if payload.name is not None:
        category.name = payload.name
    db.commit()
    db.refresh(category)
    return category
    
    
    
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(id: UUID, db: Session = Depends(get_db)):
    category = db.get(CategoryORM, str(id))
    if category is None:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    db.delete(category)
    db.commit()
