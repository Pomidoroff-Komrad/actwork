from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime, timedelta


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Define Models
class BorrowedBook(BaseModel):
    book_id: str
    book_title: str
    borrowed_date: datetime
    due_date: Optional[datetime] = None

class Student(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    first_name: str
    last_name: str
    class_name: str
    borrowed_books: List[BorrowedBook] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)

class StudentCreate(BaseModel):
    first_name: str
    last_name: str
    class_name: str

class StudentUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    class_name: Optional[str] = None

class Book(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    author: str
    quantity: int = 1
    borrowed_count: int = 0
    available: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

class BookCreate(BaseModel):
    title: str
    author: str
    quantity: int = 1

class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    quantity: Optional[int] = None

class BorrowRequest(BaseModel):
    student_id: str
    book_id: str
    due_days: Optional[int] = 14  # Default 2 weeks

class ReturnRequest(BaseModel):
    student_id: str
    book_id: str

# Basic route
@api_router.get("/")
async def root():
    return {"message": "Librarian Assistant API"}

# Student endpoints
@api_router.post("/students", response_model=Student)
async def create_student(student: StudentCreate):
    student_dict = student.dict()
    student_obj = Student(**student_dict)
    await db.students.insert_one(student_obj.dict())
    return student_obj

@api_router.get("/students", response_model=List[Student])
async def get_all_students():
    students = await db.students.find().to_list(1000)
    return [Student(**student) for student in students]

@api_router.get("/students/class/{class_name}", response_model=List[Student])
async def get_students_by_class(class_name: str):
    students = await db.students.find({"class_name": class_name}).to_list(1000)
    return [Student(**student) for student in students]

@api_router.get("/classes")
async def get_all_classes():
    classes = await db.students.distinct("class_name")
    return {"classes": classes}

@api_router.put("/students/{student_id}", response_model=Student)
async def update_student(student_id: str, student_update: StudentUpdate):
    update_data = {k: v for k, v in student_update.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No valid fields provided for update")
    
    result = await db.students.update_one(
        {"id": student_id}, 
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    
    updated_student = await db.students.find_one({"id": student_id})
    return Student(**updated_student)

@api_router.delete("/students/{student_id}")
async def delete_student(student_id: str):
    result = await db.students.delete_one({"id": student_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted successfully"}

# Book endpoints
@api_router.post("/books", response_model=Book)
async def create_book(book: BookCreate):
    book_dict = book.dict()
    book_obj = Book(**book_dict)
    await db.books.insert_one(book_obj.dict())
    return book_obj

@api_router.get("/books", response_model=List[Book])
async def get_all_books():
    books = await db.books.find().to_list(1000)
    return [Book(**book) for book in books]

@api_router.put("/books/{book_id}", response_model=Book)
async def update_book(book_id: str, book_update: BookUpdate):
    update_data = {k: v for k, v in book_update.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No valid fields provided for update")
    
    result = await db.books.update_one(
        {"id": book_id}, 
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Book not found")
    
    updated_book = await db.books.find_one({"id": book_id})
    return Book(**updated_book)

@api_router.delete("/books/{book_id}")
async def delete_book(book_id: str):
    result = await db.books.delete_one({"id": book_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}

# Class management
class ClassCreate(BaseModel):
    name: str

@api_router.post("/classes")
async def create_class(class_data: ClassCreate):
    # For now, we'll just return success since classes are created when students are added
    # But we could store empty classes in the future if needed
    return {"message": f"Class {class_data.name} is ready to accept students", "class_name": class_data.name}

@api_router.get("/stats")
async def get_stats():
    # Get total students
    total_students = await db.students.count_documents({})
    
    # Get total books
    total_books = await db.books.count_documents({})
    
    # Get class counts
    pipeline = [
        {"$group": {"_id": "$class_name", "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]
    class_counts = await db.students.aggregate(pipeline).to_list(1000)
    
    # Get available books count
    available_books = await db.books.count_documents({"available": True})
    
    return {
        "total_students": total_students,
        "total_books": total_books,
        "available_books": available_books,
        "total_classes": len(class_counts),
        "class_counts": {item["_id"]: item["count"] for item in class_counts}
    }

# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()