
import numpy as np
import typesense

from ..base.module import BaseANN


class typesenseHnsw(BaseANN):
    def __init__(self, metric, method_param):
        print("Initializing Typesense HNSW Method Parameters:", method_param)
        self.metric = {"angular": "cosine", "euclidean": "l2"}[metric]
        self.name = 'typesenseHnsw'
        self.client = typesense.Client(
            {
                "nodes": [{
                    "host": "localhost",
                    "port": "8108",
                    "protocol": "http"
                }],
                "api_key": "aaa",
                "connection_timeout_seconds": 2000000,
            }
        )
        self.method_param = method_param
        self.documents = []

    def fit(self, X):
        # Only l2 is supported currently
        print("Indexing", X.shape[0], "vectors of dimension", X.shape[1])
        schema = {
            "name": "ann_benchmark",
            "fields": [
                {"name": '_id', "type": "int32"},
                {"name": "vector", "type": "float[]", "num_dim": X.shape[1], "hnsw_params": { "M": self.method_param["M"] } },
            ]
        }
        try:
            self.client.collections.create(schema)
        except Exception as e:
            print(e)
            self.client.collections["ann_benchmark"].delete()
            self.client.collections.create(schema)
        self.documents = []
        for i, x in enumerate(X):
            self.documents.append({"_id": i, "vector": x.tolist()})
        self.client.collections["ann_benchmark"].documents.import_(self.documents)
        print("Indexed", len(self.documents), "documents")
    def set_query_arguments(self, params):
        if params.get("deleteAndReindex", False):
            print("Deleting and re-indexing all documents")
            start = int(params.get("start", 0) * len(self.documents))
            end = int(params.get("end", len(self.documents)) * len(self.documents))
            print("Re-indexing documents with _id in range [{}, {})".format(start, end))
            self.client.collections["ann_benchmark"].documents.delete({"filter_by": "_id:>= {}&&_id:< {}".format(start, end)})
            print("Deleted documents with _id in range [{}, {})".format(start, end))
            self.client.collections["ann_benchmark"].documents.import_(self.documents[start:end])
            print("Re-indexed documents with _id in range [{}, {})".format(start, end))

    def query(self, v, n):
        # print(np.expand_dims(v,axis=0).shape)
        # print(self.p.knn_query(np.expand_dims(v,axis=0), k = n)[0])
        res = self.client.collections["ann_benchmark"].documents.search({
            "q": "*",
            "vector_query": "vector:([{}], k:{})".format(','.join(map(str, v)), n),
        })
        return [hit['document']['_id'] for hit in res['hits']]

    def freeIndex(self):
        del self.client
