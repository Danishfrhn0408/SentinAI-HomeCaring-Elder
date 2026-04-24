import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("Tiada API Key dijumpai. Sila periksa fail .env anda.")

# Format baru untuk connect ke Gemini
client = genai.Client(api_key=API_KEY)

app = FastAPI(title="SentinAI Backend")

class VisionData(BaseModel):
    event_type: str
    confidence: float
    timestamp: str

@app.get("/")
def read_root():
    return {"message": "SentinAI Backend is active and running."}

@app.post("/api/emergency-alert")
def process_alert(data: VisionData):
    try:
        prompt = f"""
        You are SentinAI, an emergency medical response agent.
        You just received a camera detection alert from a senior citizen's home.
        
        Event: {data.event_type}
        Confidence: {data.confidence}
        Time: {data.timestamp}
        
        If the event is 'fall_detected' and confidence is above 0.80, generate a short, urgent message to be sent to a family member's WhatsApp. State the required immediate action. If not, state that it is a false alarm.
        """
        
        # Panggil Gemini menggunakan SDK versi baharu
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        
        received_dict = data.model_dump() if hasattr(data, 'model_dump') else data.dict()
        
        return {
            "status": "success",
            "received_data": received_dict,
            "gemini_action": response.text
        }
    except Exception as e:
        print(f"🔴 ERROR DETAIL: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))