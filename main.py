
"""
=========================================================
          STUDENT MANAGEMENT SYSTEM
=========================================================
Features:
1. Add student
2. View all students
3. Search student
4. Update student
5. Delete student
6. Sort students
7. Filter students by course
8. Calculate grades
9. Display statistics
10. Export student data
11. Backup data
12. Restore backup
13. View top students
14. Search by marks
15. Attendance management
16. Delete all records
17. Exit

Storage: JSON file
Libraries: Python standard library only
"""

import json
import os
import shutil
from datetime import datetime
from dataclasses import dataclass
from typing import Callable


DATA_FILE = "students.json"
BACKUP_FILE = "students_backup.json"


# =========================================================
# BUTTON COMPONENT
# =========================================================

@dataclass
class Button:
    """Represent an actionable option in the command-line menu."""

    label: str
    shortcut: str
    on_click: Callable[[], None]
    enabled: bool = True

    def render(self):
        """Return the button's menu representation."""

        state = "" if self.enabled else " (disabled)"
        return f"{self.shortcut:>2}. {self.label}{state}"

    def click(self):
        """Run the button action when the button is enabled."""

        if not self.enabled:
            return False

        self.on_click()
        return True


# =========================================================
# STUDENT CLASS
# =========================================================

class Student:
    """Represent a student."""

    def __init__(
        self,
        student_id,
        name,
        age,
        course,
        email,
        marks=0,
        attendance=0
    ):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.course = course
        self.email = email
        self.marks = marks
        self.attendance = attendance

    def calculate_grade(self):
        """Calculate grade using marks."""

        if self.marks >= 90:
            return "A+"
        elif self.marks >= 80:
            return "A"
        elif self.marks >= 70:
            return "B"
        elif self.marks >= 60:
            return "C"
        elif self.marks >= 50:
            return "D"
        else:
            return "F"

    def to_dict(self):
        """Convert student object into dictionary."""

        return {
            "student_id": self.student_id,
            "name": self.name,
            "age": self.age,
            "course": self.course,
            "email": self.email,
            "marks": self.marks,
            "attendance": self.attendance,
            "grade": self.calculate_grade()
        }

    @staticmethod
    def from_dict(data):
        """Create a student object from dictionary."""

        return Student(
            student_id=data["student_id"],
            name=data["name"],
            age=data["age"],
            course=data["course"],
            email=data["email"],
            marks=data.get("marks", 0),
            attendance=data.get("attendance", 0)
        )


# =========================================================
# STUDENT MANAGER CLASS
# =========================================================

class StudentManager:
    """Manage student records and file storage."""

    def __init__(self):
        self.students = []
        self.load_data()

    # -----------------------------------------------------
    # LOAD DATA
    # -----------------------------------------------------

    def load_data(self):
        """Load saved students from JSON."""

        if not os.path.exists(DATA_FILE):
            self.students = []
            return

        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            self.students = [
                Student.from_dict(item)
                for item in data
            ]

        except (json.JSONDecodeError, KeyError, TypeError) as error:
            print("Could not load student data:", error)
            self.students = []

    # -----------------------------------------------------
    # SAVE DATA
    # -----------------------------------------------------

    def save_data(self):
        """Save students to JSON."""

        try:
            with open(DATA_FILE, "w", encoding="utf-8") as file:
                json.dump(
                    [student.to_dict() for student in self.students],
                    file,
                    indent=4
                )

            return True

        except OSError as error:
            print("Could not save data:", error)
            return False

    # -----------------------------------------------------
    # GENERATE ID
    # -----------------------------------------------------

    def generate_id(self):
        """Generate the next student ID."""

        if not self.students:
            return 1

        return max(
            student.student_id for student in self.students
        ) + 1

    # -----------------------------------------------------
    # GET INPUT
    # -----------------------------------------------------

    @staticmethod
    def get_integer(prompt, minimum=None, maximum=None):
        """Read and validate integer input."""

        while True:
            try:
                value = int(input(prompt))

                if minimum is not None and value < minimum:
                    print(f"Value must be at least {minimum}.")
                    continue

                if maximum is not None and value > maximum:
                    print(f"Value must not exceed {maximum}.")
                    continue

                return value

            except ValueError:
                print("Please enter a valid whole number.")

    @staticmethod
    def get_text(prompt):
        """Read non-empty text."""

        while True:
            value = input(prompt).strip()

            if value:
                return value

            print("This field cannot be empty.")

    @staticmethod
    def get_email(prompt):
        """Perform basic email validation."""

        while True:
            email = input(prompt).strip().lower()

            if (
                "@" in email
                and "." in email.split("@")[-1]
                and " " not in email
            ):
                return email

            print("Please enter a valid email address.")

    # -----------------------------------------------------
    # FIND STUDENT
    # -----------------------------------------------------

    def find_student(self, student_id):
        """Find a student by ID."""

        for student in self.students:
            if student.student_id == student_id:
                return student

        return None

    # -----------------------------------------------------
    # ADD STUDENT
    # -----------------------------------------------------

    def add_student(self):
        """Add a new student record."""

        print("\n========== ADD STUDENT ==========")

        student_id = self.generate_id()
        print("Generated Student ID:", student_id)

        name = self.get_text("Enter name: ")
        age = self.get_integer("Enter age: ", 1, 120)
        course = self.get_text("Enter course: ")
        email = self.get_email("Enter email: ")

        if any(s.email == email for s in self.students):
            print("This email is already registered.")
            return

        marks = self.get_integer("Enter marks (0-100): ", 0, 100)
        attendance = self.get_integer(
            "Enter attendance (0-100): ", 0, 100
        )

        student = Student(
            student_id,
            name,
            age,
            course,
            email,
            marks,
            attendance
        )

        self.students.append(student)

        if self.save_data():
            print("Student added successfully!")
        else:
            self.students.pop()
            print("Student was not saved.")

    # -----------------------------------------------------
    # DISPLAY ONE STUDENT
    # -----------------------------------------------------

    @staticmethod
    def display_student(student):
        """Display complete student details."""

        print("\n" + "-" * 45)
        print("Student ID :", student.student_id)
        print("Name       :", student.name)
        print("Age        :", student.age)
        print("Course     :", student.course)
        print("Email      :", student.email)
        print("Marks      :", student.marks)
        print("Grade      :", student.calculate_grade())
        print("Attendance :", f"{student.attendance}%")
        print("-" * 45)

    # -----------------------------------------------------
    # VIEW STUDENTS
    # -----------------------------------------------------

    def view_students(self):
        """Display all students."""

        print("\n========== ALL STUDENTS ==========")

        if not self.students:
            print("No student records found.")
            return

        for student in self.students:
            self.display_student(student)

        print("Total students:", len(self.students))

    # -----------------------------------------------------
    # SEARCH STUDENT
    # -----------------------------------------------------

    def search_student(self):
        """Search by ID, name, email, or course."""

        print("\n========== SEARCH STUDENT ==========")
        query = self.get_text("Enter ID, name, email or course: ")
        query = query.lower()

        results = [
            student
            for student in self.students
            if (
                query == str(student.student_id)
                or query in student.name.lower()
                or query in student.email.lower()
                or query in student.course.lower()
            )
        ]

        if not results:
            print("No matching students found.")
            return

        print("Matching students:", len(results))

        for student in results:
            self.display_student(student)

    # -----------------------------------------------------
    # UPDATE STUDENT
    # -----------------------------------------------------

    def update_student(self):
        """Update existing student details."""

        print("\n========== UPDATE STUDENT ==========")

        student_id = self.get_integer("Enter student ID: ", 1)
        student = self.find_student(student_id)

        if student is None:
            print("Student not found.")
            return

        self.display_student(student)

        print("Press Enter to keep the current value.")

        new_name = input(f"Name [{student.name}]: ").strip()
        new_course = input(f"Course [{student.course}]: ").strip()
        new_email = input(f"Email [{student.email}]: ").strip()

        if new_email:
            new_email = new_email.lower()

            if (
                "@" not in new_email
                or "." not in new_email.split("@")[-1]
                or " " in new_email
            ):
                print("Invalid email.")
                return

            if any(
                s.email == new_email and s is not student
                for s in self.students
            ):
                print("This email is already used by another student.")
                return

        new_age_text = input(f"Age [{student.age}]: ").strip()
        new_marks_text = input(f"Marks [{student.marks}]: ").strip()
        new_attendance_text = input(
            f"Attendance [{student.attendance}]: "
        ).strip()

        try:
            new_age = (
                int(new_age_text) if new_age_text else student.age
            )
            new_marks = (
                int(new_marks_text)
                if new_marks_text else student.marks
            )
            new_attendance = (
                int(new_attendance_text)
                if new_attendance_text else student.attendance
            )

            if not 1 <= new_age <= 120:
                raise ValueError("Age must be between 1 and 120.")

            if not 0 <= new_marks <= 100:
                raise ValueError("Marks must be between 0 and 100.")

            if not 0 <= new_attendance <= 100:
                raise ValueError(
                    "Attendance must be between 0 and 100."
                )

        except ValueError as error:
            print("Invalid input:", error)
            return

        old_data = student.to_dict()

        if new_name:
            student.name = new_name

        if new_course:
            student.course = new_course

        if new_email:
            student.email = new_email

        student.age = new_age
        student.marks = new_marks
        student.attendance = new_attendance

        if self.save_data():
            print("Student updated successfully!")
        else:
            restored = Student.from_dict(old_data)
            index = self.students.index(student)
            self.students[index] = restored
            print("Update could not be saved.")

    # -----------------------------------------------------
    # DELETE STUDENT
    # -----------------------------------------------------

    def delete_student(self):
        """Delete one student."""

        print("\n========== DELETE STUDENT ==========")

        student_id = self.get_integer("Enter student ID: ", 1)
        student = self.find_student(student_id)

        if student is None:
            print("Student not found.")
            return

        self.display_student(student)

        confirm = input("Delete this student? (yes/no): ").strip().lower()

        if confirm != "yes":
            print("Deletion cancelled.")
            return

        index = self.students.index(student)
        self.students.pop(index)

        if self.save_data():
            print("Student deleted successfully!")
        else:
            self.students.insert(index, student)
            print("Deletion could not be saved.")

    # -----------------------------------------------------
    # SORT STUDENTS
    # -----------------------------------------------------

    def sort_students(self):
        """Sort students by selected field."""

        print("\n1. Sort by name")
        print("2. Sort by marks")
        print("3. Sort by age")
        print("4. Sort by attendance")

        choice = input("Choose sorting option: ").strip()

        sort_options = {
            "1": ("name", lambda s: s.name.lower()),
            "2": ("marks", lambda s: s.marks),
            "3": ("age", lambda s: s.age),
            "4": ("attendance", lambda s: s.attendance)
        }

        if choice not in sort_options:
            print("Invalid sorting option.")
            return

        field, key_function = sort_options[choice]
        order = input("Ascending order? (yes/no): ").strip().lower()

        self.students.sort(
            key=key_function,
            reverse=(order != "yes")
        )

        print(f"Students sorted by {field}.")

        for student in self.students:
            self.display_student(student)

    # -----------------------------------------------------
    # FILTER BY COURSE
    # -----------------------------------------------------

    def filter_by_course(self):
        """Show students enrolled in a particular course."""

        course = self.get_text("Enter course name: ").lower()

        results = [
            student for student in self.students
            if course in student.course.lower()
        ]

        if not results:
            print("No students found for this course.")
            return

        for student in results:
            self.display_student(student)

    # -----------------------------------------------------
    # STATISTICS
    # -----------------------------------------------------

    def show_statistics(self):
        """Display class statistics."""

        print("\n========== STATISTICS ==========")

        if not self.students:
            print("No data available.")
            return

        total = len(self.students)
        average_marks = sum(s.marks for s in self.students) / total
        average_age = sum(s.age for s in self.students) / total
        average_attendance = (
            sum(s.attendance for s in self.students) / total
        )

        passed = sum(s.marks >= 40 for s in self.students)
        failed = total - passed

        print("Total students     :", total)
        print(f"Average marks      : {average_marks:.2f}")
        print(f"Average age        : {average_age:.2f}")
        print(f"Average attendance : {average_attendance:.2f}%")
        print("Passed students    :", passed)
        print("Failed students    :", failed)

        courses = {}

        for student in self.students:
            courses[student.course] = (
                courses.get(student.course, 0) + 1
            )

        print("\nCourse-wise count:")

        for course, count in sorted(courses.items()):
            print(f"{course}: {count}")

    # -----------------------------------------------------
    # TOP STUDENTS
    # -----------------------------------------------------

    def show_top_students(self):
        """Display top students by marks."""

        if not self.students:
            print("No student records found.")
            return

        count = self.get_integer(
            "How many top students do you want? ", 1
        )

        ranked_students = sorted(
            self.students,
            key=lambda s: s.marks,
            reverse=True
        )

        print("\n========== TOP STUDENTS ==========")

        for position, student in enumerate(
            ranked_students[:count], start=1
        ):
            print(
                f"{position}. {student.name} - "
                f"{student.marks} marks - "
                f"Grade {student.calculate_grade()}"
            )

    # -----------------------------------------------------
    # FILTER BY MARKS
    # -----------------------------------------------------

    def filter_by_marks(self):
        """Find students in a marks range."""

        minimum = self.get_integer("Minimum marks: ", 0, 100)
        maximum = self.get_integer("Maximum marks: ", 0, 100)

        if minimum > maximum:
            print("Minimum marks cannot exceed maximum marks.")
            return

        results = [
            s for s in self.students
            if minimum <= s.marks <= maximum
        ]

        if not results:
            print("No students found in this marks range.")
            return

        for student in results:
            self.display_student(student)

    # -----------------------------------------------------
    # ATTENDANCE
    # -----------------------------------------------------

    def update_attendance(self):
        """Update a student's attendance percentage."""

        student_id = self.get_integer("Enter student ID: ", 1)
        student = self.find_student(student_id)

        if student is None:
            print("Student not found.")
            return

        attendance = self.get_integer(
            "Enter new attendance (0-100): ", 0, 100
        )

        old_attendance = student.attendance
        student.attendance = attendance

        if self.save_data():
            print("Attendance updated successfully!")
        else:
            student.attendance = old_attendance
            print("Attendance could not be saved.")

    # -----------------------------------------------------
    # EXPORT DATA
    # -----------------------------------------------------

    def export_data(self):
        """Export student records to a timestamped JSON file."""

        filename = (
            "students_export_"
            + datetime.now().strftime("%Y%m%d_%H%M%S")
            + ".json"
        )

        try:
            with open(filename, "w", encoding="utf-8") as file:
                json.dump(
                    [s.to_dict() for s in self.students],
                    file,
                    indent=4
                )

            print("Data exported to:", filename)

        except OSError as error:
            print("Export failed:", error)

    # -----------------------------------------------------
    # BACKUP
    # -----------------------------------------------------

    def backup_data(self):
        """Create a backup of student records."""

        if not self.save_data():
            print("Could not save current data.")
            return

        try:
            shutil.copy2(DATA_FILE, BACKUP_FILE)
            print("Backup created successfully!")

        except OSError as error:
            print("Backup failed:", error)

    # -----------------------------------------------------
    # RESTORE BACKUP
    # -----------------------------------------------------

    def restore_backup(self):
        """Restore student data from the backup."""

        if not os.path.exists(BACKUP_FILE):
            print("No backup file exists.")
            return

        confirm = input(
            "Restore backup? Current records will be replaced (yes/no): "
        ).strip().lower()

        if confirm != "yes":
            print("Restore cancelled.")
            return

        try:
            with open(BACKUP_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            restored_students = [
                Student.from_dict(item) for item in data
            ]

            ids = [s.student_id for s in restored_students]
            emails = [s.email for s in restored_students]

            if len(ids) != len(set(ids)):
                print("Backup contains duplicate student IDs.")
                return

            if len(emails) != len(set(emails)):
                print("Backup contains duplicate email addresses.")
                return

            old_students = self.students
            self.students = restored_students

            if self.save_data():
                print("Backup restored successfully!")
            else:
                self.students = old_students

        except (OSError, json.JSONDecodeError, KeyError, TypeError) as error:
            print("Could not restore backup:", error)

    # -----------------------------------------------------
    # DELETE ALL STUDENTS
    # -----------------------------------------------------

    def delete_all_students(self):
        """Delete all records after confirmation."""

        if not self.students:
            print("No student records to delete.")
            return

        print("WARNING: This will delete every student record.")

        confirm = input(
            "Type DELETE ALL to confirm: "
        ).strip()

        if confirm != "DELETE ALL":
            print("Operation cancelled.")
            return

        old_students = self.students
        self.students = []

        if self.save_data():
            print("All student records deleted.")
        else:
            self.students = old_students
            print("Could not delete records.")

    # -----------------------------------------------------
    # MAIN MENU
    # -----------------------------------------------------

    def get_menu_buttons(self):
        """Build the buttons used by the main menu."""

        actions = [
            self.add_student,
            self.view_students,
            self.search_student,
            self.update_student,
            self.delete_student,
            self.sort_students,
            self.filter_by_course,
            self.show_statistics,
            self.show_top_students,
            self.filter_by_marks,
            self.update_attendance,
            self.export_data,
            self.backup_data,
            self.restore_backup,
            self.delete_all_students,
            lambda: None
        ]

        labels = [
            "Add Student",
            "View All Students",
            "Search Student",
            "Update Student",
            "Delete Student",
            "Sort Students",
            "Filter by Course",
            "Show Statistics",
            "Show Top Students",
            "Filter by Marks",
            "Update Attendance",
            "Export Data",
            "Create Backup",
            "Restore Backup",
            "Delete All Students",
            "Exit"
        ]

        return [
            Button(label, str(number), action)
            for number, (label, action) in enumerate(
                zip(labels, actions), start=1
            )
        ]

    def show_menu(self):
        """Display all available features."""

        print("\n" + "=" * 50)
        print("        STUDENT MANAGEMENT SYSTEM")
        print("=" * 50)

        for button in self.get_menu_buttons():
            print(button.render())

        print("=" * 50)

    # -----------------------------------------------------
    # RUN APPLICATION
    # -----------------------------------------------------

    def run(self):
        """Start the application loop."""

        print("\nWelcome to Student Management System!")

        while True:
            self.show_menu()
            choice = input("Enter your choice (1-16): ").strip()

            if choice == "16":
                print("Thank you for using Student Management System!")
                break

            button = next(
                (
                    menu_button
                    for menu_button in self.get_menu_buttons()
                    if menu_button.shortcut == choice
                ),
                None
            )

            if button is None:
                print("Invalid choice. Please choose from 1 to 16.")
                continue

            try:
                button.click()
            except (KeyboardInterrupt, EOFError):
                print("\nInput cancelled.")
            except Exception as error:
                print("An unexpected error occurred:", error)

            input("\nPress Enter to continue...")


# =========================================================
# APPLICATION ENTRY POINT
# =========================================================

def main():
    """Create the manager and run the application."""

    manager = StudentManager()
    manager.run()


if __name__ == "__main__":
    main()
