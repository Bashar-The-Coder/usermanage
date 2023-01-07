

from fastapi import APIRouter, Depends, HTTPException, status
from app.dependency import get_db
from .. import models
from ..schemas.todosSchema import *
from sqlalchemy.orm import session

router = APIRouter(
    prefix="/todos",
    tags=["Todo"],
    dependencies=[Depends(get_db)],
    responses={404: {"description": "Not found"}},
)
 


@router.get("/")
async def create_database(db: session =Depends(get_db)):
    q =  db.query(models.Todos).all() # this is list
    db.close()
    return {"data" : q}
# get single todo
@router.get("/{todo_id}")
async def read_todo(todo_id : int,db: session =Depends(get_db)):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    if not todo_model:
        raise HTTPException (status_code = status.HTTP_404_NOT_FOUND, detail = f"requested id {todo_id} not found in database")
    return todo_model


# post todo

@router.post("/post_todo" , status_code=status.HTTP_201_CREATED)
async def create_todo(todo:TodoIn , db:session = Depends(get_db)):
    todo_body = todo.dict()
    add_todo = models.Todos(**todo_body)
    db.add(add_todo)
    db.commit()
    return {"todo" : todo_body}

@router.put("/update_todo/{todo_id}" , status_code=status.HTTP_200_OK)
async def update_todo(todo_id: int , todo_body: TodoIn, db:session = Depends(get_db)):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    if not todo_model:
        raise HTTPException (status_code = status.HTTP_404_NOT_FOUND, detail = f"requested id {todo_id} not found in database")

    todo_model.title = todo_body.title
    todo_model.description = todo_body.description
    todo_model.priority = todo_body.priority
    todo_model.complete = todo_body.complete
    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)
    return {"updated" : todo_model}

@router.delete("/delete_todo/{todo_id}" , status_code=status.HTTP_200_OK)
async def delete_todo(*,todo_id: int , db:session = Depends(get_db)):
    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    if not todo_model:
      raise HTTPException (status_code = status.HTTP_404_NOT_FOUND, detail = f"requested id {todo_id} not found in database")
    db.query(models.Todos).filter(models.Todos.id == todo_id).delete()
    db.commit()
    db.close()