from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI()

sentiment_model = pipeline("sentiment-analysis")

# 요청 받을 유저 모델
class TextInput(BaseModel):
    text: str

# 3. 감정 분석 API 만들기
@app.post("/predict")
def predict(input: TextInput):
    result = sentiment_model(input.text)[0]  # 첫 번째 결과만 사용
    return {"label": result['label'], "score": round(result['score'], 4)}
