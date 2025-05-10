import tkinter as tk
import difflib
from tkinter import messagebox

def load_words_from_file():
    filename = "arabic_words.txt"
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        messagebox.showerror("خطأ", f"ملف القاموس غير موجود!\nالرجاء إنشاء ملف '{filename}'")
        return []
    except Exception as e:
        messagebox.showerror("خطأ", f"حدث خطأ أثناء قراءة الملف: {str(e)}")
        return []

def check_spelling():
    word = enter_text.get().strip()
    if not word:
        messagebox.showwarning("تحذير", "الرجاء إدخال كلمة أولاً")
        return

    arabic_words = load_words_from_file()
    if not arabic_words:
        return

    suggestions = difflib.get_close_matches(word, arabic_words, n=3, cutoff=0.6)

    if word in arabic_words:
        cs.config(text="✔️ الكلمة صحيحة")
        spell.config(text="")
    elif suggestions:
        cs.config(text="✏️ التصحيحات المقترحة:")
        spell.config(text="، ".join(suggestions))
    else:
        cs.config(text="❌ لا يوجد اقتراح:")
        spell.config(text="")

def clear_fields():
    enter_text.delete(0, tk.END)
    cs.config(text="")
    spell.config(text="")

# واجهة المستخدم
root = tk.Tk()
root.title("--Arabic Spelling Checker--")
root.geometry("800x500")
root.config(background="#123458")

heading = tk.Label(root, text="*Spelling Checker*", font=("Trebuchet MS", 30, "bold"), bg="#123458", fg="#D8EFD3")
heading.pack(pady=(50, 0))

enter_text = tk.Entry(root, justify="center", width=30, font=("poppins", 25), bg="white", border=2)
enter_text.pack(pady=10)
enter_text.focus()

button_frame = tk.Frame(root, bg="#123458")
button_frame.pack(pady=10)

check_button = tk.Button(button_frame, text="check", command=check_spelling, font=("arial", 20, "bold"), fg="white", bg="#C70039", width=10)
check_button.grid(row=0, column=0, padx=10)

clear_button = tk.Button(button_frame, text="clear", command=clear_fields, font=("arial", 20, "bold"), fg="white", bg="#555555", width=10)
clear_button.grid(row=0, column=1, padx=10)

cs = tk.Label(root, text="", font=("poppins", 20, "bold"), bg="#123458", fg="#D8EFD3")
cs.pack(pady=(30, 5))

spell = tk.Label(root, font=("poppins", 20, "bold"), bg="#123458", fg="#D8EFD3", wraplength=600, justify="center")
spell.pack()

root.mainloop()