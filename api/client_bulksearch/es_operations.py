import pandas as pd
from elasticsearch import AsyncElasticsearch, Elasticsearch
import asyncio
import os
from functools import reduce
from fastapi import Request
from io import BytesIO
import json

ES_HOST = os.getenv("ES_HOST")
ES_USER = os.getenv("ES_USER")
ES_PASS = os.getenv("ES_PASS")


async def dosearch(index, term, client):
    body = {
                "query": {
                    "match": {
                        "ClientName": {
                            "query": term,
                            "operator": "or",
                            "fuzziness": "auto",
                        }
                    }
                }
            }
    r = await client.search(index=index, body=body)
    r = dict(r)
    r["term"] = term
    return r


# def generate_queries(terms):
#     bodies = []
#     for i in terms:
#         bodies.append(
#             {
#                 "query": {
#                     "match": {
#                         "ClientName": {
#                             "query": i,
#                             "operator": "or",
#                             "fuzziness": "auto",
#                         }
#                     }
#                 }
#             }
#         )
    
#     return bodies


def combine(df):
    df_list = []
    for i in range(0, 3):
        dfm = df.merge(
            pd.DataFrame(df[i].tolist(), index=df.index),
            left_index=True,
            right_index=True,
        ).drop(["0_x", "1_x", 2], axis="columns")
        df_list.append(dfm)
    df_final = reduce(lambda x, y: pd.merge(x, y, on="term"), df_list)
    return df_final


def create_rs_df(results, n=3):
    res_list = []
    for i in results:
        r_dict = {}
        r_dict["term"] = i["term"]
        r_dict["results"] = [
            (j["_source"]["ClientName"], j["_score"]) for j in i["hits"]["hits"][:n]
        ]
        res_list.append(r_dict)
    df = pd.DataFrame(res_list)
    df = df.set_index("term")
    df = df.merge(
        (pd.DataFrame(df["results"].tolist(), index=df.index)),
        left_index=True,
        right_index=True,
    ).drop("results", axis="columns")
    df = combine(df)
    return df


# def gather_results(bodies, index='client', host=ES_HOST, user=ES_USER, password=ES_PASS):
#     es = AsyncElasticsearch(
#         host,
#         # ca_certs="/path/to/http_ca.crt",
#         basic_auth=(user, password),
#         verify_certs=False,
#         request_timeout=300,
#     )

#     s = [
#             dosearch(
#                 index=index,
#                 body=i,
#                 client=es,
#                 term=i["query"]["match"]["ClientName"]["query"],
#             )
#             for i in bodies
#         ]
    
#     return s

# async def search(s):
#     r = await asyncio.gather(s)
#     return r

    # return await asyncio.gather(
    #     *[
    #         dosearch(
    #             index=index,
    #             body=i,
    #             client=es,
    #             term=i["query"]["match"]["ClientName"]["query"],
    #         )
    #         for i in bodies
    #     ]
    # )
    

def generate_results(df):
    spooled = BytesIO()
    df.to_csv(spooled)
    spooled.seek(0)
    return spooled

def rec_to_actions(df, index_name):
    for record in df.to_dict(orient="records"):
        yield ('{ "index" : { "_index" : "%s" }}'% (index_name))
        yield (json.dumps(record, default=int))

def index_data(data, index_name, host=ES_HOST, user=ES_USER, password=ES_PASS, replace=True):
    if replace:
        client = Elasticsearch(
            host,
            # ca_certs="/path/to/http_ca.crt",
            basic_auth=(user, password),
            verify_certs=False,
            request_timeout=300
        )
        client.indices.create(index=index_name, ignore=400)
        r = client.bulk(index=index_name, body=rec_to_actions(data, index_name))
        return r
