import tkinter as tk
from tkinter import messagebox
import requests
import json
import os

class GitHubFinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GitHub User Finder")
        self.favorites_file = "favorites.json"
        
        # UI Элементы
        tk.Label(root, text="Введите логин GitHub:").pack(pady=5)
        self.entry = tk.Entry(root)
        self.entry.pack(pady=5)
        
        tk.Button(root, text="Найти", command=self.search_user).pack(pady=5)
        
        self.result_list = tk.Listbox(root, width=50)
        self.result_list.pack(pady=10)
        
        tk.Button(root, text="В избранное", command=self.add_to_favorites).pack(pady=5)

    def search_user(self):
        username = self.entry.get().strip()
        if not username:
            messagebox.showwarning("Ошибка", "Поле поиска не должно быть пустым!")
            return
        
        response = requests.get(f"https://github.com{username}")
        if response.status_code == 200:
            data = response.json()
            self.result_list.delete(0, tk.END)
            self.result_list.insert(tk.END, f"Login: {data['login']}")
            self.result_list.insert(tk.END, f"Name: {data.get('name')}")
            self.result_list.insert(tk.END, f"Repos: {data['public_repos']}")
        else:
            messagebox.showerror("Ошибка", "Пользователь не найден")

    def add_to_favorites(self):
        # Логика сохранения в JSON
        content = self.result_list.get(0)
        if not content: return
        
        fav_user = content.replace("Login: ", "")
        favs = self.load_favorites()
        if fav_user not in favs:
            favs.append(fav_user)
            with open(self.favorites_file, "w") as f:
                json.dump(favs, f)
            messagebox.showinfo("Успех", f"{fav_user} добавлен в избранное!")

    def load_favorites(self):
        if not os.path.exists(self.favorites_file): return []
        with open(self.favorites_file, "r") as f:
            return json.load(f)

if __name__ == "__main__":
    root = tk.Tk()
    app = GitHubFinderApp(root)
    root.mainloop()
