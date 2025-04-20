from langchain_core.documents import Document
from schema.query_output import RecommendationFromLLM, FinalRecommendation, QueryResponse
from langchain_openai import ChatOpenAI
from typing import List

def generate_recommendation_from_doc(doc: Document) -> RecommendationFromLLM:
    model = ChatOpenAI(model="gpt-4.1-nano", temperature=0.3)
    model_with_schema = model.with_structured_output(RecommendationFromLLM)

    prompt = f"""
                You are helping a movie recommendation system.
                Based on the following movie plot, extract the reason why it's a good recommendation,
                and highlight its key themes.

                Movie Plot:
                {doc.page_content}
            """
    
    return model_with_schema.invoke(prompt)

def format_query_results(query: str, docs: List[Document]) -> QueryResponse:
    recommendations = []
    for doc in docs:
        llm_response = generate_recommendation_from_doc(doc)
        rec = FinalRecommendation(
            id=doc.id,
            metadata=doc.metadata,
            structured=llm_response
        )
        recommendations.append(rec)

    return QueryResponse(
        query=query,
        recommendations=recommendations
    )

