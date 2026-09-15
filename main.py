from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from contextlib import asynccontextmanager
from llm.format_response import build_display_lookup
from llm.parser import parse
from models.parsing_error import ParsingError
from models.solver_failure import SolverFailure
from solver import solver_calc
from llm.format_response import format_response

class PlanRequest(BaseModel):
    user_input: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.display_names = build_display_lookup()
    yield


app = FastAPI(lifespan=lifespan)
@app.post('/plan')
def plan(request: Request, body: PlanRequest):
    parse_result = parse(body.user_input)
    if isinstance(parse_result, ParsingError):
        raise HTTPException(status_code=422, detail=parse_result.message)
    solution = solver_calc(parse_result)
    if isinstance(solution, SolverFailure):
        raise HTTPException(status_code=422, detail=solution.message)
    output = format_response(solution, request.app.state.display_names)
    return {'plan': output}
    