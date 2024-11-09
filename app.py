#api ile cevap veren uygulama

import tkinter as tk
from tkinter import scrolledtext
import openai

# OpenAI API anahtarınızı buraya ekleyin
openai.api_key = 'API'

def ask_openai():
    user_input = input_text.get("1.0", tk.END).strip()
    if not user_input:
        return
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": user_input}
            ]
        )
        
        answer = response.choices[0].message['content'].strip()
        output_text.config(state=tk.NORMAL)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, answer)
        output_text.config(state=tk.DISABLED)
    except Exception as e:
        output_text.config(state=tk.NORMAL)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, f"Error: {e}")
        output_text.config(state=tk.DISABLED)

# Ana pencereyi oluştur
root = tk.Tk()
root.title("AI Soru Cevap Uygulaması")

# Kullanıcı giriş alanı
input_label = tk.Label(root, text="Sorunuzu yazın:")
input_label.pack(pady=5)

input_text = tk.Text(root, height=10, width=50)
input_text.pack(pady=5)

# Sor butonu
ask_button = tk.Button(root, text="Sor", command=ask_openai)
ask_button.pack(pady=5)

# Yanıt alanı
output_label = tk.Label(root, text="Yanıt:")
output_label.pack(pady=5)

output_text = scrolledtext.ScrolledText(root, height=10, width=50, state=tk.DISABLED)
output_text.pack(pady=5)

# Ana döngüyü başlat
root.mainloop()
