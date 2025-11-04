import schedule
import time
from datetime import datetime
from report import generate_daily_report
from email_sender import send_daily_report

def send_daily_pipeline_report():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Đang tạo báo cáo ngày {datetime.now().strftime('%Y-%m-%d')}...")
    html_path, chart_path = generate_daily_report()
    send_daily_report(html_path, chart_path)
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Báo cáo đã gửi thành công!")

# GỬI MỖI NGÀY LÚC 8:00 SÁNG
schedule.every().day.at("8:00").do(send_daily_pipeline_report)

print("Scheduler đã khởi động!")
print("Báo cáo sẽ gửi lúc 8:00 sáng mỗi ngày.")
print("Giữ cửa sổ này mở để chạy liên tục.")

while True:
    schedule.run_pending()
    time.sleep(60)
