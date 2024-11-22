import argparse
import requests
import traceback
import logging

# -----------------------------------
# إعداد تسجيل الأخطاء
# -----------------------------------

logging.basicConfig(
    filename="اخطاء_الفحص.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# -----------------------------------
# وظائف الفحص
# -----------------------------------

def فحص_ssl_tls(url):
    """
    فحص الاتصال عبر SSL/TLS.
    """
    try:
        print(f"جاري فحص الاتصال عبر SSL/TLS للموقع: {url}...")
        response = requests.get(url, timeout=10, verify=True)  # تأكيد التحقق من الشهادة
        if response.status_code == 200:
            return "الاتصال آمن ومشفر باستخدام SSL/TLS."
        return f"الاتصال فشل مع رمز الحالة: {response.status_code}."
    except requests.exceptions.SSLError:
        return "تحذير: شهادة SSL غير موثوقة أو غير صالحة!"
    except requests.exceptions.Timeout:
        return "خطأ: انتهت مهلة الاتصال!"
    except requests.exceptions.RequestException as e:
        logging.error(f"خطأ أثناء محاولة الاتصال: {e}")
        return f"خطأ أثناء محاولة الاتصال: {e}"

def فحص_الموقع(url):
    """
    إجراء الفحص على الموقع.
    """
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url  # إضافة http إذا لم يكن موجودًا
    النتائج = []
    النتائج.append(فحص_ssl_tls(url))
    return النتائج

# -----------------------------------
# تشغيل البرنامج عبر CLI
# -----------------------------------

def main():
    """
    نقطة بدء البرنامج.
    """
    # إعداد محلل الأوامر
    parser = argparse.ArgumentParser(description="أداة اختبار أمان المواقع")
    parser.add_argument(
        "-u", "--url", type=str, required=True, help="رابط الموقع المراد فحصه."
    )
    parser.add_argument(
        "-o", "--output", type=str, help="اختياري: ملف لحفظ نتائج الفحص."
    )
    args = parser.parse_args()

    # تشغيل الفحص
    url = args.url
    try:
        print(f"جاري فحص الموقع: {url}")
        النتائج = فحص_الموقع(url)

        print("\nنتائج الفحص:")
        for نتيجة in النتائج:
            print(نتيجة)

        # حفظ النتائج في ملف إذا تم تحديده
        if args.output:
            with open(args.output, "w", encoding="utf-8") as file:
                file.write("\n".join(النتائج))
            print(f"\nتم حفظ النتائج في الملف: {args.output}")

    except Exception as e:
        logging.error(f"حدث خطأ غير متوقع: {traceback.format_exc()}")
        print("حدث خطأ غير متوقع. يرجى مراجعة ملف السجلات للحصول على التفاصيل.")

if __name__ == "__main__":
    main()
