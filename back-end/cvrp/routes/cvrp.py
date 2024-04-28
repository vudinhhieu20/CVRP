import os
import sys
import time
import traceback
from datetime import datetime, timedelta
from pathlib import Path
from typing import Annotated, Optional

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    Header,
    HTTPException,
    UploadFile,
    status,
)
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from logger import customLogger as logger
from pydantic import BaseModel
from starlette.requests import Request

# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))

# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)

# adding the parent directory to
# the sys.path.
sys.path.append(parent)

from core.cvrp import CVRP

UPLOAD_DIR = str(Path()) + "/uploads/"

import os

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

router = APIRouter()


class CVRPRoutes(BaseModel):
    routes_greedy: Optional[list[list[int]]] = None
    routes_saving: Optional[list[list[int]]] = None


class CVRPResponse(BaseModel):
    bus_stop_coord: Optional[list[list[float]]] = None
    bus_stop_assign: Optional[list[list[str]]] = None
    routes: Optional[CVRPRoutes] = None


@router.post("/upload_file/", response_model=CVRPResponse)
async def upload_file_for_cvrp(
    # file_upload: Annotated[UploadFile, File()],
    # # max_student: Optional[int] = 10,
    # # max_distance: Optional[int] = 20,
    # # max_capacity: Optional[int] = 10,
    # max_student: Annotated[int, Form()],
    # max_distance: Annotated[int, Form()],
    # max_capacity: Annotated[int, Form()],
    file_upload: UploadFile = File(),
    max_student: str = Form(),
    max_distance: str = Form(),
    max_capacity: str = Form(),
):
    print("Start handle upload file")
    try:
        data = file_upload.file.read()
        file_extension = file_upload.filename.split(".")[-1]
        if file_extension != "xls" and file_extension != "xlsx":
            return JSONResponse(
                status_code=400,
                content={"message": f"Oops! did something. There goes a rainbow..."},
            )
        print("Max student upload: ", int(max_student))
        print("Max distance upload: ", int(max_distance))
        print("Max capacity upload: ", int(max_capacity))
        cvrpSolver = CVRP(
            raw_bytes_dataset=data,
            max_distance_from_node=int(max_distance),
            max_student_per_node=int(max_student),
            bus_capacity=int(max_capacity),
        )
        cluster_centroids, cluster_assign_labels, routes = cvrpSolver.solve()

        # save_to = UPLOAD_DIR + file_upload.filename
        # print("Saving path: " + save_to)

        # with open(save_to, "wb") as f:
        #     f.write(data)

        cluster_centroids = cluster_centroids.tolist()

        print("cluster_centroids: ", cluster_centroids)
        print("cluster_assign: ", cluster_assign_labels)
        print("routes: ", routes)
        routesResponse = CVRPRoutes(
            routes_greedy=routes["routes_greedy"], routes_saving=routes["routes_saving"]
        )
        response = CVRPResponse(
            bus_stop_coord=cluster_centroids,
            bus_stop_assign=cluster_assign_labels,
            routes=routesResponse,
        )

    except Exception as e:
        print(e)
        traceback.print_exc()

    return response
