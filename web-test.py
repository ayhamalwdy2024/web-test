import argparse
import requests
import traceback
import logging

# -----------------------------------
# إعداد تسجيل الأخطاء
# -----------------------------------

logging.basicConfig(
    filename="scanner_errors.log",
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
        print(f"Checking {url} for SSL/TLS connection...")
        response = requests.get(url, timeout=10, verify=True)  # تأكيد التحقق من الشهادة
        if response.status_code == 200:
            return "The connection is properly encrypted via SSL/TLS."
        return f"The connection failed with status code: {response.status_code}."
    except requests.exceptions.SSLError:
        return "Warning: The SSL certificate is untrusted or invalid!"
    except requests.exceptions.Timeout:
        return "Error: Connection attempt timed out!"
    except requests.exceptions.RequestException as e:
        logging.error(f"RequestException: {e}")
        return f"Error during connection attempt: {e}"

def فحص_الموقع(url):
    """
    إجراء الفحص على الموقع.
    """
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url  # تصحيح الرابط تلقائيًا
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
    parser = argparse.ArgumentParser(description="Security Testing Tool for Websites")
    parser.add_argument(
        "-u", "--url", type=str, required=True, help="URL of the website to scan."
    )
    parser.add_argument(
        "-o", "--output", type=str, help="Optional: Output file to save the scan results."
    )
    args = parser.parse_args()

    # تشغيل الفحص
    url = args.url
    try:
        print(f"Scanning the website: {url}")
        النتائج = فحص_الموقع(url)

        print("\nScan Results:")
        for نتيجة in النتائج:
            print(نتيجة)

        # حفظ النتائج في ملف إذا تم تحديده
        if args.output:
            with open(args.output, "w", encoding="utf-8") as file:
                file.write("\n".join(نتائج))
            print(f"\nResults saved to {args.output}")

    except Exception as e:
        logging.error(f"An error occurred: {traceback.format_exc()}")
        print(f"An unexpected error occurred. Please check the log file for details.")

if __name__ == "__main__":
    main()
