from database import *
from fastapi import FastAPI, Body, status, Depends
from fastapi.responses import JSONResponse, FileResponse

app = FastAPI()

# определяем зависимость
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def main():
    return FileResponse("Public/index.html")

@app.get("/api/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@app.get("/api/users/{id}")
def get_user(id: int, db: Session = Depends(get_db)):
    return db.query(User).filter(User.id == id).first()

@app.post("/api/users")
def create_user(user: User, db: Session = Depends(get_db)):
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# @app.put("/api/users/{id}")
# def update_user(id: int, user: User, db: Session = Depends(get_db)):
#     db.query(User).filter(User.id == id).update(user.dict())
#     db.commit()
#     return user

@app.delete("/api/users/{id}")
def delete_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    db.delete(user)
    db.commit()
    return user