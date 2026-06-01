from fastapi import FastAPI, UploadFile, File, Form
import google.generativeai as genai
from PIL import Image
import io
import os
from dotenv import load_dotenv
load_dotenv()
app = FastAPI()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")


@app.post("/analyze-medicine")
async def analyze_medicine(
    question: str = Form(...),
    image: UploadFile = File(...)
):

    try:
        image_bytes = await image.read()

        # open image
        pil_image = Image.open(io.BytesIO(image_bytes))

        # 🔥 IMPORTANT FIX (webp/png/jpg sab ke liye safe)
        if pil_image.mode != "RGB":
            pil_image = pil_image.convert("RGB")

        response = model.generate_content([question, pil_image])

        return {
            "answer": response.text
        }

    except Exception as e:
        return {
            "error": str(e)
        }