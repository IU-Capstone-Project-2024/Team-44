import asyncio
import logging
from typing import List

from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from sympy import Q

from .ValidationModels import Question, Quiz


class QuizGenerator:
    def __init__(self, model_name: str = "llama3:instruct"):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info(f"\t\t\tInitializing QuizGenerator with model {model_name}")

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
            mirostat_eta=0.2,
            mirostat_tau=3,  # Adjust tau for more variability
            top_p=0.8,  # Use top-p sampling to control variability
            verbose=True,
            format="json",
            # base_url="http://ollama:11434",
        )

        self.llm_chain = (
            {"text": RunnablePassthrough()}
            | self.prompt_template
            | self.llm
            | self.parser
        )

    def generate_quiz(self, chunks: List[str]) -> Quiz:
        self.logger.info(f"Starting quiz generation using generate_quiz.")
        questions = []

        for chunk in chunks:
            try:
                self.logger.debug(f"\tProcessing chunk: {chunk}")
                response = self.llm_chain.invoke({"text": chunk})
                questions.extend(response.questions)
                self.logger.debug(f"\t\tGenerated questions: {response.questions}")
            except Exception as e:
                self.logger.error(f"Error generating quiz for chunk {chunk}: {e}")

        self.logger.info(
            f"\tQuiz generation completed with {len(questions)} questions."
        )
        return Quiz(questions=questions)

    async def agenerate_quiz(self, chunks: List[str]) -> Quiz:
        self.logger.info(f"Starting quiz generation using agenerate_quiz.")
        questions = []

        async def async_invoke(chunk):
            try:
                self.logger.debug(f"\tProcessing chunk: {chunk}")
                response = await self.llm_chain.ainvoke({"text": chunk})
                self.logger.debug(f"\t\tGenerated questions: {response.questions}")
                return response.questions
            except Exception as e:
                self.logger.error(f"Error generating quiz for chunk {chunk}: {e}")
                return []

        responses = await asyncio.gather(*[async_invoke(chunk) for chunk in chunks])
        questions = [question for response in responses for question in response]

        self.logger.info(
            f"\tQuiz generation completed with {len(questions)} questions."
        )
        return Quiz(questions=questions)

    def generate_quiz_batch(self, chunks: List[str], batch_size: int = 2) -> Quiz:
        self.logger.info(f"Starting quiz generation using generate_quiz_batch.")
        questions = []

        for i in range(0, len(chunks), batch_size):
            batch_chunks = chunks[i : i + batch_size]
            try:
                self.logger.debug(f"\tProcessing batch chunks: {batch_chunks}")
                responses = self.llm_chain.batch(
                    [{"text": chunk} for chunk in batch_chunks],
                    config={"max_concurrency": batch_size},
                )
                for response in responses:
                    questions.extend(response.questions)
                    self.logger.debug(f"\t\tGenerated questions: {response.questions}")
            except Exception as e:
                self.logger.error(
                    f"Error generating batch quiz for chunks {batch_chunks}: {e}"
                )

        self.logger.info(
            f"\tQuiz generation completed with {len(questions)} questions."
        )
        return Quiz(questions=questions)

    async def generate_quiz_abatch(
        self, chunks: List[str], batch_size: int = 2
    ) -> Quiz:
        self.logger.info(f"Starting quiz generation using generate_quiz_abatch.")
        questions = []

        async def async_batch_invoke(batch_chunks):
            try:
                self.logger.debug(f"\tProcessing batch chunks: {batch_chunks}")
                responses = await self.llm_chain.abatch(
                    [{"text": chunk} for chunk in batch_chunks],
                    config={"max_concurrency": batch_size},
                )
                batch_questions = [
                    question
                    for response in responses
                    for question in response.questions
                ]
                self.logger.debug(f"\t\tGenerated questions: {batch_questions}")
                return batch_questions
            except Exception as e:
                self.logger.error(
                    f"Error generating async batch quiz for chunks {batch_chunks}: {e}"
                )
                return []

        tasks = [
            async_batch_invoke(chunks[i : i + batch_size])
            for i in range(0, len(chunks), batch_size)
        ]
        results = await asyncio.gather(*tasks)
        questions = [question for batch in results for question in batch]

        self.logger.info(
            f"\tQuiz generation completed with {len(questions)} questions."
        )
        return Quiz(questions=questions)

    def generate_pquiz(self, chunks: List[str], batch_size: int = 2) -> Quiz:
        self.logger.info(f"Starting quiz generation using generate_pquiz.")
        questions = []

        for chunk_split in range(0, len(chunks), batch_size):
            batch_chunks = chunks[chunk_split : chunk_split + batch_size]
            try:
                self.logger.debug(f"\tProcessing batch chunks: {batch_chunks}")
                par_chain = RunnableParallel(
                    {f"chain_{i}": self.llm_chain for i in range(len(batch_chunks))}
                )

                response = par_chain.invoke(
                    {
                        f"chain_{i}": {"text": chunk}
                        for i, chunk in enumerate(batch_chunks)
                    }
                )

                questions.extend(
                    [response[f"chain_{i}"].questions for i in range(len(batch_chunks))]
                )
                self.logger.debug(f"\t\tGenerated questions: {questions}")
            except Exception as e:
                self.logger.error(
                    f"Error generating parallel quiz for chunks {batch_chunks}: {e}"
                )
        questions = [
            question
            for question_sub_array in questions
            for question in question_sub_array
        ]
        self.logger.info(
            f"\tQuiz generation completed with {len(questions)} questions."
        )
        return Quiz(questions=questions)
