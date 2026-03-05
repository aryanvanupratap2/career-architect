from fastapi import APIRouter
from career.service import generate_career_path

router = APIRouter(prefix="/career", tags=["Career"])


@router.post("/generate")
async def generate(data: dict):

    roadmap = await generate_career_path(data)


    return {"roadmap": roadmap}

