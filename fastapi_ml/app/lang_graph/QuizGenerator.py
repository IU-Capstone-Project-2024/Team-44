import asyncio
from typing import List

from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

from .ValidationModels import Question, Quiz


class QuizGenerator:
    def __init__(self, model_name: str = "llama3:instruct"):
        self.parser = PydanticOutputParser(pydantic_object=Quiz)
        self.prompt_template = PromptTemplate(
            template="Generate a quiz from the following notes. Use only material from notes.\nEach question should have four options, and one correct answer which must be included in the options.\n{format_instructions}\nNotes:\n{text}\n",
            input_variables=["text"],
            partial_variables={
                "format_instructions": self.parser.get_format_instructions()
            },
        )

        self.llm = ChatOllama(
            model=model_name,
            keep_alive="5m",
            temperature=0.2,
            mirostat=2,
            mirostat_eta=0.1,
            mirostat_tau=3,  # Adjust tau for more variability
            top_p=0.9,  # Use top-p sampling to control variability
            verbose=True,
            format="json",
            #base_url="http://ollama:11434",
        )

        self.llm_chain = (
            {"text": RunnablePassthrough()}
            | self.prompt_template
            | self.llm
            | self.parser
        )

    def generate_quiz(self, chunks: List) -> Quiz:
        # chunks = self.text_splitter(docs=[notes])[0]
        questions = []

        for chunk in chunks:
            response = self.llm_chain.invoke({"text": chunk})
            questions.extend(response.questions)

        return Quiz(questions=questions)

    async def agenerate_quiz(self, chunks: List) -> Quiz:
        # chunks = self.text_splitter(docs=[notes])[0]
        questions = []

        async def async_invoke(chunk):
            response = await self.llm_chain.ainvoke({"text": chunk})
            return response.questions

        responses = await asyncio.gather(*[async_invoke(chunk) for chunk in chunks])
        questions = [
            question for response in responses for question in response]

        print(questions)
        return Quiz(questions=questions)

    def generate_quiz_batch(self, chunks: List, batch_size: int = 2) -> Quiz:
        # chunks = self.text_splitter(docs=[notes])[0]
        questions = []

        for i in range(0, len(chunks), batch_size):
            batch_chunks = chunks[i: i + batch_size]
            responses = self.llm_chain.batch(
                [{"text": chunk} for chunk in batch_chunks],
                config={"max_concurrency": batch_size},
            )
            for response in responses:
                questions.extend(response.questions)

        return Quiz(questions=questions)

    async def generate_quiz_abatch(self, chunks: List, batch_size: int = 2) -> Quiz:
        # chunks = self.text_splitter(docs=[notes])[0]
        questions = []

        async def async_batch_invoke(batch_chunks):
            responses = await self.llm_chain.abatch(
                [{"text": chunk} for chunk in batch_chunks],
                config={"max_concurrency": batch_size},
            )
            return [
                question for response in responses for question in response.questions
            ]

        tasks = [
            async_batch_invoke(chunks[i: i + batch_size])
            for i in range(0, len(chunks), batch_size)
        ]
        results = await asyncio.gather(*tasks)
        questions = [question for batch in results for question in batch]

        return Quiz(questions=questions)

    def generate_pquiz(self, chunks: List, batch_size: int = 2) -> Quiz:
        # chunks = self.text_splitter(docs=[notes])[0]
        questions = []

        for chunk_split in range(0, len(chunks), batch_size):
            batch_chunks = chunks[chunk_split: chunk_split + batch_size]
            par_chain = RunnableParallel(
                {f"chain_{i}": self.llm_chain for i in range(
                    len(batch_chunks))}
            )

            response = par_chain.invoke(
                {
                    f"chain_{i}": {"text": chunk}
                    for i, chunk in enumerate(batch_chunks)
                }
            )

            questions.extend(
                [response[f"chain_{i}"].questions for i in range(
                    len(batch_chunks))]
            )
        print(questions)
        return Quiz(
            questions=[
                question
                for question_sub_array in questions
                for question in question_sub_array
            ]
        )
