import tkinter as tk
from tkinter import messagebox, ttk
import os

# --- የደህንነት መረጃ ---
USER_NAME = "demeke"
PASS_WORD = "1234"
FILE_NAME = "customers_list.txt"

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("DERESE GARMENT - Login")
        self.root.geometry("400x350")
        self.root.configure(bg="#f4f4f4")
        
        tk.Label(root, text="DERESE GARMENT", font=("Arial", 20, "bold"), fg="#28a745", bg="#f4f4f4").pack(pady=30)
        
        tk.Label(root, text="የተጠቃሚ ስም:", bg="#f4f4f4").pack()
        self.user_entry = tk.Entry(root, font=("Arial", 12))
        self.user_entry.pack(pady=5)
        
        tk.Label(root, text="ሚስጥራዊ ቁጥር:", bg="#f4f4f4").pack()
        self.pass_entry = tk.Entry(root, font=("Arial", 12), show="*")
        self.pass_entry.pack(pady=5)
        
        tk.Button(root, text="ግባ (Login)", command=self.check_login, bg="#28a745", fg="white", font=("Arial", 12, "bold"), width=15).pack(pady=25)

    def check_login(self):
        if self.user_entry.get() == USER_NAME and self.pass_entry.get() == PASS_WORD:
            self.root.destroy()
            start_main_app()
        else:
            messagebox.showerror("ስህተት", "የተጠቃሚ ስም ወይም ሚስጥራዊ ቁጥር ተሳስቷል!")

def start_main_app():
    # እዚህ ጋር የእርስዎ ዋና ኮድ (ባለፈው የሰራነው) ይቀጥላል
    main_root = tk.Tk()
    main_root.title("DERESE GARMENT - Main System")
    main_root.geometry("600x500")
    tk.Label(main_root, text="እንኳን ደህና መጡ! ስራዎን መቀጠል ይችላሉ።", font=("Arial", 14)).pack(pady=50)
    main_root.mainloop()

if __name__ == "__main__":
    login_root = tk.Tk()
    app = LoginWindow(login_root)
    login_root.mainloop()
