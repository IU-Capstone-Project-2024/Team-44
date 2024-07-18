from typing import List

from pydantic import BaseModel, Field, field_validator


class Question(BaseModel):
    question: str = Field(description="The quiz question")
    options: List[str] = Field(description="List of multiple-choice options")
    correct_answers: List[str] = Field(description="List of correct answers")

    # @field_validator("options")
    # def check_options_length(cls, v):
    #     if len(v) != 4:
    #         raise ValueError("Each question must have exactly 4 options.")
    #     return v

    # @field_validator("correct_answers")
    # def check_correct_answers_length(cls, v):
    #     if len(v) != 1:
    #         raise ValueError("There must be exactly one correct answer.")
    #     return v


class Quiz(BaseModel):
    questions: List[Question] = Field(description="List of quiz questions")
