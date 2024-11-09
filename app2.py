import tkinter as tk
from tkinter import scrolledtext
import pyttsx3
import speech_recognition as sr
import threading
import time

# Önceden tanımlanmış cevaplar
predefined_answers = {
    "merhaba": "Merhaba! Size nasıl yardımcı olabilirim?",
    "nasılsın": "Ben bir yapay zeka olduğum için duygularım yok ama size yardımcı olmak için buradayım!",
    "deneme": "Rica ederim! Başka bir şey var mı?",
    "görüşürüz": "Görüşürüz! İyi günler!",
    "programı kapat": "Programı kapatıyorum.",
}

# Dinleme durumu
listening = False

def recognize_speech():
    global listening
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            update_status("Dinleniyor...", "blue")
            speak("Dinleniyor...")
            audio_data = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio_data, language='tr-TR')
            input_text.delete("1.0", tk.END)
            input_text.insert(tk.END, text)
            update_status("Yanıtlanıyor...", "orange")
            speak("Yanıtlanıyor...")
            process_command(text.lower())
        except sr.UnknownValueError:
            update_status("Sesi anlama hatası.", "red")
            speak("Sesi anlama hatası.")
        except sr.RequestError:
            update_status("API hatası.", "red")
            speak("API hatası.")
        except sr.WaitTimeoutError:
            update_status("Zaman aşımı hatası.", "red")
            speak("Zaman aşımı hatası.")
        finally:
            time.sleep(3)  # 3 saniye bekleme süresi
            if listening:
                recognize_speech()

def process_command(command):
    if "programı kapat" in command:
        answer = predefined_answers["programı kapat"]
        threading.Thread(target=speak, args=(answer, close_application)).start()
    else:
        ask_openai(command)

def ask_openai(command):
    answer = predefined_answers.get(command, "Üzgünüm, bu konuda bir cevabım yok.")
    update_output(answer)
    threading.Thread(target=speak, args=(answer,)).start()

def update_output(answer):
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, answer)
    output_text.config(state=tk.DISABLED)
    command_history.config(state=tk.NORMAL)
    command_history.insert(tk.END, f"Kullanıcı: {input_text.get('1.0', tk.END).strip()}\nYapay Zeka: {answer}\n\n")
    command_history.config(state=tk.DISABLED)
    command_history.see(tk.END)  # Komut geçmişini otomatik kaydır

def update_status(message, color):
    status_label.config(text=message, fg=color)
    root.update_idletasks()

def speak(text, callback=None):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
    if callback:
        callback()

def close_application():
    global listening
    listening = False
    speak("Program kapanıyor.")
    root.after(1000, root.destroy)  # Programın kapanma işlemini biraz geciktirir

def start_listening():
    global listening
    listening = True
    threading.Thread(target=speak, args=("Merhaba Kaan, sana nasıl yardımcı olabilirim?",)).start()
    root.after(5000, recognize_speech)  # 5 saniye bekleme süresi ve sonra dinlemeye başla

# Ana pencereyi oluştur
root = tk.Tk()
root.title("Sesli Komut Uygulaması")
root.geometry("700x600")
root.resizable(False, False)

# Başlık
title_label = tk.Label(root, text="Sesli Komut Uygulaması", font=("Helvetica", 16, "bold"))
title_label.pack(pady=10)

# Kullanıcı giriş alanı
input_label = tk.Label(root, text="Sesli komutla sorgulayın:", font=("Helvetica", 12))
input_label.pack(pady=5)

input_text = tk.Text(root, height=5, width=60, font=("Helvetica", 12))
input_text.pack(pady=10)

# Yanıt alanı
output_label = tk.Label(root, text="Yanıt:", font=("Helvetica", 12))
output_label.pack(pady=5)

output_text = scrolledtext.ScrolledText(root, height=5, width=60, font=("Helvetica", 12), state=tk.DISABLED)
output_text.pack(pady=10)

# Komut geçmişi
command_history = scrolledtext.ScrolledText(root, height=10, width=60, font=("Helvetica", 10), state=tk.DISABLED)
command_history.pack(pady=10)

# Durum etiketi
status_label = tk.Label(root, text="Dinlenmeye hazır...", font=("Helvetica", 10, "italic"), fg="green")
status_label.pack(pady=5)

# Dinlemeyi başlat
root.after(1000, start_listening)

# Ana döngüyü başlat
root.mainloop()
