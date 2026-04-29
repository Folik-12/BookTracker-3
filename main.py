import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

class BookTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker")
        self.file_path = "books.json"
        self.books = self.load_data()

        # Интерфейс ввода
        tk.Label(root, text="Название:").grid(row=0, column=0)
        self.title_entry = tk.Entry(root)
        self.title_entry.grid(row=0, column=1)

        tk.Label(root, text="Автор:").grid(row=1, column=0)
        self.author_entry = tk.Entry(root)
        self.author_entry.grid(row=1, column=1)

        tk.Label(root, text="Жанр:").grid(row=2, column=0)
        self.genre_entry = tk.Entry(root)
        self.genre_entry.grid(row=2, column=1)

        tk.Label(root, text="Страниц:").grid(row=3, column=0)
        self.pages_entry = tk.Entry(root)
        self.pages_entry.grid(row=3, column=1)

        tk.Button(root, text="Добавить книгу", command=self.add_book).grid(row=4, column=0, columnspan=2, pady=10)

        # Фильтры
        tk.Label(root, text="Фильтр по жанру:").grid(row=5, column=0)
        self.filter_genre = tk.Entry(root)
        self.filter_genre.grid(row=5, column=1)
        
        tk.Button(root, text="Фильтровать", command=self.apply_filter).grid(row=6, column=0, columnspan=2)

        # Таблица
        self.tree = ttk.Treeview(root, columns=("Title", "Author", "Genre", "Pages"), show='headings')
        self.tree.heading("Title", text="Название")
        self.tree.heading("Author", text="Автор")
        self.tree.heading("Genre", text="Жанр")
        self.tree.heading("Pages", text="Страницы")
        self.tree.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

        self.update_table(self.books)

    def add_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        genre = self.genre_entry.get()
        pages = self.pages_entry.get()

        if not (title and author and genre and pages):
            messagebox.showerror("Ошибка", "Заполните все поля!")
            return

        try:
            pages = int(pages)
        except ValueError:
            messagebox.showerror("Ошибка", "Количество страниц должно быть числом!")
            return

        new_book = {"title": title, "author": author, "genre": genre, "pages": pages}
        self.books.append(new_book)
        self.save_data()
        self.update_table(self.books)
        messagebox.showinfo("Успех", "Книга добавлена!")

    def apply_filter(self):
        genre = self.filter_genre.get().lower()
        filtered = [b for b in self.books if genre in b['genre'].lower()]
        # Доп. фильтр: более 200 страниц (пример из ТЗ)
        filtered = [b for b in filtered if b['pages'] > 200]
        self.update_table(filtered)

    def update_table(self, data):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for book in data:
            self.tree.insert("", "end", values=(book['title'], book['author'], book['genre'], book['pages']))

    def save_data(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.books, f, ensure_ascii=False, indent=4)

    def load_data(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

if __name__ == "__main__":
    root = tk.Tk()
    app = BookTracker(root)
    root.mainloop()
