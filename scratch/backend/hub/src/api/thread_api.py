from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class ListThreadsResponse(BaseModel):
    threads: list[str]

@router.get("/list_threads")
async def list_threads():
    return ListThreadsResponse(threads=["thread1", "thread2", "thread3"])

class GetThreadResponse(BaseModel):
    messages: list[str]

@router.get("/get_thread")
async def get_thread():
    return GetThreadResponse(messages=["message1", "message2", "message3"])

class AppendToThreadRequest(BaseModel):
    message: str

class AppendToThreadResponse(BaseModel):
    success: bool

@router.post("/append_to_thread")
async def append_to_thread(request: AppendToThreadRequest):
    return AppendToThreadResponse(success=True)
