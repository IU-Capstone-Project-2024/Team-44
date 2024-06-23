from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    TextSplitter,
    CharacterTextSplitter,
)
from numpy import ndarray
from torch import Tensor

from agents.SummaryGenerator import SummaryGenerator
from agents.QuizGenerator import QuizGenerator
from agents.ValidationModels import Quiz, Question

from VectorSpace.Embedder import Embedder

from VectorSpace.VectorDB import VectorStore

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
        quiz_model_name="llama3:instruct",
    ) -> None:
        """__init__ Router for managing action/data flow in the app

        Args:
            embedding_size (int, optional): embeddings size to use
            text_splitter (TextSplitter, optional): text splitter instance to use
            quiz_model_name (str, optional): model name from Ollama (currently using Ollama)
        """
        self.text_splitter = text_splitter

        self.embedder = Embedder(embedding_size=embedding_size)
        self.vector_store = VectorStore(
            text_splitter=self.text_splitter, embedder=self.embedder
        )
        self.text_splitter = text_splitter
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
            query_results = self.vector_store.retriever.vectorstore.similarity_search(
                query=query
            )
        else:
            retriver = self.vector_store.retriever.vectorstore.as_retriever(
                search_type=search_type, search_kwargs=search_kwargs
            )
            query_results = retriver.invoke(query)

        return query_results

    def add_docs(self, documents: List[Document]) -> bool:
        """add_docs _summary_

        Args:
            documents (List[Document]): LangChain Documents

        Returns:
            bool: True for success, False for error raised
        """

        # TODO: Consider case of uploading identical documnets multiple times -- Need to check

        docs = []
        threshold_retriver = self.vector_store.retriever.vectorstore.as_retriever(
            search_type="similarity_score_threshold",
            search_kwargs={"score_threshold": 0.95},
        )
        for doc in documents:
            if len(threshold_retriver.invoke(doc.page_content)) == 0:
                docs.append(doc)

        self.vector_store.add_docs(docs)

        return float(len(docs) / len(documents))

    def embed(self) -> Callable[..., Tensor | ndarray | list]:
        """Retruns fucntion used for embeddings.
            Function exists only for testing reasons!

        Returns:
            Callable[..., Tensor | ndarray | list]: embedding function
        """
        return self.embedder.embed

    def generate_quiz(self, documents: List[Document]) -> Quiz:
        """generate_quiz generate quiz based on provided documents.
            Generation is sequantial for all provied documents

        Args:
            documents (List[Document]): LangChain Documents

        Returns:
            _type_: _description_
        """
        str_text = ""
        for doc in documents:
            str_text += doc.page_content

        quiz = self.quiz_generator.generate_quiz(notes=str_text)

        return quiz

    def generate_summary(self, documents: List[Document]):
        """generate_summary _summary_

        Args:
            documents (List[Document]): LangChain Documents

        Returns:
            _type_: _description_
        """
        splitted_docs = self.text_splitter.split_documents(documents)

        summary = [
            self.summary_generator.generate_summary(text=doc.page_content)
            for doc in splitted_docs
        ]
        # parse?
        return summary

    async def agenerate_quiz(self, documents: List[Document]):
        """agenerate_quiz: async version of generate_quiz

        Args:
            documents (List[Document]): LangChain Documents

        Raises:
            NotImplementedError: _description_
        """
        raise NotImplementedError("Will be implemented later")

    async def agenerate_summary(self, documents: List[Document]):
        """agenerate_summary: async version of generate_summary

        Args:
            documents (List[Document]): LangChain Documents

        Raises:
            NotImplementedError: _description_
        """
        raise NotImplementedError("Will be implemented later")


if __name__ == "__main__":

    def main():
        text_small = "Photosynthesis is the process used by plants to convert light energy into chemical energy."

        doc_creator = RecursiveCharacterTextSplitter()

        document = doc_creator.create_documents(texts=[text_small])
        router = Router()
        quiz = router.generate_quiz(documents=document)
        print(quiz)

    main()
