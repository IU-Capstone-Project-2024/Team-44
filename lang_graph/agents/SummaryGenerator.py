import os
from langchain import HumanMessages, SystemMessages
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOllama


class SymmaryGenerator:
    def __init__(self) -> None:
        self.llm = ChatOllama(name="llama3")
        self.promt = PromptTemplate(
            template=
            """

            """
        )

    def generate_summary(
            context: str,

    ) -> str:
        raise NotImplementedError()