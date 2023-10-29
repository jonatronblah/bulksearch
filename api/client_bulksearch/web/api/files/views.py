from fastapi import APIRouter, Request, Depends
from fastapi.responses import StreamingResponse, FileResponse
from elasticsearch import AsyncElasticsearch
import os
import asyncio
import aiohttp

from client_bulksearch.db.models.users import current_active_user
from client_bulksearch.es_operations import generate_results, dosearch, create_rs_df


ES_HOST = os.getenv("ES_HOST")
ES_USER = os.getenv("ES_USER")
ES_PASS = os.getenv("ES_PASS")

router = APIRouter()

current_user = current_active_user


@router.post("/clientsearch")
async def process_json(request: Request, user=Depends(current_user), index='client'):
    terms = await request.json()
    terms = set(terms)
    es = AsyncElasticsearch(
        ES_HOST,
        # ca_certs="/path/to/http_ca.crt",
        basic_auth=(ES_USER, ES_PASS),
        verify_certs=False,
        request_timeout=300,
    )
    # s = [
    #         dosearch(
    #             index=index,
    #             body=i,
    #             client=es,
    #             term=i["query"]["match"]["ClientName"]["query"],
    #         )
    #         for i in bodies
    #     ]
    awaitables = [dosearch(index=index, term=i, client=es) for i in terms]
    r = await asyncio.gather(*awaitables)
    await es.close()

    # r = await asyncio.gather(*s)
    df = create_rs_df(results=r)
    spooled = generate_results(df)
    # df.to_csv('/app/src/test.csv')
    return StreamingResponse(spooled, media_type="text/csv")
