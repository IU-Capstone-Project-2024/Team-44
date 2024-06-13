from langchain_community.embeddings import OllamaEmbeddings
from torch import Tensor


class Embedder:
    def __init__(self) -> None:
        self.embedder = OllamaEmbeddings(
            model="nomic-embed-text:latest",  # dim=768 - could be changed if following https://huggingface.co/nomic-ai/nomic-embed-text-v1.5
            query_instruction="search_query:",
            embed_instruction="search_document:",
        )


def demo_() -> None:
    from semantic_chunkers import StatisticalChunker
    from semantic_router.encoders import HuggingFaceEncoder

    encoder = HuggingFaceEncoder()
    chunker = StatisticalChunker(encoder=encoder)  # get an API for nomic embed
    print(chunker)


def d_() -> None:
    import torch
    import torch.nn.functional as F
    from transformers import AutoTokenizer, AutoModel

    def mean_pooling(model_output, attention_mask) -> Tensor:
        token_embeddings = model_output[0]
        input_mask_expanded = (
            attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        )
        return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(
            input_mask_expanded.sum(1), min=1e-9
        )

    sentences = [
        "search_query: What is TSNE?",
        "search_query: Who is Laurens van der Maaten?",
    ]

    tokenizer = AutoTokenizer.from_pretrained(
        "bert-base-uncased", model_max_length=8192
    )
    model = AutoModel.from_pretrained(
        "nomic-ai/nomic-embed-text-v1.5",
        trust_remote_code=True,
        safe_serialization=True,
        rotary_scaling_factor=2,
    )
    model.eval()

    encoded_input = tokenizer(
        sentences, padding=True, truncation=True, return_tensors="pt"
    )

    matryoshka_dim = 512

    with torch.no_grad():
        model_output = model(**encoded_input)

    embeddings = mean_pooling(model_output, encoded_input["attention_mask"])
    embeddings = F.layer_norm(embeddings, normalized_shape=(embeddings.shape[1],))
    embeddings = embeddings[:, :matryoshka_dim]
    embeddings = F.normalize(embeddings, p=2, dim=1)
    print(embeddings)


# d_()
