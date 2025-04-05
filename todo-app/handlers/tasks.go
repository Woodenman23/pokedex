package handlers

import (
	"html/template"
	"net/http"
	"strconv"
	"todo-app/db"
	"todo-app/models"
)

var templates = template.Must(template.ParseGlob("templates/*.html"))

func Index(w http.ResponseWriter, r *http.Request) {
	rows, err := db.DB.Query("SELECT id, description, done FROM tasks")
	if err != nil {
		http.Error(w, "Failed to fetch tasks", http.StatusInternalServerError)
		return
	}
	defer rows.Close()

	var tasks []models.Task
	for rows.Next() {
		var task models.Task
		if err := rows.Scan(&task.ID, &task.Description, &task.Done); err != nil {
			http.Error(w, "Failed to scan tasks", http.StatusInternalServerError)
			return
		}
		tasks = append(tasks, task)
	}

	if err := templates.ExecuteTemplate(w, "index.html", tasks); err != nil {
		http.Error(w, "Failed to render template", http.StatusInternalServerError)
	}
}

func AddTask(w http.ResponseWriter, r *http.Request) {
	if r.Method != "POST" {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	description := r.FormValue("description")
	if description == "" {
		http.Error(w, "Description required", http.StatusBadRequest)
		return
	}

	result, err := db.DB.Exec("INSERT INTO tasks (description, done) VALUES (?, ?)", description, false)
	if err != nil {
		http.Error(w, "Failed to add task", http.StatusInternalServerError)
		return
	}

	id, err := result.LastInsertId()
	if err != nil {
		http.Error(w, "Failed to get task ID", http.StatusInternalServerError)
		return
	}

	task := models.Task{ID: int(id), Description: description, Done: false}
	if err := templates.ExecuteTemplate(w, "task", task); err != nil {
		http.Error(w, "Failed to render task", http.StatusInternalServerError)
	}
}

func ToggleTask(w http.ResponseWriter, r *http.Request) {
	if r.Method != "PUT" {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	idStr := r.URL.Path[len("/toggle/"):]
	id, err := strconv.Atoi(idStr)
	if err != nil {
		http.Error(w, "Invalid task ID", http.StatusBadRequest)
		return
	}

	// 1. Query the current done state from the DB
	var currentDone bool
	err = db.DB.QueryRow("SELECT done FROM tasks WHERE id = ?", id).Scan(&currentDone)
	if err != nil {
		http.Error(w, "Failed to fetch current task state", http.StatusInternalServerError)
		return
	}

	// 2. Invert the current done state
	newDone := !currentDone

	// 3. Update the DB with the new done state
	_, err = db.DB.Exec("UPDATE tasks SET done = ? WHERE id = ?", newDone, id)
	if err != nil {
		http.Error(w, "Failed to update task", http.StatusInternalServerError)
		return
	}

	// 4. Fetch the updated task from the DB
	var task models.Task
	err = db.DB.QueryRow("SELECT id, description, done FROM tasks WHERE id = ?", id).
		Scan(&task.ID, &task.Description, &task.Done)
	if err != nil {
		http.Error(w, "Failed to fetch updated task", http.StatusInternalServerError)
		return
	}

	// 5. Render the updated task using the named template "task"
	if err := templates.ExecuteTemplate(w, "task", task); err != nil {
		http.Error(w, "Failed to render task", http.StatusInternalServerError)
	}
}

func DeleteTask(w http.ResponseWriter, r *http.Request) {
	if r.Method != "DELETE" {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	idStr := r.URL.Path[len("/delete/"):]
	id, err := strconv.Atoi(idStr)
	if err != nil {
		http.Error(w, "Invalid task ID", http.StatusBadRequest)
		return
	}

	_, err = db.DB.Exec("DELETE FROM tasks WHERE id = ?", id)
	if err != nil {
		http.Error(w, "Failed to delete task", http.StatusInternalServerError)
		return
	}

	// Return a 200 OK with an empty body so HTMX will swap out (i.e., remove) the element
	w.WriteHeader(http.StatusOK)
	w.Write([]byte(""))
}
