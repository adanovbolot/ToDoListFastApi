from sqlalchemy.orm import Session
from todo.app import app, templates
from fastapi import Request, Depends, Form
from todo.database.base import get_db
from todo.models import ToDo
from todo.config import settings
from starlette.responses import RedirectResponse, FileResponse
from starlette.status import HTTP_303_SEE_OTHER, HTTP_302_FOUND


@app.get('/')
def home(request: Request, db_session: Session = Depends(get_db)):
    todos = db_session.query(ToDo).all()
    return templates.TemplateResponse('todo/index.html',
                                      {'request': request,
                                       'app_name': settings.app_name,
                                       'todo_list': todos}
                                      )


@app.post("/add")
def add(title: str = Form(...), db_session: Session = Depends(get_db)):
    new_todo = ToDo(title=title)
    db_session.add(new_todo)
    db_session.commit()
    url = app.url_path_for('home')
    return RedirectResponse(url=url, status_code=HTTP_303_SEE_OTHER)


@app.get('/update/{todo_id}')
def update(todo_id: int, db_session: Session = Depends(get_db)):
    todo = db_session.query(ToDo).filter(ToDo.id==todo_id).first()
    todo.is_complete = not todo.is_complete
    db_session.commit()
    url = app.url_path_for('home')
    return RedirectResponse(url=url, status_code=HTTP_302_FOUND)


@app.get('/delete/{todo_id}')
def delete(todo_id: int, db_session: Session = Depends(get_db)):
    todo = db_session.query(ToDo).filter_by(id=todo_id).first()
    db_session.delete(todo)
    db_session.commit()

    url = app.url_path_for('home')
    return RedirectResponse(url=url, status_code=HTTP_302_FOUND)

    
@app.get('/search')
def search(anime: str = Form(...)):
    # anime = 'https://service.sovetromantica.com/v1/animesearch?anime_name='
    return templates.TemplateResponse('todo/search.html', context={
        'app_name': settings.app_name,
        # 'anime': anime,
    })
