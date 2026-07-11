from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import json

from graph import graph

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)


class Query(BaseModel):
    query: str


@app.post("/query")
def query(data: Query):

    def generate():

        state = {"query": data.query}

        for event in graph.stream(state):

            node = list(event.keys())[0]
            values = event[node]

            yield f"data:{json.dumps({'type':'progress','node':node})}\n\n"

            if node == "response":

                payload = {

                    "type":"answer",

                    "answer":values["answer"],

                    "entity":values["entity"],

                    "source":values["source"],

                    "archive_url":values["archive_url"],

                    "object_type":values["object_type"]

                }

                yield f"data:{json.dumps(payload)}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream"
    )