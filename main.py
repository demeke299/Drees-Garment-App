import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
import os
import unicodedata
from datetime import datetime
import webbrowser

# የፋይል ስም
FILE_NAME = "customers_list.txt"

# --- ዳታ የማስተዳደሪያ ተግባራት ---
def get_all_records():
    if not os.path.exists(FILE_NAME): return []
    try:
        with open(FILE_NAME, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except: return []

def save_all_records(records):
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        for r in records: f.write(r + "\n")

def normalize_text(text):
    if not text: return ""
    return unicodedata.normalize('NFC', text.strip())

# --- ዋና ስራዎች ---
current_idx = -1

def display_record(idx):
    global current_idx
    records = get_all_records()
    
    if 0 <= idx < len(records):
        current_idx = idx
        line = records[idx]
        parts = line.split(" | ")
        
        try:
            val = parts[0].split(": ")[1]
            label_id_val.config(text=val)
        except: pass
        
        for i, label_name in enumerate(labels_text):
            entries[i].delete(0, tk.END)
            for p in parts:
                if p.startswith(label_name + ": "):
                    entries[i].insert(0, p.replace(label_name + ": ", "", 1))
        
        for p in parts:
            if p.startswith("ሁኔታ: "):
                status_var.set(p.replace("ሁኔታ: ", "", 1))
    else:
        clear_fields()

def next_id():
    global current_idx
    records = get_all_records()
    if current_idx < len(records) - 1:
        display_record(current_idx + 1)
    else:
        clear_fields()
        label_id_val.config(text=str(len(records) + 1))

def prev_id():
    global current_idx
    if current_idx > 0:
        display_record(current_idx - 1)
    elif current_idx == -1: 
        records = get_all_records()
        if records: display_record(len(records) - 1)

def clear_fields():
    global current_idx
    records = get_all_records()
    current_idx = len(records)
    for e in entries: e.delete(0, tk.END)
    status_var.set("አልተሰራም")
    label_id_val.config(text=str(len(records) + 1))

def save_data():
    if not entries[0].get():
        messagebox.showerror("ስህተት", "እባክዎ ስም ያስገቡ!")
        return
    
    records = get_all_records()
    data = [f"ተ.ቁ: {len(records) + 1}"]
    for i, l in enumerate(labels_text):
        data.append(f"{l}: {entries[i].get()}")
    data.append(f"ሁኔታ: {status_var.get()}")
    
    with open(FILE_NAME, "a", encoding="utf-8") as f:
        f.write(" | ".join(data) + "\n")
    
    messagebox.showinfo("ተሳክቷል", "መረጃው ተመዝግቧል!")
    clear_fields()

def update_data():
    records = get_all_records()
    if 0 <= current_idx < len(records):
        parts = records[current_idx].split(" | ")
        orig_id = parts[0] 
        
        data = [orig_id]
        for i, l in enumerate(labels_text):
            data.append(f"{l}: {entries[i].get()}")
        data.append(f"ሁኔታ: {status_var.get()}")
        
        records[current_idx] = " | ".join(data)
        save_all_records(records)
        messagebox.showinfo("ተሳክቷል", "መረጃው ታድሷል!")
    else:
        messagebox.showwarning("ማስጠንቀቂያ", "መጀመሪያ የሚታደስ መረጃ ይምረጡ!")

def search_by_name():
    search_term = simpledialog.askstring("ፍለጋ", "የደንበኛ ስም ይጻፉ፡")
    if not search_term: return
    search_term = normalize_text(search_term).lower()
    records = get_all_records()
    for i, r in enumerate(records):
        if search_term in normalize_text(r).lower():
            display_record(i)
            return
    messagebox.showinfo("አልተገኘም", "የተፈለገው ደንበኛ የለም።")

def check_overdue():
    records = get_all_records()
    overdue_list = []
    today = datetime.now()
    for r in records:
        parts = r.split(" | ")
        try:
            date_p = [p for p in parts if "የቀጠሮ ቀን" in p]
            if date_p: # እዚህ ጋር የነበረው የገብ ስህተት ተስተካክሏል
                d_str = date_p[0].split(": ")[1].strip()
                for fmt in ('%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y'):
                    try:
                        d_obj = datetime.strptime(d_str, fmt)
                        if d_obj < today and "ተጠናቋል" not in r:
                            name = parts[1].split(": ")[1]
                            overdue_list.append(f"{name} ({d_str})")
                        break
                    except: continue
        except: continue
    if overdue_list: 
        messagebox.showwarning("ቀጠሮ ያለፈባቸው", "\n".join(overdue_list))
    else: 
        messagebox.showinfo("ሁኔታ", "ቀጠሮ ያለፈበት የለም።")

def show_income_report():
    records = get_all_records()
    paid, rem = 0.0, 0.0
    for r in records:
        for p in r.split(" | "):
            if "ቃብድ: " in p:
                try: paid += float(p.split(": ")[1])
                except: pass
            if "ቀሪ ሂሳብ: " in p:
                try: rem += float(p.split(": ")[1])
                except: pass
    messagebox.showinfo("ሪፖርት", f"የተሰበሰበ፡ {paid} ብር\nቀሪ፡ {rem} ብር\nጠቅላላ፡ {paid+rem} ብር")

def send_sms():
    name, phone, bal = entries[0].get(), entries[1].get(), entries[11].get()
    if not phone: 
        messagebox.showwarning("ስህተት", "ስልክ ቁጥር የለም!")
        return
    msg = f"ሰላም {name}፣ ስራው ተጠናቋል። ቀሪ ሂሳብ {bal} ብር ይዘው መጥተው መውሰድ ይችላሉ።"
    webbrowser.open(f"sms:{phone}?body={msg}")

# --- UI ---
root = tk.Tk()
root.title("DERESE GARMENT")
root.geometry("450x850")

# ሎጎውን ለማስገባት
try:
    img = tk.PhotoImage(file='garment_logo.png')
    root.iconphoto(False, img)
except:
    pass

tk.Label(root, text="DERESE GARMENT", font=("Arial", 20, "bold"), fg="#28a745").pack(pady=10)

canvas = tk.Canvas(root)
scroll = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
frame = tk.Frame(canvas)
canvas.create_window((0,0), window=frame, anchor="nw")
canvas.configure(yscrollcommand=scroll.set)
canvas.pack(side="left", fill="both", expand=True)
scroll.pack(side="right", fill="y")
frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Navigation
nav = tk.Frame(frame)
nav.pack(pady=10, fill="x")
tk.Button(nav, text=" < ", command=prev_id, width=10, bg="#eee").pack(side="left", padx=20)
label_id_val = tk.Label(nav, text=str(len(get_all_records())+1), font=("Arial", 22, "bold"), fg="red")
label_id_val.pack(side="left", expand=True)
tk.Button(nav, text=" > ", command=next_id, width=10, bg="#eee").pack(side="left", padx=20)

labels_text = ["የደንበኛ ስም", "ስልክ ቁጥር", "የትዕዛዝ ዓይነት", "ትከሻ", "ጡት", "ወገብ", "እጅጌ", "Upper ቁመት", "Lower ቁመት", "ጠቅላላ ዋጋ", "ቃብድ", "ቀሪ ሂሳብ", "የቀጠሮ ቀን"]
entries = []
for t in labels_text:
    r = tk.Frame(frame)
    r.pack(fill="x", pady=2, padx=20)
    tk.Label(r, text=t, width=14, anchor="w", font=("Arial", 10, "bold")).pack(side="left")
    e = tk.Entry(r, font=("Arial", 11), bd=1, relief="solid")
    e.pack(side="right", expand=True, fill="x")
    entries.append(e)

tk.Label(frame, text="የስፌት ሁኔታ፡", font=("Arial", 10, "bold")).pack(pady=(10,0))
status_var = tk.StringVar(value="አልተሰራም")
tk.OptionMenu(frame, status_var, "አልተሰራም", "በስፌት ላይ", "ተጠናቋል").pack(pady=5)

# Buttons
tk.Button(frame, text="አዲስ መዝገብ (Clear)", command=clear_fields, bg="#6c757d", fg="white", font=("Arial", 10, "bold"), pady=5).pack(fill="x", padx=40, pady=2)
tk.Button(frame, text="መዝግብ (Save)", command=save_data, bg="#28a745", fg="white", font=("Arial", 10, "bold"), pady=8).pack(fill="x", padx=40, pady=2)
tk.Button(frame, text="🔍 ፈልግ (Search)", command=search_by_name, bg="#17a2b8", fg="white", font=("Arial", 10, "bold"), pady=8).pack(fill="x", padx=40, pady=2)
tk.Button(frame, text="🔄 አድስ (Update)", command=update_data, bg="#007bff", fg="white", font=("Arial", 10, "bold"), pady=8).pack(fill="x", padx=40, pady=2)
tk.Button(frame, text="📊 ሪፖርት", command=show_income_report, bg="#6f42c1", fg="white", font=("Arial", 10, "bold"), pady=8).pack(fill="x", padx=40, pady=2)
tk.Button(frame, text="✉️ SMS ላክ", command=send_sms, bg="#fd7e14", fg="white", font=("Arial", 10, "bold"), pady=8).pack(fill="x", padx=40, pady=2)
tk.Button(frame, text="⚠️ ቀጠሮ ያለፈባቸው", command=check_overdue, bg="#ffc107", font=("Arial", 10, "bold"), pady=8).pack(fill="x", padx=40, pady=2)

root.mainloop()
