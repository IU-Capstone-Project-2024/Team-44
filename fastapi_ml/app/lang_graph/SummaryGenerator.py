import logging
from typing import List

from langchain_huggingface import HuggingFacePipeline
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline

from .ValidationModels import Summary


class SummaryGenerator:
    def __init__(self) -> None:
        self.system_msg = """
        Make a summary of provided text. Find key points and build a summary around these key points.
        """
        self.llm = self.__initialize_pipilene()

    def __initialize_pipilene(
        self,
    ) -> HuggingFacePipeline:
        import torch

        model_id = "slauw87/bart_summarisation"  # Limitation of 1024 tokens
        tokenizer = AutoTokenizer.from_pretrained(model_id)

        model = AutoModelForSeq2SeqLM.from_pretrained(model_id)

        device = "cuda" if torch.cuda.is_available() else "cpu"

        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info(f"\t\t\tInitializing SummaryGenerator with model {model_id}")

        return HuggingFacePipeline(
            pipeline=pipeline(
                task="summarization",
                model=model,
                tokenizer=tokenizer,
                max_new_tokens=500,
                top_k=60,
                temperature=0.3,
                do_sample=True,
                num_beams=6,  # increase comp. load + better quality
                length_penalty=2.0,
                device=device,
            )
        )

    def generate_summary(
        self,
        chunks: List[str],  # choose a data format
    ) -> Summary:
        self.logger.info(f"Starting summary generation using.\n\tChunks: {chunks}")
        summary = "\n".join([self.llm.invoke(chunk) for chunk in chunks])
        return Summary(summary=summary)


if __name__ == "__main__":
    text = """
			Encoder: The encoder is composed of a stack of N = 6 identical layers. Each layer has two sub-layers. The first is a multi-head self-attention mechanism, and the second is a simple, position- wise fully connected feed-forward network. We employ a residual connection [11] around each of the two sub-layers, followed by layer normalization [1]. That is, the output of each sub-layer is LayerNorm(x + Sublayer(x)), where Sublayer(x) is the function implemented by the sub-layer itself. To facilitate these residual connections, all sub-layers in the model, as well as the embedding layers, produce outputs of dimension dmodel = 512.
			Decoder: The decoder is also composed of a stack of N = 6 identical layers. In addition to the two sub-layers in each encoder layer, the decoder inserts a third sub-layer, which performs multi-head attention over the output of the encoder stack. Similar to the encoder, we employ residual connections around each of the sub-layers, followed by layer normalization. We also modify the self-attention sub-layer in the decoder stack to prevent positions from attending to subsequent positions. This masking, combined with fact that the output embeddings are offset by one position, ensures that the predictions for position i can depend only on the known outputs at positions less than i.
		"""
    s = SummaryGenerator()
    ans = s.generate_summary(chunks=[text])
    print(type(ans), ans)
