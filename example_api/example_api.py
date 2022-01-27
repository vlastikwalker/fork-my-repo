import sys
import logging
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
sys.path.append('..')
from utils.db import simple_query, delete_row, insert_row, update_row

tags_metadata = [
    {
        "name": "entrees",
        "description": "Operations with entrees.",
    },
]

app = FastAPI(
    title="Bento API",
    description="An example api built with FastAPI and Hypercorn",
    version="1.0.0",
    openapi_tags=tags_metadata
)

logging.basicConfig(filename='/var/log/bento/example_api.log', level=logging.DEBUG)
log = logging.getLogger(__name__)

class NewEntree(BaseModel):
    entree_name:str

class Entree(NewEntree):
    entree_id:int

@app.get("/")
async def root():
    return {"Hello": "World"}

@app.post('/entrees', response_model=Entree, status_code=201, tags=["entrees"])
async def create_entree(entree: NewEntree):
    """
    Create an entree
    - **entree_name**: each entree must have a name
    """
    entree_id = insert_row("INSERT INTO test.entree (entree_name) VALUES (:entree_name) RETURNING entree_id", entree.dict())

    return Entree(entree_id=entree_id, entree_name=entree.entree_name)

@app.get('/entrees', response_model=List[Entree], tags=["entrees"])
async def get_entrees():
    """
    Get all of the entrees
    """
    rows = simple_query('SELECT * FROM test.entree')
    return rows

@app.get('/entree/<entree_id>', response_model=Entree, tags=["entrees"])
async def get_entree(entree_id):
    """
    Get an entree by id
    - **entree_id**: the unique id of the entree
    """
    rows = simple_query('SELECT * FROM test.entree WHERE entree_id = :entree_id', {'entree_id': entree_id})
    if (len(rows) == 0):
        raise HTTPException(status_code=404, detail="Entree {} doesn't exist".format(entree_id))
    else:
        return rows[0]

@app.delete('/entree/<entree_id>', status_code=204, tags=["entrees"])
async def delete_entree(entree_id):
    """
    Delete an entree
    - **entree_id**: the unique id of the entree
    """ 
    rowcount = delete_row('DELETE FROM test.entree WHERE entree_id = :entree_id', {'entree_id': entree_id})
    if rowcount == 0:
        raise HTTPException(status_code=404, detail="Entree {} doesn't exist".format(entree_id))
    else:
        return ''

@app.put('/entree/<entree_id>', response_model=Entree, status_code=201, tags=["entrees"])
async def update_entree(entree_id:int, entree: Entree):
    """
    Update an entree
    - **entree_id**: the unique id of the entree
    - **entree_name**: update the name of the entree
    """
    rowcount = update_row("UPDATE test.entree SET entree_name = :entree_name WHERE entree_id = :entree_id", entree.dict())
    if (rowcount == 0):
        raise HTTPException(status_code=404, detail="Entree {} doesn't exist".format(entree_id))
    else:
        return entree