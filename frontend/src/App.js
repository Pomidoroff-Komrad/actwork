import React, { useState, useEffect } from "react";
import "./App.css";
import axios from "axios";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Component for adding new class
const AddClassModal = ({ isOpen, onClose, onAdd }) => {
  const [className, setClassName] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(`${API}/classes`, {
        name: className
      });
      onAdd(className);
      setClassName("");
      onClose();
    } catch (error) {
      console.error("Error adding class:", error);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-96">
        <h2 className="text-xl font-bold mb-4">Add New Class</h2>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2">
              Class Name
            </label>
            <input
              type="text"
              value={className}
              onChange={(e) => setClassName(e.target.value)}
              className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:border-blue-500"
              placeholder="e.g., 7A, 7B, 8C"
              required
            />
          </div>
          <div className="flex justify-end space-x-2">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600"
            >
              Add Class
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

// Component for adding students
const AddStudentModal = ({ isOpen, onClose, onAdd }) => {
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [className, setClassName] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(`${API}/students`, {
        first_name: firstName,
        last_name: lastName,
        class_name: className
      });
      onAdd(response.data);
      setFirstName("");
      setLastName("");
      setClassName("");
      onClose();
    } catch (error) {
      console.error("Error adding student:", error);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg p-6 w-96">
        <h2 className="text-xl font-bold mb-4">Add New Student</h2>
        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2">
              First Name
            </label>
            <input
              type="text"
              value={firstName}
              onChange={(e) => setFirstName(e.target.value)}
              className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:border-blue-500"
              required
            />
          </div>
          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2">
              Last Name
            </label>
            <input
              type="text"
              value={lastName}
              onChange={(e) => setLastName(e.target.value)}
              className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:border-blue-500"
              required
            />
          </div>
          <div className="mb-4">
            <label className="block text-gray-700 text-sm font-bold mb-2">
              Class
            </label>
            <input
              type="text"
              value={className}
              onChange={(e) => setClassName(e.target.value)}
              className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:border-blue-500"
              placeholder="e.g., 7A, 7B"
              required
            />
          </div>
          <div className="flex justify-end space-x-2">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
            >
              Add Student
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

// Component for book management
const BookPanel = ({ isOpen, onClose }) => {
  const [books, setBooks] = useState([]);
  const [newBook, setNewBook] = useState({ title: "", author: "", isbn: "" });
  const [editingBook, setEditingBook] = useState(null);

  useEffect(() => {
    if (isOpen) {
      fetchBooks();
    }
  }, [isOpen]);

  const fetchBooks = async () => {
    try {
      const response = await axios.get(`${API}/books`);
      setBooks(response.data);
    } catch (error) {
      console.error("Error fetching books:", error);
    }
  };

  const handleAddBook = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(`${API}/books`, newBook);
      setBooks([...books, response.data]);
      setNewBook({ title: "", author: "", isbn: "" });
    } catch (error) {
      console.error("Error adding book:", error);
    }
  };

  const handleDeleteBook = async (bookId) => {
    try {
      await axios.delete(`${API}/books/${bookId}`);
      setBooks(books.filter(book => book.id !== bookId));
    } catch (error) {
      console.error("Error deleting book:", error);
    }
  };

  const handleEditBook = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.put(`${API}/books/${editingBook.id}`, editingBook);
      setBooks(books.map(book => book.id === editingBook.id ? response.data : book));
      setEditingBook(null);
    } catch (error) {
      console.error("Error updating book:", error);
    }
  };

  return (
    <div className={`fixed top-0 right-0 h-full w-96 bg-white shadow-2xl transform transition-transform duration-300 z-40 ${
      isOpen ? 'translate-x-0' : 'translate-x-full'
    }`}>
      <div className="p-6 h-full overflow-y-auto">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold text-gray-800">Books Library</h2>
          <button
            onClick={onClose}
            className="text-gray-500 hover:text-gray-700 text-2xl"
          >
            ×
          </button>
        </div>

        {/* Add Book Form */}
        <form onSubmit={handleAddBook} className="mb-6 bg-gray-50 p-4 rounded-lg">
          <h3 className="text-lg font-semibold mb-3">Add New Book</h3>
          <input
            type="text"
            placeholder="Book Title"
            value={newBook.title}
            onChange={(e) => setNewBook({...newBook, title: e.target.value})}
            className="w-full px-3 py-2 border rounded-lg mb-2 focus:outline-none focus:border-blue-500"
            required
          />
          <input
            type="text"
            placeholder="Author"
            value={newBook.author}
            onChange={(e) => setNewBook({...newBook, author: e.target.value})}
            className="w-full px-3 py-2 border rounded-lg mb-2 focus:outline-none focus:border-blue-500"
            required
          />
          <input
            type="text"
            placeholder="ISBN (optional)"
            value={newBook.isbn}
            onChange={(e) => setNewBook({...newBook, isbn: e.target.value})}
            className="w-full px-3 py-2 border rounded-lg mb-3 focus:outline-none focus:border-blue-500"
          />
          <button
            type="submit"
            className="w-full bg-green-500 text-white py-2 rounded-lg hover:bg-green-600"
          >
            Add Book
          </button>
        </form>

        {/* Books List */}
        <div className="space-y-3">
          <h3 className="text-lg font-semibold">All Books</h3>
          {books.map((book) => (
            <div key={book.id} className="border rounded-lg p-3 bg-gray-50">
              {editingBook && editingBook.id === book.id ? (
                <form onSubmit={handleEditBook}>
                  <input
                    type="text"
                    value={editingBook.title}
                    onChange={(e) => setEditingBook({...editingBook, title: e.target.value})}
                    className="w-full px-2 py-1 border rounded mb-2"
                  />
                  <input
                    type="text"
                    value={editingBook.author}
                    onChange={(e) => setEditingBook({...editingBook, author: e.target.value})}
                    className="w-full px-2 py-1 border rounded mb-2"
                  />
                  <input
                    type="text"
                    value={editingBook.isbn || ""}
                    onChange={(e) => setEditingBook({...editingBook, isbn: e.target.value})}
                    className="w-full px-2 py-1 border rounded mb-2"
                    placeholder="ISBN"
                  />
                  <div className="flex space-x-2">
                    <button type="submit" className="px-3 py-1 bg-blue-500 text-white rounded text-sm">
                      Save
                    </button>
                    <button
                      type="button"
                      onClick={() => setEditingBook(null)}
                      className="px-3 py-1 bg-gray-500 text-white rounded text-sm"
                    >
                      Cancel
                    </button>
                  </div>
                </form>
              ) : (
                <div>
                  <h4 className="font-semibold">{book.title}</h4>
                  <p className="text-gray-600">by {book.author}</p>
                  {book.isbn && <p className="text-sm text-gray-500">ISBN: {book.isbn}</p>}
                  <p className="text-sm">{book.available ? "Available" : "Checked out"}</p>
                  <div className="flex space-x-2 mt-2">
                    <button
                      onClick={() => setEditingBook(book)}
                      className="px-3 py-1 bg-blue-500 text-white rounded text-sm hover:bg-blue-600"
                    >
                      Edit
                    </button>
                    <button
                      onClick={() => handleDeleteBook(book.id)}
                      className="px-3 py-1 bg-red-500 text-white rounded text-sm hover:bg-red-600"
                    >
                      Delete
                    </button>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

// Main App Component
function App() {
  const [classes, setClasses] = useState([]);
  const [selectedClass, setSelectedClass] = useState(null);
  const [students, setStudents] = useState([]);
  const [isAddStudentModalOpen, setIsAddStudentModalOpen] = useState(false);
  const [isAddClassModalOpen, setIsAddClassModalOpen] = useState(false);
  const [isBookPanelOpen, setIsBookPanelOpen] = useState(false);
  const [editingStudent, setEditingStudent] = useState(null);
  const [stats, setStats] = useState({
    total_students: 0,
    total_books: 0,
    available_books: 0,
    total_classes: 0,
    class_counts: {}
  });

  useEffect(() => {
    fetchClasses();
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const response = await axios.get(`${API}/stats`);
      setStats(response.data);
    } catch (error) {
      console.error("Error fetching stats:", error);
    }
  };

  const fetchClasses = async () => {
    try {
      const response = await axios.get(`${API}/classes`);
      setClasses(response.data.classes);
    } catch (error) {
      console.error("Error fetching classes:", error);
    }
  };

  const fetchStudentsByClass = async (className) => {
    try {
      const response = await axios.get(`${API}/students/class/${className}`);
      setStudents(response.data);
      setSelectedClass(className);
    } catch (error) {
      console.error("Error fetching students:", error);
    }
  };

  const handleAddStudent = (newStudent) => {
    if (selectedClass === newStudent.class_name) {
      setStudents([...students, newStudent]);
    }
    if (!classes.includes(newStudent.class_name)) {
      setClasses([...classes, newStudent.class_name]);
    }
    // Refresh stats when a new student is added
    fetchStats();
  };

  const handleAddClass = (newClassName) => {
    if (!classes.includes(newClassName)) {
      setClasses([...classes, newClassName]);
    }
    // Refresh stats when a new class is added
    fetchStats();
  };

  const handleDeleteStudent = async (studentId) => {
    try {
      await axios.delete(`${API}/students/${studentId}`);
      setStudents(students.filter(student => student.id !== studentId));
      // Refresh stats when a student is deleted
      fetchStats();
    } catch (error) {
      console.error("Error deleting student:", error);
    }
  };

  const handleUpdateStudent = async (studentId, updates) => {
    try {
      const response = await axios.put(`${API}/students/${studentId}`, updates);
      setStudents(students.map(student => student.id === studentId ? response.data : student));
      setEditingStudent(null);
      // Refresh classes if class was changed
      fetchClasses();
    } catch (error) {
      console.error("Error updating student:", error);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">📚 Librarian Assistant</h1>
              <p className="text-gray-600">Manage students and books efficiently</p>
            </div>
            <div className="flex space-x-3">
              <button
                onClick={() => setIsAddClassModalOpen(true)}
                className="bg-green-600 hover:bg-green-700 text-white font-bold py-3 px-6 rounded-lg transition duration-200"
              >
                ➕ Add Class
              </button>
              <button
                onClick={() => setIsAddStudentModalOpen(true)}
                className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg transition duration-200"
              >
                👤 Add Student
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Stats Bar */}
      <div className="bg-gradient-to-r from-blue-500 to-purple-600 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
            <div>
              <div className="text-2xl font-bold">{stats.total_students}</div>
              <div className="text-blue-100">Total Students</div>
            </div>
            <div>
              <div className="text-2xl font-bold">{stats.total_classes}</div>
              <div className="text-blue-100">Classes</div>
            </div>
            <div>
              <div className="text-2xl font-bold">{stats.total_books}</div>
              <div className="text-blue-100">Total Books</div>
            </div>
            <div>
              <div className="text-2xl font-bold">{stats.available_books}</div>
              <div className="text-blue-100">Available Books</div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {!selectedClass ? (
          <div>
            <h2 className="text-2xl font-bold text-gray-800 mb-6">Select a Class</h2>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
              {classes.map((className) => (
                <div
                  key={className}
                  onClick={() => fetchStudentsByClass(className)}
                  className="bg-white rounded-xl shadow-lg p-6 cursor-pointer transform hover:scale-105 transition duration-200 hover:shadow-xl border-2 border-transparent hover:border-blue-300"
                >
                  <div className="text-center">
                    <div className="text-4xl mb-3">🎓</div>
                    <h3 className="text-xl font-bold text-gray-800">{className}</h3>
                    <div className="mt-2">
                      <span className="inline-block bg-blue-100 text-blue-800 text-sm px-3 py-1 rounded-full">
                        {stats.class_counts[className] || 0} students
                      </span>
                    </div>
                    <p className="text-gray-600 mt-2 text-sm">Click to view students</p>
                  </div>
                </div>
              ))}
              {classes.length === 0 && (
                <div className="col-span-full text-center py-12">
                  <div className="text-6xl mb-4">📝</div>
                  <h3 className="text-xl font-semibold text-gray-600">No classes yet</h3>
                  <p className="text-gray-500 mb-4">Create your first class to get started</p>
                  <button
                    onClick={() => setIsAddClassModalOpen(true)}
                    className="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded-lg transition duration-200"
                  >
                    ➕ Add First Class
                  </button>
                </div>
              )}
            </div>
          </div>
        ) : (
          <div>
            <div className="flex justify-between items-center mb-6">
              <div>
                <button
                  onClick={() => setSelectedClass(null)}
                  className="text-blue-600 hover:text-blue-800 font-semibold mb-2"
                >
                  ← Back to Classes
                </button>
                <h2 className="text-2xl font-bold text-gray-800">Class {selectedClass}</h2>
              </div>
            </div>
            
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {students.map((student) => (
                <div key={student.id} className="bg-white rounded-lg shadow-lg p-4">
                  {editingStudent && editingStudent.id === student.id ? (
                    <div>
                      <input
                        type="text"
                        value={editingStudent.first_name}
                        onChange={(e) => setEditingStudent({...editingStudent, first_name: e.target.value})}
                        className="w-full px-2 py-1 border rounded mb-2"
                        placeholder="First Name"
                      />
                      <input
                        type="text"
                        value={editingStudent.last_name}
                        onChange={(e) => setEditingStudent({...editingStudent, last_name: e.target.value})}
                        className="w-full px-2 py-1 border rounded mb-2"
                        placeholder="Last Name"
                      />
                      <input
                        type="text"
                        value={editingStudent.class_name}
                        onChange={(e) => setEditingStudent({...editingStudent, class_name: e.target.value})}
                        className="w-full px-2 py-1 border rounded mb-2"
                        placeholder="Class"
                      />
                      <div className="flex space-x-2">
                        <button
                          onClick={() => handleUpdateStudent(student.id, {
                            first_name: editingStudent.first_name,
                            last_name: editingStudent.last_name,
                            class_name: editingStudent.class_name
                          })}
                          className="px-3 py-1 bg-blue-500 text-white rounded text-sm"
                        >
                          Save
                        </button>
                        <button
                          onClick={() => setEditingStudent(null)}
                          className="px-3 py-1 bg-gray-500 text-white rounded text-sm"
                        >
                          Cancel
                        </button>
                      </div>
                    </div>
                  ) : (
                    <div>
                      <h3 className="text-lg font-semibold">{student.first_name} {student.last_name}</h3>
                      <p className="text-gray-600">Class: {student.class_name}</p>
                      <div className="flex space-x-2 mt-3">
                        <button
                          onClick={() => setEditingStudent(student)}
                          className="px-3 py-1 bg-blue-500 text-white rounded text-sm hover:bg-blue-600"
                        >
                          Edit
                        </button>
                        <button
                          onClick={() => handleDeleteStudent(student.id)}
                          className="px-3 py-1 bg-red-500 text-white rounded text-sm hover:bg-red-600"
                        >
                          Delete
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              ))}
              {students.length === 0 && (
                <div className="col-span-full text-center py-12">
                  <div className="text-6xl mb-4">👥</div>
                  <h3 className="text-xl font-semibold text-gray-600">No students in this class</h3>
                  <p className="text-gray-500">Add students to get started</p>
                </div>
              )}
            </div>
          </div>
        )}
      </main>

      {/* Books Panel Arrow */}
      <button
        onClick={() => setIsBookPanelOpen(true)}
        className="fixed top-1/2 right-0 transform -translate-y-1/2 bg-green-600 hover:bg-green-700 text-white p-3 rounded-l-lg shadow-lg z-30"
      >
        📚 →
      </button>

      {/* Modals and Panels */}
      <AddStudentModal 
        isOpen={isAddStudentModalOpen}
        onClose={() => setIsAddStudentModalOpen(false)}
        onAdd={handleAddStudent}
      />
      
      <BookPanel 
        isOpen={isBookPanelOpen}
        onClose={() => setIsBookPanelOpen(false)}
      />

      {/* Overlay */}
      {isBookPanelOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-30 z-30"
          onClick={() => setIsBookPanelOpen(false)}
        />
      )}
    </div>
  );
}

export default App;