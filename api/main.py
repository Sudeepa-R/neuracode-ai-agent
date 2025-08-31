from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import logging
from src.neuracode_ai_agent.crew import NeuracodeAiAgent

app = FastAPI(title="Code Converter API")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConversionRequest(BaseModel):
    source_language: str
    target_language: str
    code_snippet: str
    
class ConversionResponse(BaseModel):
    converted_code: str

    
@app.get("/health-check")
def Api_health_check():
    res =  { "status": "healthy", "message": "API is running smoothly ✅","timestamp": datetime.utcnow().isoformat() + "Z"}
    return res
    
@app.post("/convert", response_model=ConversionResponse)
def convert_code(request: ConversionRequest):
    try:
        crew = NeuracodeAiAgent().crew()
        result = crew.kickoff(inputs=request.dict())
        return ConversionResponse(converted_code=result.raw)
    except Exception as e:
        logger.error(f"Error in convert : {e}", exc_info=True)
        return { "error" : f" An error occured while processing the data: {e}"}