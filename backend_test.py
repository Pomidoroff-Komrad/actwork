#!/usr/bin/env python3
"""
Comprehensive Backend API Testing for Librarian Assistant
Tests all Student and Book CRUD operations with MongoDB integration
"""

import requests
import json
import uuid
from datetime import datetime
import sys
import os

# Get backend URL from frontend .env file
def get_backend_url():
    try:
        with open('/app/frontend/.env', 'r') as f:
            for line in f:
                if line.startswith('REACT_APP_BACKEND_URL='):
                    return line.split('=', 1)[1].strip()
    except Exception as e:
        print(f"Error reading backend URL: {e}")
        return None

BASE_URL = get_backend_url()
if not BASE_URL:
    print("ERROR: Could not get backend URL from frontend/.env")
    sys.exit(1)

API_URL = f"{BASE_URL}/api"
print(f"Testing backend API at: {API_URL}")

class LibrarianAPITester:
    def __init__(self):
        self.session = requests.Session()
        self.created_students = []
        self.created_books = []
        self.test_results = {
            'passed': 0,
            'failed': 0,
            'errors': []
        }

    def log_result(self, test_name, success, message=""):
        if success:
            self.test_results['passed'] += 1
            print(f"✅ {test_name}")
        else:
            self.test_results['failed'] += 1
            self.test_results['errors'].append(f"{test_name}: {message}")
            print(f"❌ {test_name}: {message}")

    def test_health_check(self):
        """Test basic health check endpoint"""
        try:
            response = self.session.get(f"{API_URL}/")
            if response.status_code == 200:
                data = response.json()
                if "message" in data:
                    self.log_result("Health Check", True)
                    return True
                else:
                    self.log_result("Health Check", False, "Missing message in response")
            else:
                self.log_result("Health Check", False, f"Status code: {response.status_code}")
        except Exception as e:
            self.log_result("Health Check", False, f"Exception: {str(e)}")
        return False

    def test_create_student(self, first_name, last_name, class_name):
        """Test creating a new student"""
        try:
            student_data = {
                "first_name": first_name,
                "last_name": last_name,
                "class_name": class_name
            }
            response = self.session.post(f"{API_URL}/students", json=student_data)
            
            if response.status_code == 200:
                student = response.json()
                if all(key in student for key in ['id', 'first_name', 'last_name', 'class_name', 'created_at']):
                    self.created_students.append(student['id'])
                    self.log_result(f"Create Student ({first_name} {last_name})", True)
                    return student
                else:
                    self.log_result(f"Create Student ({first_name} {last_name})", False, "Missing required fields in response")
            else:
                self.log_result(f"Create Student ({first_name} {last_name})", False, f"Status code: {response.status_code}")
        except Exception as e:
            self.log_result(f"Create Student ({first_name} {last_name})", False, f"Exception: {str(e)}")
        return None

    def test_get_all_students(self):
        """Test retrieving all students"""
        try:
            response = self.session.get(f"{API_URL}/students")
            if response.status_code == 200:
                students = response.json()
                if isinstance(students, list):
                    self.log_result("Get All Students", True)
                    return students
                else:
                    self.log_result("Get All Students", False, "Response is not a list")
            else:
                self.log_result("Get All Students", False, f"Status code: {response.status_code}")
        except Exception as e:
            self.log_result("Get All Students", False, f"Exception: {str(e)}")
        return None

    def test_get_students_by_class(self, class_name):
        """Test retrieving students by class"""
        try:
            response = self.session.get(f"{API_URL}/students/class/{class_name}")
            if response.status_code == 200:
                students = response.json()
                if isinstance(students, list):
                    # Verify all students belong to the requested class
                    for student in students:
                        if student.get('class_name') != class_name:
                            self.log_result(f"Get Students by Class ({class_name})", False, "Student with wrong class returned")
                            return None
                    self.log_result(f"Get Students by Class ({class_name})", True)
                    return students
                else:
                    self.log_result(f"Get Students by Class ({class_name})", False, "Response is not a list")
            else:
                self.log_result(f"Get Students by Class ({class_name})", False, f"Status code: {response.status_code}")
        except Exception as e:
            self.log_result(f"Get Students by Class ({class_name})", False, f"Exception: {str(e)}")
        return None

    def test_get_all_classes(self):
        """Test retrieving all classes"""
        try:
            response = self.session.get(f"{API_URL}/classes")
            if response.status_code == 200:
                data = response.json()
                if "classes" in data and isinstance(data["classes"], list):
                    self.log_result("Get All Classes", True)
                    return data["classes"]
                else:
                    self.log_result("Get All Classes", False, "Missing or invalid classes field")
            else:
                self.log_result("Get All Classes", False, f"Status code: {response.status_code}")
        except Exception as e:
            self.log_result("Get All Classes", False, f"Exception: {str(e)}")
        return None

    def test_update_student(self, student_id, update_data):
        """Test updating a student"""
        try:
            response = self.session.put(f"{API_URL}/students/{student_id}", json=update_data)
            if response.status_code == 200:
                student = response.json()
                # Verify the update was applied
                for key, value in update_data.items():
                    if student.get(key) != value:
                        self.log_result("Update Student", False, f"Field {key} not updated correctly")
                        return None
                self.log_result("Update Student", True)
                return student
            elif response.status_code == 404:
                self.log_result("Update Student", False, "Student not found")
            else:
                self.log_result("Update Student", False, f"Status code: {response.status_code}")
        except Exception as e:
            self.log_result("Update Student", False, f"Exception: {str(e)}")
        return None

    def test_delete_student(self, student_id):
        """Test deleting a student"""
        try:
            response = self.session.delete(f"{API_URL}/students/{student_id}")
            if response.status_code == 200:
                data = response.json()
                if "message" in data:
                    self.log_result("Delete Student", True)
                    return True
                else:
                    self.log_result("Delete Student", False, "Missing message in response")
            elif response.status_code == 404:
                self.log_result("Delete Student", False, "Student not found")
            else:
                self.log_result("Delete Student", False, f"Status code: {response.status_code}")
        except Exception as e:
            self.log_result("Delete Student", False, f"Exception: {str(e)}")
        return False

    def test_create_book(self, title, author, isbn=None, available=True):
        """Test creating a new book"""
        try:
            book_data = {
                "title": title,
                "author": author,
                "available": available
            }
            if isbn:
                book_data["isbn"] = isbn
                
            response = self.session.post(f"{API_URL}/books", json=book_data)
            
            if response.status_code == 200:
                book = response.json()
                if all(key in book for key in ['id', 'title', 'author', 'available', 'created_at']):
                    self.created_books.append(book['id'])
                    self.log_result(f"Create Book ({title})", True)
                    return book
                else:
                    self.log_result(f"Create Book ({title})", False, "Missing required fields in response")
            else:
                self.log_result(f"Create Book ({title})", False, f"Status code: {response.status_code}")
        except Exception as e:
            self.log_result(f"Create Book ({title})", False, f"Exception: {str(e)}")
        return None

    def test_get_all_books(self):
        """Test retrieving all books"""
        try:
            response = self.session.get(f"{API_URL}/books")
            if response.status_code == 200:
                books = response.json()
                if isinstance(books, list):
                    self.log_result("Get All Books", True)
                    return books
                else:
                    self.log_result("Get All Books", False, "Response is not a list")
            else:
                self.log_result("Get All Books", False, f"Status code: {response.status_code}")
        except Exception as e:
            self.log_result("Get All Books", False, f"Exception: {str(e)}")
        return None

    def test_update_book(self, book_id, update_data):
        """Test updating a book"""
        try:
            response = self.session.put(f"{API_URL}/books/{book_id}", json=update_data)
            if response.status_code == 200:
                book = response.json()
                # Verify the update was applied
                for key, value in update_data.items():
                    if book.get(key) != value:
                        self.log_result("Update Book", False, f"Field {key} not updated correctly")
                        return None
                self.log_result("Update Book", True)
                return book
            elif response.status_code == 404:
                self.log_result("Update Book", False, "Book not found")
            else:
                self.log_result("Update Book", False, f"Status code: {response.status_code}")
        except Exception as e:
            self.log_result("Update Book", False, f"Exception: {str(e)}")
        return None

    def test_delete_book(self, book_id):
        """Test deleting a book"""
        try:
            response = self.session.delete(f"{API_URL}/books/{book_id}")
            if response.status_code == 200:
                data = response.json()
                if "message" in data:
                    self.log_result("Delete Book", True)
                    return True
                else:
                    self.log_result("Delete Book", False, "Missing message in response")
            elif response.status_code == 404:
                self.log_result("Delete Book", False, "Book not found")
            else:
                self.log_result("Delete Book", False, f"Status code: {response.status_code}")
        except Exception as e:
            self.log_result("Delete Book", False, f"Exception: {str(e)}")
        return False

    def test_error_handling(self):
        """Test error handling for non-existent IDs"""
        fake_id = str(uuid.uuid4())
        
        # Test non-existent student
        try:
            response = self.session.get(f"{API_URL}/students/{fake_id}")
            # This endpoint doesn't exist, so we expect 404 or 405
            if response.status_code in [404, 405]:
                self.log_result("Error Handling - Non-existent Student GET", True)
            else:
                self.log_result("Error Handling - Non-existent Student GET", False, f"Unexpected status: {response.status_code}")
        except Exception as e:
            self.log_result("Error Handling - Non-existent Student GET", False, f"Exception: {str(e)}")

        # Test updating non-existent student
        try:
            response = self.session.put(f"{API_URL}/students/{fake_id}", json={"first_name": "Test"})
            if response.status_code == 404:
                self.log_result("Error Handling - Update Non-existent Student", True)
            else:
                self.log_result("Error Handling - Update Non-existent Student", False, f"Expected 404, got {response.status_code}")
        except Exception as e:
            self.log_result("Error Handling - Update Non-existent Student", False, f"Exception: {str(e)}")

        # Test deleting non-existent student
        try:
            response = self.session.delete(f"{API_URL}/students/{fake_id}")
            if response.status_code == 404:
                self.log_result("Error Handling - Delete Non-existent Student", True)
            else:
                self.log_result("Error Handling - Delete Non-existent Student", False, f"Expected 404, got {response.status_code}")
        except Exception as e:
            self.log_result("Error Handling - Delete Non-existent Student", False, f"Exception: {str(e)}")

        # Test updating non-existent book
        try:
            response = self.session.put(f"{API_URL}/books/{fake_id}", json={"title": "Test"})
            if response.status_code == 404:
                self.log_result("Error Handling - Update Non-existent Book", True)
            else:
                self.log_result("Error Handling - Update Non-existent Book", False, f"Expected 404, got {response.status_code}")
        except Exception as e:
            self.log_result("Error Handling - Update Non-existent Book", False, f"Exception: {str(e)}")

        # Test deleting non-existent book
        try:
            response = self.session.delete(f"{API_URL}/books/{fake_id}")
            if response.status_code == 404:
                self.log_result("Error Handling - Delete Non-existent Book", True)
            else:
                self.log_result("Error Handling - Delete Non-existent Book", False, f"Expected 404, got {response.status_code}")
        except Exception as e:
            self.log_result("Error Handling - Delete Non-existent Book", False, f"Exception: {str(e)}")

    def run_comprehensive_tests(self):
        """Run all tests in sequence"""
        print("=" * 60)
        print("LIBRARIAN ASSISTANT BACKEND API TESTING")
        print("=" * 60)
        
        # 1. Health check
        if not self.test_health_check():
            print("❌ Health check failed - aborting tests")
            return
        
        print("\n--- STUDENT MANAGEMENT TESTS ---")
        
        # 2. Create students in different classes
        student1 = self.test_create_student("Emma", "Johnson", "7A")
        student2 = self.test_create_student("Liam", "Smith", "7A")
        student3 = self.test_create_student("Sophia", "Brown", "7B")
        student4 = self.test_create_student("Noah", "Davis", "8A")
        
        # 3. Test retrieving all students
        all_students = self.test_get_all_students()
        
        # 4. Test retrieving students by class
        class_7a_students = self.test_get_students_by_class("7A")
        class_7b_students = self.test_get_students_by_class("7B")
        class_8a_students = self.test_get_students_by_class("8A")
        
        # 5. Test getting all classes
        all_classes = self.test_get_all_classes()
        
        # 6. Test updating student (moving between classes)
        if student1:
            self.test_update_student(student1['id'], {"class_name": "8A", "first_name": "Emma-Updated"})
        
        print("\n--- BOOK MANAGEMENT TESTS ---")
        
        # 7. Create books with and without ISBN
        book1 = self.test_create_book("The Great Gatsby", "F. Scott Fitzgerald", "978-0-7432-7356-5")
        book2 = self.test_create_book("To Kill a Mockingbird", "Harper Lee")  # No ISBN
        book3 = self.test_create_book("1984", "George Orwell", "978-0-452-28423-4", False)  # Not available
        
        # 8. Test retrieving all books
        all_books = self.test_get_all_books()
        
        # 9. Test updating book availability
        if book3:
            self.test_update_book(book3['id'], {"available": True, "title": "1984 - Updated Edition"})
        
        print("\n--- ERROR HANDLING TESTS ---")
        
        # 10. Test error handling
        self.test_error_handling()
        
        print("\n--- DATA PERSISTENCE VERIFICATION ---")
        
        # 11. Verify data persistence by re-fetching
        final_students = self.test_get_all_students()
        final_books = self.test_get_all_books()
        
        if final_students is not None and final_books is not None:
            self.log_result("Data Persistence Verification", True)
        else:
            self.log_result("Data Persistence Verification", False, "Could not verify data persistence")
        
        print("\n--- CLEANUP TESTS ---")
        
        # 12. Test deletion (cleanup)
        for student_id in self.created_students[:2]:  # Delete first 2 students
            self.test_delete_student(student_id)
        
        for book_id in self.created_books[:1]:  # Delete first book
            self.test_delete_book(book_id)
        
        # Print final results
        print("\n" + "=" * 60)
        print("TEST RESULTS SUMMARY")
        print("=" * 60)
        print(f"✅ Passed: {self.test_results['passed']}")
        print(f"❌ Failed: {self.test_results['failed']}")
        
        if self.test_results['errors']:
            print("\nFAILED TESTS:")
            for error in self.test_results['errors']:
                print(f"  • {error}")
        
        success_rate = (self.test_results['passed'] / (self.test_results['passed'] + self.test_results['failed'])) * 100
        print(f"\nSuccess Rate: {success_rate:.1f}%")
        
        return self.test_results['failed'] == 0

if __name__ == "__main__":
    tester = LibrarianAPITester()
    success = tester.run_comprehensive_tests()
    sys.exit(0 if success else 1)