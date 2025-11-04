import os
import base64
import time
import subprocess
from dotenv import load_dotenv
from google.cloud import aiplatform

load_dotenv()
os.makedirs("temp", exist_ok=True)

FFMPEG_PATH =...

def generate_asset(description: str, example_urls: list = None, format: str = "png", model: str = None):
    fmt = format.lower()
    print(f"[AI] Generating asset (format={fmt})...")

    if fmt not in {"png", "jpg", "jpeg", "gif"}:
        print(f"[AI] Định dạng không hỗ trợ: {fmt}")
        return None

    try:
        project = os.getenv("GCP_PROJECT_ID")
        location = "us-central1"
        aiplatform.init(project=project, location=location)

        model_name = model or "imagen-3.0-generate-001"
        endpoint = f"projects/{project}/locations/{location}/publishers/google/models/{model_name}"

        prompt = f"Pixel art style: {description}"
        if example_urls:
            prompt += f". Reference: {', '.join(example_urls)}"

        client = aiplatform.gapic.PredictionServiceClient()

        timestamp = int(time.time())
        safe_desc = "".join(c if c.isalnum() else "_" for c in description)[:30]

        if fmt != "gif":
            response = client.predict(
                endpoint=endpoint,
                instances=[{"prompt": prompt}],
                parameters={"sampleCount": 1}
            )

            img_b64 = response.predictions[0]["bytesBase64Encoded"]
            img_bytes = base64.b64decode(img_b64)

            final_path = f"temp/{safe_desc}_{timestamp}.{fmt}"
            with open(final_path, "wb") as f:
                f.write(img_bytes)

            print(f"[AI] SUCCESS: {final_path}")
            return final_path

        frames = []
        frame_prompts = [
            f"{prompt} frame 1: preparing to jump",
            f"{prompt} frame 2: mid jump",
            f"{prompt} frame 3: peak jump",
            f"{prompt} frame 4: landing"
        ]

        for i, frame_prompt in enumerate(frame_prompts, 1):
            response = client.predict(
                endpoint=endpoint,
                instances=[{"prompt": frame_prompt}],
                parameters={"sampleCount": 1}
            )

            img_b64 = response.predictions[0]["bytesBase64Encoded"]
            img_bytes = base64.b64decode(img_b64)

            frame_path = f"temp/{safe_desc}_{timestamp}_frame{i}.png"
            with open(frame_path, "wb") as f:
                f.write(img_bytes)

            frames.append(frame_path)

        gif_path = f"temp/{safe_desc}_{timestamp}.gif"
        cmd = [
            FFMPEG_PATH, "-y",
            "-i", frames[0], "-i", frames[1], "-i", frames[2], "-i", frames[3],
            "-filter_complex", "concat=n=4:v=1:a=0,framerate=8,scale=512:-1",
            "-loop", "0",
            gif_path
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print(f"[FFmpeg] Lỗi: {result.stderr}")
            for frame in frames:
                if os.path.exists(frame):
                    os.remove(frame)
            return None

        # XÓA FRAME TẠM
        for frame in frames:
            if os.path.exists(frame):
                os.remove(frame)

        print(f"[AI] SUCCESS: {gif_path}")
        return gif_path

    except Exception as e:
        print(f"[AI] Lỗi: {e}")
        return None
