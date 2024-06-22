import errno

from langchain_text_splitters import RecursiveCharacterTextSplitter, TextSplitter
from numpy import ndarray
from torch import Tensor
from agents import SummaryGenerator
from agents import QuizGenerator

from VectorSpace import Embedder
from VectorSpace import VectorStore

from langchain_core.documents import Document

from typing import Callable, List


class Router:
    """Router for managing action/data flow in the app"""

    def __init__(
        self,
        embedding_size: int = 768,
        text_splitter: TextSplitter = RecursiveCharacterTextSplitter(
            chunk_size=2000, chunk_overlap=100
        ),
        quiz_model_name="llama3:8b",
    ) -> None:
        """__init__ _summary_

        Args:
            embedding_size (int, optional): embeddings size to use
            text_splitter (TextSplitter, optional): text splitter instance to use
            quiz_model_name (str, optional): model name from Ollama (currently using Ollama)
        """
        self.embedder = Embedder(embedding_size=embedding_size)
        self.vector_store = VectorStore(text_splitter=text_splitter)
        self.summary_generator = SummaryGenerator()
        self.quiz_generator = QuizGenerator(model_name=quiz_model_name)

    def retrieve(
        self,
        query: str,
        search_type: str | None = None,
        search_kwargs: None | dict = None,
    ) -> None | List[Document]:
        """retrive - retrive the data from vectore_store by given parameters.
        If parameters does not passed: used retriver with "similarity" and "k=4"

        Args:
            query (str): Search query
            search_type (str | None, optional): Can be "similarity", "mmr", or "similarity_score_threshold"
            search_kwargs (None | dict, optional): basic langchain retriver search kwargs

        Returns:
            None | List[Document]: None for raised error, retrived documents if successd
        """
        if search_type is None and search_kwargs is None:
            try:
                query_results = (
                    self.vector_store.retriever.vectorstore.similarity_search(
                        query=query
                    )
                )
            except errno as e:
                print(e.with_traceback())
                return None
        try:
            retriver = self.vector_store.retriever.vectorstore.as_retriever(
                search_type=search_type, search_kwargs=search_kwargs
            )
            query_results = retriver.invoke(query)

        except errno as e:
            print(e.with_traceback())
            return None

        return query_results

    def add_docs(self, documents: Document | List[Document]) -> bool:
        """add_docs _summary_

        Args:
            documents (Document | List[Document]): LangChain Documents

        Returns:
            bool: True for success, False for error raised
        """

        # check the
        try:
            self.vector_store.add_docs(documents)
        except errno as e:
            print(e.with_traceback())
            return False
        return True

    def embed(self) -> Callable[..., Tensor | ndarray | list]:
        """Retruns fucntion used for embeddings

        Returns:
            Callable[..., Tensor | ndarray | list]: embedding function
        """
        return self.embedder.embed

    def generate_quiz(self, documents: Document | List[Document]):
        """generate_quiz _summary_

        Args:
            documents (Document | List[Document]): LangChain Documents

        Returns:
            _type_: _description_
        """
        # Actions:
        # documents -> str -> invoke
        quiz = self.quiz_generator.generate_quiz(text="")

        # parse a quiz?

        return quiz

    def generate_summary(self, documents: Document | List[Document]):
        """generate_summary _summary_

        Args:
            documents (Document | List[Document]): LangChain Documents

        Returns:
            _type_: _description_
        """
        # Actions:
        # documents -> str -> invoke
        summary = self.summary_generator.generate_summary(text="")
        # parse
        return summary

    async def agenerate_quiz(self, documents: Document | List[Document]):
        """agenerate_quiz: async version of generate_quiz

        Args:
            documents (Document | List[Document]): LangChain Documents

        Raises:
            NotImplementedError: _description_
        """
        raise NotImplementedError("Will be implemented later")

    async def agenerate_summary(self, documents: Document | List[Document]):
        """agenerate_summary: async version of generate_summary

        Args:
            documents (Document | List[Document]): LangChain Documents

        Raises:
            NotImplementedError: _description_
        """
        raise NotImplementedError("Will be implemented later")


if __name__ == "__main__":
    q = Embedder(embedding_size=64)
    a = q.embed("asdasd")
    print(a)
