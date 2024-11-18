import requests
from tkinter import Tk, Label, Button, Text, messagebox
import random

# -----------------------------------
# وظائف الفحص
# -----------------------------------

# فحص الاتصال عبر SSL/TLS
def فحص_ssl_tls(url):
    try:
        # محاولة الاتصال بالموقع عبر HTTP
        print(f"Checking {url} for SSL/TLS connection...")
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return "The connection is properly encrypted via SSL/TLS."
        return f"The connection failed with status code: {response.status_code}."
    except requests.exceptions.SSLError:
        return "Warning: The SSL certificate is untrusted!"
    except requests.exceptions.RequestException as e:
        return f"Error during connection attempt: {e}"

# فحص الموقع
def فحص_الموقع(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        raise ValueError("Invalid URL format. The URL should start with 'http://' or 'https://'")
    
    # إجراء الفحص للموقع
    النتائج = []
    النتائج.append(فحص_ssl_tls(url))
    
    return النتائج

# -----------------------------------
# تغيير الألوان بشكل ديناميكي
# -----------------------------------

def تغيير_اللون():
    # قائمة من الألوان الممكنة
    ألوان = ["#0f0f0f", "#1c1c1c", "#232323", "#333333", "#444444", "#00FF00", "#00FFFF", "#FF00FF", "#FF0000", "#FFFF00"]
    
    # اختيار لون عشوائي من القائمة
    لون_عشوائي = random.choice(ألوان)
    
    # تغيير لون خلفية النافذة
    نافذة.configure(bg=لون_عشوائي)
    
    # تغيير لون النص في الواجهة
    for widget in نافذة.winfo_children():
        if isinstance(widget, Label) or isinstance(widget, Button):
            widget.configure(fg="white", bg=لون_عشوائي)
    
    # استدعاء الوظيفة بعد ثانية واحدة لتغيير اللون مرة أخرى
    نافذة.after(1000, تغيير_اللون)

# -----------------------------------
# واجهة المستخدم
# -----------------------------------
def تشغيل_الفحص():
    url = رابط_الموقع.get("1.0", "end-1c")  # الحصول على الرابط من الحقل النصي
    if not url.strip():
        messagebox.showwarning("Warning", "Please enter a website URL.")
        return

    try:
        نتائج = فحص_الموقع(url)
        شاشة_النتائج.delete("1.0", "end")  # تنظيف النتائج السابقة
        for نتيجة in نتائج:
            شاشة_النتائج.insert("end", نتيجة + "\n")
    except ValueError as ve:
        messagebox.showerror("Error", str(ve))
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Connection Error", f"Failed to connect: {str(e)}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# -----------------------------------
# إنشاء نافذة التطبيق
# -----------------------------------
نافذة = Tk()
نافذة.title("Web Test - Security Testing Tool")
نافذة.geometry("800x400")
نافذة.configure(bg="#333333")  # البداية بلون داكن

# إضافة تغيير الألوان بشكل ديناميكي
تغيير_اللون()  # بدء تغيير الألوان

# إضافة العنوان
Label(نافذة, text="Web Test - Security Testing Tool", font=("Arial", 20), fg="white", bg="#333333").pack(pady=10)

# إضافة معلومات المبرمج
Label(نافذة, text="Programmer: Ayham Alwdy", font=("Arial", 12), fg="gray", bg="#333333").pack()
Label(نافذة, text="Phone: 00963938627021", font=("Arial", 12), fg="gray", bg="#333333").pack()
Label(نافذة, text="About the Programmer:", font=("Arial", 12), fg="white", bg="#333333").pack(pady=5)
Label(نافذة, text="My name is Ayham, from Syria, currently living in Germany.", font=("Arial", 12), fg="gray", bg="#333333").pack()
Label(نافذة, text="I am studying Cybersecurity and working in VS Code.", font=("Arial", 12), fg="gray", bg="#333333").pack()

# حقل الإدخال للرابط (استخدام Text بدلاً من Entry)
Label(نافذة, text="Enter the website URL:", font=("Arial", 14), bg="#333333", fg="white").pack(pady=5)
رابط_الموقع = Text(نافذة, width=50, height=1, font=("Arial", 14))
رابط_الموقع.pack(pady=10)

# زر الفحص
زر_فحص = Button(نافذة, text="Scan Website", command=تشغيل_الفحص, font=("Arial", 14), bg="#00FF00", fg="black")
زر_فحص.pack(pady=10)

# منطقة عرض النتائج
شاشة_النتائج = Text(نافذة, width=90, height=15, font=("Arial", 12), bg="#222222", fg="white")
شاشة_النتائج.pack(pady=20)

# تشغيل التطبيق
نافذة.mainloop()
