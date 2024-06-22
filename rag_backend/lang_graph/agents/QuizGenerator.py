from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import LLMChain
from langchain_community.chat_models import ChatOllama
from langchain_core.runnables import RunnablePassthrough

from .ValidationModels import Quiz, Question


class QuizGenerator:
    def __init__(self, model_name="llama3:instruct"):
        self.parser = PydanticOutputParser(pydantic_object=Quiz)
        self.prompt_template = PromptTemplate(
            template="Generate a quiz from the following notes. Use only material from notes.\nEach question should have four options, and one correct answer which must be included in the options.\n{format_instructions}\nNotes:\n{text}\n",
            input_variables=["text"],
            partial_variables={
                "format_instructions": self.parser.get_format_instructions()
            },
        )

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100,
        )

        self.llm = ChatOllama(
            model=model_name,
            keep_alive=0,
            temperature=0.0,
            top_k=50,
            top_p=0.5,
            verbose=True,
            format="json",
        )

        self.llm_chain = (
            {"text": RunnablePassthrough()}
            | self.prompt_template
            | self.llm
            | self.parser
        )

    def generate_quiz(self, notes: str) -> dict:
        chunks = self.text_splitter.split_text(notes)
        questions = []
        for chunk in chunks:
            response = self.llm_chain.invoke({"text": chunk})
            questions.extend(response.questions)
        return Quiz(questions=questions)


if __name__ == "__main__":
    notes = "Photosynthesis is the process used by plants to convert light energy into chemical energy."
    generator = QuizGenerator()
    quiz_json = generator.generate_quiz(notes)
    print(quiz_json)
