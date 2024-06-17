from io import BytesIO

from fastapi import UploadFile, File, Depends
from fastapi.routing import APIRouter
from PIL import Image

from lib.pytorch_prediction import PytorchPrediction
from api.responses.response import Responses
from api.schemas import Review

router = APIRouter(tags=['prediction'])
pytorch_model = PytorchPrediction()


def get_pytorch_model():
    return pytorch_model


@router.get("/")
async def index():
    return {'result': 'exito'}


@router.post("/pytorch_predict")
async def pytorch_predict(
    review: Review,
    model: PytorchPrediction = Depends(get_pytorch_model)
):

    class_name, score = model.predict(review.text)
    data = {"class_name": class_name, "score": score}
    return Responses.ok(data)
