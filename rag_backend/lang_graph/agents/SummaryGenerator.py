# from langchain_community.chat_models import ChatOllama
from langchain_core.messages.base import BaseMessage
from transformers import T5ForConditionalGeneration, AutoModelForSeq2SeqLM
from transformers import AutoTokenizer
from transformers import pipeline
from langchain_huggingface import HuggingFacePipeline


class SummaryGenerator:
    def __init__(self) -> None:
        self.system_msg = """
        Make a summary of provided text. Find key points and build a summary around these key points.
        """
        model_id = "slauw87/bart_summarisation"  # Limitation of 1024 tokens
        tokenizer = AutoTokenizer.from_pretrained(model_id)

        model = AutoModelForSeq2SeqLM.from_pretrained(model_id)

        pipe = pipeline(
            task="summarization",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=5000,
            top_k=50,
            temperature=0.1,
            do_sample=True,
            num_beams=20,  # increase comp. load + better quality
            # length_penalty=3.0
        )

        self.llm = HuggingFacePipeline(pipeline=pipe)

        # self.llm = ChatOllama( # High quality, but need more computation power
        #     model="llama3:8b",
        #     keep_alive=0,
        #     temperature=0.0,
        #     system=self.system_msg,
        #     top_k=10,
        #     top_p=0.05,
        #     verbose=True,
        # )

    def generate_summary(
        self,
        text: str,  # choose a data format
    ) -> BaseMessage:
        question = self.llm.invoke(text)
        return question


if __name__ == "__main__":
    text = """
			Encoder: The encoder is composed of a stack of N = 6 identical layers. Each layer has two sub-layers. The first is a multi-head self-attention mechanism, and the second is a simple, position- wise fully connected feed-forward network. We employ a residual connection [11] around each of the two sub-layers, followed by layer normalization [1]. That is, the output of each sub-layer is LayerNorm(x + Sublayer(x)), where Sublayer(x) is the function implemented by the sub-layer itself. To facilitate these residual connections, all sub-layers in the model, as well as the embedding layers, produce outputs of dimension dmodel = 512.
			Decoder: The decoder is also composed of a stack of N = 6 identical layers. In addition to the two sub-layers in each encoder layer, the decoder inserts a third sub-layer, which performs multi-head attention over the output of the encoder stack. Similar to the encoder, we employ residual connections around each of the sub-layers, followed by layer normalization. We also modify the self-attention sub-layer in the decoder stack to prevent positions from attending to subsequent positions. This masking, combined with fact that the output embeddings are offset by one position, ensures that the predictions for position i can depend only on the known outputs at positions less than i.
		"""
    s = SummaryGenerator()
    ans = s.generate_summary(text=text)
    print(type(ans), ans)
