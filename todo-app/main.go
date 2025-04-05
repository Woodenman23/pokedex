package main

import (
	"fmt"
	"net/http"
	"todo-app/db"
	"todo-app/handlers"
)

func main() {
	db.InitDB()

	http.HandleFunc("/", handlers.Index)
	http.HandleFunc("/add", handlers.AddTask)
	http.HandleFunc("/toggle/", handlers.ToggleTask)
	http.HandleFunc("/delete/", handlers.DeleteTask)
	http.Handle("/static/", http.StripPrefix("/static/", http.FileServer(http.Dir("static"))))

	fmt.Println("Server started at :8082")
	http.ListenAndServe(":8082", nil)
}
