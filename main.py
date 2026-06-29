import asyncio
import json
import aiofiles
import os
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# task 1
@app.get("/")

def home():
    return {"message": "FastAPI is running"}


# task 2
FILE_PATH = "intern_data.json"

async def read_intern_data():
    if not os.path.exists(FILE_PATH):
        return []
    
    async with aiofiles.open(FILE_PATH, "r") as file:
        content = await file.read()
        return json.loads(content) if content else []



async def write_intern_data(data):
    async with aiofiles.open(FILE_PATH, "w") as file:
        await file.write(json.dumps(data, indent=4))


# task 3
class InternCreate(BaseModel):
    name: str
    role: str
    
def _generate_intern_id(interns):
    """Generate unique intern ID like INT001, INT002"""
    if not interns:
        return "INT001"

    numeric_ids = [
        int(i["intern_id"][3:])
        for i in interns
        if i.get("intern_id", "").startswith("INT")
    ]

    max_id = max(numeric_ids) if numeric_ids else 0
    return f"INT{max_id + 1:03d}"

@app.post("/interns")
async def add_intern(intern: InternCreate):
    interns = await read_intern_data()

    intern_id = _generate_intern_id(interns)

    new_intern = {
        "intern_id": intern_id,
        "name": intern.name,
        "role": intern.role,
        "status": "Active",
        "daily_hours": [],  
        "daily_tasks": []  
    }

    interns.append(new_intern)
    await write_intern_data(interns)

    return {
        "message": "Intern added successfully",
        "intern_id": intern_id
    }



# task 4
from typing import List

class ActivityInput(BaseModel):
    hours: float
    tasks: List[str]


@app.post("/interns/{intern_id}/activity")
async def add_activity(intern_id: str, activity: ActivityInput):
    interns = await read_intern_data()
    intern_id = intern_id.upper()   

    for intern in interns:
        if intern["intern_id"] == intern_id:
            if intern["status"] != "Active":
                return {"error": "Intern is not active"}


# task 5
@app.get("/interns/{intern_id}/summary")
async def view_intern_summary(intern_id: str):
    interns = await read_intern_data()

    for intern in interns:
        if intern["intern_id"] == intern_id:
            daily_hours = intern.get("daily_hours", [])
            total_hours = sum(daily_hours)
            average_hours = total_hours / len(daily_hours) if daily_hours else 0

            return {
                "intern_id": intern_id,
                "name": intern["name"],
                "role": intern["role"],
                "status": intern["status"],
                "total_hours": total_hours,
                "average_hours": average_hours,
                "daily_tasks": intern.get("daily_tasks", [])
            }

    return {"error": "Intern not found"}


# task 6 
@app.get("/statistics")
async def overall_statistics():
    interns = await read_intern_data()

    total_interns = len(interns)
    total_hours_all = 0
    top_performer = None
    max_hours = None

    for intern in interns:
        daily_hours = intern.get("daily_hours", [])
        total_hours = sum(daily_hours)
        total_hours_all += total_hours

        if max_hours is None or total_hours > max_hours:
            max_hours = total_hours
            top_performer = {
                "intern_id": intern["intern_id"],
                "name": intern["name"],
                "role": intern["role"],
                "total_hours": total_hours
            }

    average_hours = total_hours_all / total_interns if total_interns > 0 else 0

    return {
        "total_interns": total_interns,
        "average_hours": average_hours,
        "top_performer": top_performer
    }


# task 7
class TestInput(BaseModel):
    delay_seconds: int

@app.post("/test-async")
async def test_async(input_data: TestInput):
    await asyncio.sleep(input_data.delay_seconds)
    return {"message": f"Finished after {input_data.delay_seconds} seconds"}