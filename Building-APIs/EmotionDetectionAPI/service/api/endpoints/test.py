from fastapi import APIRouter

testRouter = APIRouter()

@testRouter.get("/test")
async def test():
    return {'test': 'test'}