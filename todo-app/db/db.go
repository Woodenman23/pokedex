package db

import (
	"database/sql"
	_ "github.com/mattn/go-sqlite3"
	"log"
)

var DB *sql.DB // pointer to empty DB object

func InitDB() {
	var err error
	DB, err = sql.Open("sqlite3", "./tasks.db") // open the ./tasks.db database using sqlite driver
	if err != nil {
		log.Fatal("Failed to open database:", err) // log.fatal takes multiple args and prints them
	}

	_, err = DB.Exec(`CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        description TEXT,
        done BOOLEAN
    )`)
	if err != nil {
		log.Fatal("Failed to create table:", err)
	}
}
