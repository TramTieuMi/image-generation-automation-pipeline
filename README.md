# AI Asset Automation Pipeline

**Automatically turns text into AI images/GIFs**, uploads to **Google Drive**, and sends **daily email reports** — all from a Google Sheet.

---

## What It Does
- User writes: *"a dancing cat in space"* → in Google Sheet
- System **reads it**, calls **AI**, makes image/GIF
- **Uploads** to Drive → gets link
- **Updates** Sheet with link + "done"
- **Logs** everything
- Every day at **8:00 AM** → sends **email report** with:
  - Total tasks
  - Success / Failed
  - Pie chart
  - Full table

---

## Project Files
Athena_Task1/
├── main.py           → Run to process all pending tasks
├── scheduler.py      → Auto-send report every morning
├── db.py             → Save logs to database
├── report.py         → Make HTML report + chart
├── email_sender.py   → Send email via Gmail
├── gsheets.py        → Read & update Google Sheet
├── gdrive.py         → Upload file to Drive
├── ai_client.py      → Talk to AI (Imagen 3)
├── notifier.py       → Show alerts (console)
├── .env              → Your secret config
└── logs.db           → Created automatically


---

## Setup (5 mins)

1. **Install packages**
   ```bash
   pip install google-api-python-client google-auth pandas matplotlib python-dotenv schedule
2. Create .env

GCP_PROJECT_ID=your-project
GDRIVE_FOLDER_ID=your-folder-id
GSHEETS_SPREADSHEET_ID=your-sheet-id

EMAIL_SENDER=you@gmail.com
EMAIL_PASSWORD=your-app-password
ADMIN_EMAIL=admin@gmail.com

Share Google Sheet with:
your-project@appspot.gserviceaccount.com (as Editor)

## How to Run
Process Tasks Now

python main.py
→ Finds all "pending" → generates → uploads → updates

Auto Daily Report (8:00 AM)
python scheduler.py
→ Keep window open
→ Or use Windows Task Scheduler to run at boot

Test Report Right Now
python test_report.py
→ Sends today’s report instantly


Notes

No free AI API for big use → using Google Imagen 3 (paid, 100/day)
GIFs made with FFmpeg (from PNG frames)
MP3/audio not supported yet
System catches all errors → logs + notifies


   
