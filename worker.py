
import os
import time
from ai_client import generate_asset
from gsheets import read_new_requests, update_status
from gdrive import upload_asset
from notifier import send_notification
from db import log_request


def main():
    print("Starting Asset Pipeline...")

    requests = read_new_requests()
    if not requests:
        print("No new requests.")
        return

    for req in requests:
        row_index = req["row_index"]
        desc = req["description"]
        fmt = req["format"].lower() if req.get("format") else "png"
        model = req.get("model") or "imagen-3.0-generate-001"
        example_urls = req.get("example_asset_urls") or []

        print(f"\n[Processing] Row {row_index} - {desc} (format={fmt}, model={model})")

        asset_path = None
        drive_url = None

        try:
            # BƯỚC 1: TẠO ẢNH
            print("[AI] Generating...")
            asset_path = generate_asset(
                description=desc,
                example_urls=example_urls,
                format=fmt,
                model=model
            )

            if not asset_path or not os.path.exists(asset_path):
                raise Exception("Cannot generate asset!")

            # BƯỚC 2: UPLOAD
            print(f"[Drive] Uploading {os.path.basename(asset_path)}...")
            drive_url = upload_asset(asset_path, description=desc)

            if not drive_url:
                raise Exception("Failure to upload")

            # BƯỚC 3: CẬP NHẬT + GỬI + LOG
            update_status(row_index, drive_url)
            send_notification(drive_url, desc, success=True)
            log_request(desc, fmt, model, example_urls, drive_url, "success")
            print("[Done] Checkmark")

        except Exception as e:
            error_msg = str(e)
            print(f"[Error] Row {row_index}: {error_msg}")
            send_notification("", desc, success=False, error=error_msg)
            log_request(desc, fmt, model, example_urls, "", "failed")

        finally:
            if asset_path and os.path.exists(asset_path):
                try:
                    os.remove(asset_path)
                    print(f"[Cleanup]: {asset_path}")
                except:
                    pass
            time.sleep(1)

    print("\nPipeline completed!")


if __name__ == "__main__":
    main()
