import sqlite3
conn = sqlite3.connect('students.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER,
        grade TEXT
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        date TEXT,
        status TEXT CHECK(status IN ('Present', 'Absent')),
        FOREIGN KEY (student_id) REFERENCES students(id)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS grades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        subject TEXT NOT NULL,
        grade TEXT NOT NULL,
        FOREIGN KEY (student_id) REFERENCES students(id)
    )
''')

conn.commit()

def add_student():
    name = input("Enter student name: ")
    age = int(input("Enter age: "))
    grade = input("Enter grade: ")
    cursor.execute("INSERT INTO students (name, age, grade) VALUES (?, ?, ?)", (name, age, grade))
    conn.commit()
    print("✅ Student added successfully!\n")

def view_students():
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    if rows:
        print("\n📋 Student List:")
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}, Grade: {row[3]}")
        print()
    else:
        print("📭 No student records found.\n")

def update_student():
    student_id = int(input("Enter student ID to update: "))
    name = input("Enter new name: ")
    age = int(input("Enter new age: "))
    grade = input("Enter new grade: ")
    cursor.execute("UPDATE students SET name = ?, age = ?, grade = ? WHERE id = ?", (name, age, grade, student_id))
    if cursor.rowcount == 0:
        print("❌ Student not found.\n")
    else:
        conn.commit()
        print("✅ Student updated successfully!\n")

def delete_student():
    student_id = int(input("Enter student ID to delete: "))
    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
    if cursor.rowcount == 0:
        print("❌ Student not found.\n")
    else:
        conn.commit()
        print("🗑️ Student deleted successfully!\n")

def search_student():
    student_id = int(input("Enter student ID to search: "))
    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    row = cursor.fetchone()
    if row:
        print(f"🔍 Found: ID: {row[0]}, Name: {row[1]}, Age: {row[2]}, Grade: {row[3]}\n")
    else:
        print("❌ Student not found.\n")

def mark_attendance():
    student_id = int(input("Enter student ID: "))
    date = input("Enter date (YYYY-MM-DD): ")
    status = input("Enter status (Present/Absent): ").capitalize()
    if status not in ['Present', 'Absent']:
        print("❌ Invalid status. Use 'Present' or 'Absent'.")
        return
    cursor.execute("INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)",
                   (student_id, date, status))
    conn.commit()
    print("✅ Attendance recorded.\n")

def view_attendance():
    student_id = int(input("Enter student ID to view attendance: "))
    cursor.execute("SELECT date, status FROM attendance WHERE student_id = ? ORDER BY date", (student_id,))
    rows = cursor.fetchall()
    if rows:
        print(f"\n📅 Attendance for Student ID {student_id}:")
        for date, status in rows:
            print(f"{date}: {status}")
        print()
    else:
        print("📭 No attendance records found.\n"
def add_grade():
    student_id = int(input("Enter student ID: "))
    subject = input("Enter subject: ")
    grade = input("Enter grade (e.g., A, B, C): ").upper()
    cursor.execute("INSERT INTO grades (student_id, subject, grade) VALUES (?, ?, ?)",
                   (student_id, subject, grade))
    conn.commit()
    print("✅ Grade recorded.\n")

def view_grades():
    student_id = int(input("Enter student ID to view grades: "))
    cursor.execute("SELECT subject, grade FROM grades WHERE student_id = ?", (student_id,))
    rows = cursor.fetchall()
    if rows:
        print(f"\n📊 Grades for Student ID {student_id}:")
        for subject, grade in rows:
            print(f"{subject}: {grade}")
        print()
    else:
        print("📭 No grades found.\n")
def main():
    while True:
        print("📚 Student Management System")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Update Student")
        print("4. Delete Student")
        print("5. Search Student")
        print("6. Mark Attendance")
        print("7. View Attendance")
        print("8. Add Grade")
        print("9. View Grades")
        print("10. Exit")

        choice = input("Choose an option: ")
        print()

        if choice == '1':
            add_student()
        elif choice == '2':
            view_students()
        elif choice == '3':
            update_student()
        elif choice == '4':
            delete_student()
        elif choice == '5':
            search_student()
        elif choice == '6':
            mark_attendance()
        elif choice == '7':
            view_attendance()
        elif choice == '8':
            add_grade()
        elif choice == '9':
            view_grades()
        elif choice == '10':
            print("👋 Exiting... Goodbye!")
            break
        else:
            print("⚠️ Invalid choice. Please try again.\n")

if __name__ == '__main__':
    main()
    conn.close()
