Culla, Clark Cedric C. ACP-FINAL-PROJECT
# Leastahan

Leastahan is a Python-based task management application built with a graphical user interface (GUI) using Tkinter. It allows users to manage personalized to-do lists, complete with the ability to add, view, mark, and delete items. The data is stored in an SQLite database, ensuring persistence across sessions.

---

## Features

- **User Management**:
  - Users are identified by their names.
  - Each user has a unique list of items tied to their account.
  
- **Item Management**:
  - Add new tasks to your list.
  - View and mark tasks as completed.
  - Delete tasks from your list.
  
- **Database Integration**:
  - All data is stored in an SQLite database for persistence.

- **Progress Tracking**:
  - Track the percentage of completed tasks using a progress bar.

- **Responsive GUI**:
  - Intuitive, user-friendly interface with Tkinter.

---

## Project Structure

1. **Database Setup**:
   - Creates `users` and `items` tables in an SQLite database.
   - Stores user information and task details, including their completion status.

2. **Main Window**:
   - Displays options to add tasks or view/manage lists.

3. **Core Functions**:
   - **Add User**: Registers a new user or fetches an existing one.
   - **Add Task**: Adds a task to the logged-in user's list.
   - **View List**: Displays all tasks with options to mark as completed or delete.
   - **Delete Task**: Removes a task from the database and the list.
   - **Update Progress**: Dynamically calculates the completion percentage of tasks.

4. **Tkinter GUI**:
   - Main interface with buttons and input fields for seamless interaction.
   - Secondary windows for viewing and managing task lists.

---

## How to Use

### 1. Prerequisites
- Python 3.7 or higher
- SQLite3 (usually included with Python installations)

### 2. Installation
1. Clone or download the repository.
2. Ensure the required libraries are installed:
   ```bash
   pip install tk
