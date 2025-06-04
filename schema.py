from pydantic import BaseModel
from typing import List

class search_request(BaseModel):
    parameter: str

class SearchResult(BaseModel):
    title: str
    link: str
    snippet: str

class search_response(BaseModel):
    results: List[SearchResult]