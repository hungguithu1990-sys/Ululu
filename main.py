from fastapi import FastAPI, Query
from duckduckgo_search import DDGS
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Bật CORS để Hugging Face có thể gọi API này
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok", "message": "DDG Proxy đang chạy!"}

@app.get("/search")
def search(q: str = Query(..., description="Từ khóa tìm kiếm")):
    try:
        # Dùng backend lite để tránh bị chặn
        results = list(DDGS().text(q, max_results=5, backend="lite", region="vn-vi"))
        
        if not results:
            return {"context": ""}
            
        context = ""
        for res in results:
            context += f"- {res.get('title')}: {res.get('body')}\n"
            
        return {"context": context}
    except Exception as e:
        return {"error": str(e)}
