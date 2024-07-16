from typing import Any, List, Dict

from pydantic import PrivateAttr
import torch
import torch.nn.functional as F
from torch import Tensor
from transformers import AutoModel, AutoTokenizer


from langchain_core.embeddings import Embeddings
from semantic_router.encoders import BaseEncoder


class Embedder(BaseEncoder, Embeddings):
    name: str = "custom-nomic-embedder"
    score_threshold: float = 0.8

    embedding_size: int = 768
    query_types: Dict = {
        "search_query": "Use this when you want to encode a query for question-answering over text that was embedded with search_document.",
        "search_document": "The default embedding task type. Any document you want to use for retrieval or store in a vector database should use this task type.",
        "classification": "Use this if your embeddings are for classification (e.g. training a linear probe for a target classification task)",
        "clustering": "Use this if your embeddings need very high linear separability (e.g. building a topic model on your embeddings)",
    }

    _tokenizer: Any = PrivateAttr()
    _model: Any = PrivateAttr()

    class Config:
        arbitrary_types_allowed = True

    def __init__(
        self,
        embedding_size: int = 768,
        score_threshold=0.8,
        name="custom-nomic-embedder",
        **data,
    ) -> None:
        super().__init__(name=name, score_threshold=score_threshold)

        self.embedding_size = embedding_size
        self.name = name
        self.score_threshold = score_threshold

        object.__setattr__(
            self,
            "_tokenizer",
            AutoTokenizer.from_pretrained("bert-base-uncased", model_max_length=8192),
        )
        object.__setattr__(
            self,
            "_model",
            AutoModel.from_pretrained(
                pretrained_model_name_or_path="nomic-ai/nomic-embed-text-v1.5",
                trust_remote_code=True,
                safe_serialization=True,
                rotary_scaling_factor=2,
            ),
        )
        self._model.eval()

    def __mean_pooling(self, model_output, attention_mask) -> Tensor:
        token_embeddings = model_output[0]
        input_mask_expanded = (
            attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        )
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(
            input_mask_expanded.sum(1), min=1e-9
        )

    def embed(
        self,
        texts: List[str],
        querry: str = "search_document: ",
        return_array=False,
        return_ndarray=False,
    ) -> Tensor:
        """Function for creating embeddings"""

        if isinstance(texts, str):
            texts = [texts]

        texts = [querry + text for text in texts]

        encoded_input = self._tokenizer(
            texts, padding=True, truncation=True, return_tensors="pt"
        )

        with torch.no_grad():
            model_output = self._model(**encoded_input)

        embeddings = self.__mean_pooling(model_output, encoded_input["attention_mask"])
        embeddings = F.layer_norm(embeddings, normalized_shape=(embeddings.shape[1],))
        embeddings = embeddings[:, : self.embedding_size]
        embeddings = F.normalize(embeddings, p=2, dim=1)

        if return_ndarray:
            return embeddings.numpy()

        if return_array:
            embedded_list = embeddings.tolist()
            if len(embedded_list) == 1:
                embedded_list = embedded_list[0]
            return embedded_list

        return embeddings

    def _get_embedding(self, texts: str, querry: str) -> Tensor:
        return self.embed(texts=texts, return_array=True)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed search docs. Implemented for LangChain vector store campatability"""
        return self._get_embedding(texts=texts, querry="search_document:")

    def embed_query(self, text: str) -> List[float]:
        """Embed query text.Implemented for LangChain vector store campatability"""
        return self._get_embedding(texts=text, querry="search_query:")

    def __call__(
        self,
        docs: List[str],
        batch_size: int = 32,
        **kwds: torch.Any,
    ) -> List:
        """__call__ Used for semantic_chunkers

        Args:
            docs (List[str]): list of strings
            batch_size (int, optional): Batch size for embedder. Defaults to 32.

        Returns:
            List: list of all embeddings
        """
        all_embeddings = []
        for i in range(0, len(docs), batch_size):
            all_embeddings.extend(self.embed(docs[i : i + batch_size]))

        return all_embeddings
