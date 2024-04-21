import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from prompt_assistant import prompt_suggestion, prompt_remix

app = FastAPI()

class Query(BaseModel):
    question: str


# 根據提問建議prompt
@app.post("/suggest/")
async def suggest(query: Query):
    try:
        response = prompt_suggestion(query.question)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# 先搜尋其他使用者用過的prompt，再結合這些歷史紀錄與提問，來建議prompt(也就是RAG)
@app.post("/remix/")
def remix(query: Query):
    try:
        response = prompt_remix(query.question)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, log_level="info")