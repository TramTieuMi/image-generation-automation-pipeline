# report.py – ĐÃ SỬA: XỬ LÝ example_urls RỖNG/NULL
import sqlite3
import json
from datetime import datetime
import matplotlib.pyplot as plt
import os

DB_PATH = "logs.db"
REPORT_DIR = "reports"
os.makedirs(REPORT_DIR, exist_ok=True)

def generate_daily_report():
    today = datetime.now().strftime("%Y-%m-%d")
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # THỐNG KÊ
    c.execute('SELECT status, COUNT(*) FROM task_logs WHERE DATE(timestamp) = ? GROUP BY status', (today,))
    results = c.fetchall()
    total = sum(count for _, count in results)
    success = sum(count for s, count in results if s == "success")
    failed = total - success
    rate = (success / total * 100) if total > 0 else 0

    # CHI TIẾT
    c.execute('''
        SELECT id, description, format, model, example_urls, asset_url, status, timestamp
        FROM task_logs WHERE DATE(timestamp) = ? ORDER BY timestamp DESC
    ''', (today,))
    tasks = c.fetchall()
    conn.close()

    # BIỂU ĐỒ
    plt.figure(figsize=(7, 5))
    plt.pie([success, failed], labels=['Success', 'Failed'], colors=['#4CAF50', '#F44336'],
            autopct='%1.1f%%', startangle=90)
    plt.title(f"Report - {today}\nTotal: {total} | Success: {rate:.1f}%")
    chart_path = f"{REPORT_DIR}/chart_{today}.png"
    plt.savefig(chart_path, dpi=150, bbox_inches='tight')
    plt.close()

    # HTML – AN TOÀN VỚI NULL/RỖNG
    rows = ""
    for task in tasks:
        id_, desc, fmt, model, example_urls_json, url, status, time = task
        status_icon = "Success" if status == "success" else "Failed"
        link = f'<a href="{url}" target="_blank">Xem</a>' if url else "—"

        # XỬ LÝ example_urls AN TOÀN
        try:
            example_list = json.loads(example_urls_json) if example_urls_json else []
            example = "Có" if example_list else "Không"
        except:
            example = "Không"

        rows += f"""
        <tr>
            <td>{id_}</td>
            <td>{desc}</td>
            <td>{fmt.upper()}</td>
            <td>{model}</td>
            <td>{example}</td>
            <td>{link}</td>
            <td>{status_icon}</td>
            <td>{time[11:16] if time else ""}</td>
        </tr>
        """

    html = f"""
    <h2>Daily Report - {today}</h2>
    <p><b>Total:</b> {total} | <b>Success:</b> {success} | <b>Failed:</b> {failed} | <b>Rate:</b> {rate:.1f}%</p>
    <img src="chart_{today}.png" width="500">
    <h3>Chi Tiết</h3>
    <table border="1" cellpadding="8" style="border-collapse: collapse; width: 100%; font-size: 14px;">
        <tr style="background:#f0f0f0; text-align:center;">
            <th>ID</th><th>Description</th><th>Format</th><th>Model</th><th>Example</th><th>Link</th><th>Status</th><th>Time</th>
        </tr>
        {rows or "<tr><td colspan='8' style='text-align:center;'>Không có task</td></tr>"}
    </table>
    """
    html_path = f"{REPORT_DIR}/report_{today}.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    return html_path, chart_path

# # report.py
# import sqlite3
# from datetime import datetime
# import matplotlib.pyplot as plt
# import os
# import json

# DB_PATH = "logs.db"
# REPORT_DIR = "reports"
# os.makedirs(REPORT_DIR, exist_ok=True)

# def generate_daily_report():
#     today = datetime.now().strftime("%Y-%m-%d")
#     conn = sqlite3.connect(DB_PATH)
#     c = conn.cursor()

#     # THỐNG KÊ
#     c.execute('''
#         SELECT status, COUNT(*) FROM task_logs
#         WHERE DATE(timestamp) = ?
#         GROUP BY status
#     ''', (today,))
#     results = c.fetchall()
#     total = sum(count for _, count in results)
#     success = sum(count for s, count in results if s == "success")
#     failed = total - success
#     success_rate = (success / total * 100) if total > 0 else 0

#     # CHI TIẾT
#     c.execute('''
#         SELECT id, description, format, model, asset_url, status, timestamp
#         FROM task_logs
#         WHERE DATE(timestamp) = ?
#         ORDER BY timestamp DESC
#     ''', (today,))
#     tasks = c.fetchall()
#     conn.close()

#     # BIỂU ĐỒ
#     labels = ['Success', 'Failed']
#     sizes = [success, failed]
#     colors = ['#4CAF50', '#F44336']
#     plt.figure(figsize=(7, 5))
#     plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
#     plt.title(f"Pipeline Report - {today}\nTotal: {total} | Success: {success_rate:.1f}%")
#     chart_path = f"{REPORT_DIR}/chart_{today}.png"
#     plt.savefig(chart_path, dpi=150, bbox_inches='tight')
#     plt.close()

#     # BẢNG CHI TIẾT
#     task_rows = ""
#     for task in tasks:
#         id_, desc, fmt, model, url, status, time = task
#         status_icon = "Success" if status == "success" else "Failed"
#         link = f'<a href="{url}" target="_blank">Xem</a>' if url else "—"
#         example = "Có" if json.loads(task[4]) else "Không" if task[4] else "—"
#         task_rows += f"""
#         <tr>
#             <td>{id_}</td>
#             <td>{desc}</td>
#             <td>{fmt.upper()}</td>
#             <td>{model}</td>
#             <td>{example}</td>
#             <td>{link}</td>
#             <td>{status_icon}</td>
#             <td>{time[11:19]}</td>
#         </tr>
#         """

#     html = f"""
#     <h2>Daily Report - {today}</h2>
#     <p><strong>Total:</strong> {total} | <strong>Success:</strong> {success} | <strong>Failed:</strong> {failed} | <strong>Rate:</strong> {success_rate:.1f}%</p>
#     <img src="chart_{today}.png" width="500">
#     <h3>Chi Tiết</h3>
#     <table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse; width: 100%; font-size: 14px;">
#         <tr style="background: #f0f0f0; text-align: center;">
#             <th>ID</th><th>Description</th><th>Format</th><th>Model</th><th>Example</th><th>Link</th><th>Status</th><th>Time</th>
#         </tr>
#         {task_rows or "<tr><td colspan='8' style='text-align:center;'>Không có task</td></tr>"}
#     </table>
#     """
#     html_path = f"{REPORT_DIR}/report_{today}.html"
#     with open(html_path, "w", encoding="utf-8") as f:
#         f.write(html)

#     return html_path, chart_path