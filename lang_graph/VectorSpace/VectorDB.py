from langchain.vectorstores import Chroma
from langchain.storage import InMemoryStore
from langchain.retrievers.multi_vector import MultiVectorRetriever
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.text_splitter import TextSplitter

from langchain_core.documents import Document

from typing import List

from . import Embedder


class VectorStore:
    """
    Usage ways:

    .. code-block:: python


    vector_store = VectorStore()
    vector_store.add_docs(documents)

    query_results = vector_store.retriever.vectorstore.similarity_search(query_1)

    query_1 = "Place Text Here For Your Query"

    # Only get the single most similar document from the dataset
    query_results = vector_store.retriever.vectorstore.as_retriever(
                search_type="similarity",
                search_kwargs={
                    "k": 5
                }
            )
    # Only retrieve documents that have a relevance score
    # Above a certain threshold
    query_results = vector_store.retriever.vectorstore.as_retriever(
                search_type="similarity_score_threshold",
                search_kwargs={
                    'score_threshold': 0.8
                }
            )

    # Retrieve more documents with higher diversity
    # Useful if your dataset has many similar documents
    query_results = vector_store.retriever.vectorstore.as_retriever(
                search_type="mmr",
                search_kwargs={
                    'k': 6,
                    'lambda_mult': 0.25
                }
            )


    # Retrieve more documents with higher diversity
    # Useful if your dataset has many similar documents
    query_results = vector_store.retriever.vectorstore.as_retriever(
                search_type="mmr",
                search_kwargs={
                    'k': 5,
                    'fetch_k': 50
                }
            )

    # Use a filter to only retrieve documents from a specific paper name
    query_results = vector_store.retriever.vectorstore.as_retriever(
                search_kwargs={
                    'filter' : {
                        'paper_title':'Attention All You Need'
                    }
                }
            )

    """

    def __init__(
        self,
        text_splitter: TextSplitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=100
        ),
    ) -> None:
        self.embedder = Embedder()
        self.recursice_splitter = text_splitter

        self.vector_store = Chroma(
            embedding_function=self.embedder,
            persist_directory=".VectorData/chroma_db",
            collection_name="Chroma-Nomic-768",
        )

        self.store = InMemoryStore()

        self.retriever = MultiVectorRetriever(
            vectorstore=self.vector_store,
            docstore=self.store,
        )

    def add_docs(self, documents: Document | List[Document]) -> None:
        """
        Possible way to load Documents:

        .. code-block:: python
        loader = TextLoader("test_txt.txt")
        documents = loader.load()

        vector_store = VectorStore()
        vector_store.add_docs(documents)

        """
        docs = []
        for doc in documents:
            docs.extend(doc)

        texts = self.recursice_splitter.split_documents(docs)

        self.retriever.vectorstore.add_documents(texts)
