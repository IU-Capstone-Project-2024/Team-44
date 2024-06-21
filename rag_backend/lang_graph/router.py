from uu import Error
from .agents import SummaryGenerator
from .agents import QuizGenerator

from .VectorSpace.Embedder import Embedder

from .VectorSpace.VectorDB import VectorStore

from langchain_core.documents import Document

from typing import List


class Router:
    def __init__(self) -> None:
        self.embedder = Embedder()
        self.vector_store = VectorStore()
        self.summary_generator = SummaryGenerator()
        self.quiz_generator = QuizGenerator()

    def retrieve(
        self,
        query: str,
        search_type: str | None = None,
        search_kwargs: None | dict = None,
    ) -> None | List[Document]:
        if search_type is None and search_kwargs is None:
            try:
                query_results = (
                    self.vector_store.retriever.vectorstore.similarity_search(
                        query=query
                    )
                )
            except Error as e:
                print(e.with_traceback())
                return None
        try:
            retriver = self.vector_store.retriever.vectorstore.as_retriever(
                search_type=search_type, search_kwargs=search_kwargs
            )
            query_results = retriver.invoke(query)

        except Error as e:
            print(e.with_traceback())
            return None

        return query_results

    def add_docs(self, documents: Document | List[Document]) -> bool:
        try:
            self.vector_store.add_docs(documents)
        except Error as e:
            print(e.with_traceback())
            return False
        return True

    def embed():
        raise NotImplementedError("Will be implemented later")

    async def generate_quiz():
        raise NotImplementedError("Will be implemented later")

    async def generate_summary():
        raise NotImplementedError("Will be implemented later")

    async def agenerate_quiz():
        raise NotImplementedError("Will be implemented later")

    async def agenerate_summary():
        raise NotImplementedError("Will be implemented later")
