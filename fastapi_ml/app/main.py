import asyncio
import json
from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from .lang_graph.QuizGenerator import QuizGenerator
from .lang_graph.SummaryGenerator import SummaryGenerator
from .lang_graph.ValidationModels import Question, Quiz, Summary
from pydantic import BaseModel

quiz_generator = QuizGenerator()
summary_generator = SummaryGenerator()

app = FastAPI()


class TextRequest(BaseModel):
    text: List[str]


class SummaryRequest(BaseModel):
    query: List[str]



@app.post("/summary", response_model=Summary)
async def summary(request: SummaryRequest) -> Summary: 
    return summary_generator.generate_summary(request.query)


@app.post("/quiz", response_model=Quiz)
async def quiz(request: TextRequest) -> Quiz:
    # if not request.user.is_authenticated:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You are not logged in")
    print("start")
    #quiz = await quiz_generator.generate_quiz_abatch(chunks=request.text)
    quiz = quiz_generator.generate_pquiz(chunks=request.text)
    return quiz
