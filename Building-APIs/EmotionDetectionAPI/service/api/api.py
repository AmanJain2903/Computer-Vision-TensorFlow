from fastapi import APIRouter
from service.api.endpoints.detect import emoRouter
from service.api.endpoints.test import testRouter

apiRouter = APIRouter()
apiRouter.include_router(testRouter)
apiRouter.include_router(emoRouter)

