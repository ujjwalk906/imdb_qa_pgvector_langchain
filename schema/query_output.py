from typing import List, Union
from pydantic import BaseModel, Field

class RecommendationFromLLM(BaseModel):
    reason: str = Field(description="Why this movie is relevant to the query")
    highlights: List[str] = Field(description="Key themes or tags from the plot")

class FinalRecommendation(BaseModel):
    id: Union[int, str]
    metadata: dict
    structured: RecommendationFromLLM

class QueryResponse(BaseModel):
    query: str
    recommendations: List[FinalRecommendation]
