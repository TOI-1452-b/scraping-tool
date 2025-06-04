from fastapi import APIRouter
from schema import search_request, search_response
from service import google_search, api_key, cse_id, scrape_url, send_data_to_ai




search_router = APIRouter(prefix="/master-thesis")

@search_router.post("/search")
async def search_ai_tools(request: search_request):
    results = google_search(request.parameter, api_key, cse_id, 10)
    return results

@search_router.post("/analyse")
async def analyse_ai_tools():
    results = scrape_url()
    return results

@search_router.post("/llm-analysis")
async def llm_analysis():
    results = send_data_to_ai()
    return results
