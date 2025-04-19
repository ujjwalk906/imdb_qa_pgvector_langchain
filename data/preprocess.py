from langchain_core.documents import Document
from pandas import DataFrame

def create_documents(df: DataFrame):
    return [
        Document(
            page_content=row["Plot"],
            metadata={
                "title": row["Title"],
                "genre": row["Genre"],
                "origin": row["Origin/Ethnicity"],
                "year": row["Release Year"],
                "url": row["Wiki Page"]
            }
        )
        for _,row in df.iterrows()
    ]

