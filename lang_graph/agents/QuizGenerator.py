# from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain_core.messages.base import BaseMessage


class QuizGenerator:
    def __init__(self) -> None:
        self.system_msg = """
            Create several multiple choice questions based on provided text.
            Send questions in order of importance and quality.
            Strictly follow python-like format:
            ["Which of the following subjects could fly?", ["Cat", "Airplane", "Coffee", ""], ["Airplane"]]
            ["Which component(s) do(es) not exists in physical world?", ["Network Interphace Cart", "Router", "Quick Sort", "Ghost"], ["Quick Sort", "Ghost"]]
            """

        self.llm = ChatOllama(
            model="nous-hermes2:latest",
            format="json",
            keep_alive=0,
            temperature=0.0,
            system=self.system_msg,
            top_k=10,
            top_p=0.05,
            verbose=True,
        )

    def generate_quiz(
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
    q = QuizGenerator()
    ans = q.generate_quiz(text=text)
    print(ans)
