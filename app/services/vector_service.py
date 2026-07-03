import json
from pathlib import Path
from typing import List

import faiss
import numpy as np

from app.core.logger import get_logger

logger = get_logger(__name__)


class VectorService:
    """
    Handles FAISS vector indexing and retrieval.
    """

    INDEX_PATH = Path("vectorstore/faiss.index")
    METADATA_PATH = Path("vectorstore/metadata.json")

    def __init__(self, dimension: int):
        self.dimension = dimension

        self.INDEX_PATH.parent.mkdir(
            exist_ok=True,
            parents=True,
        )

        if self.INDEX_PATH.exists():

            self.index = faiss.read_index(
                str(self.INDEX_PATH)
            )

        else:

            self.index = faiss.IndexFlatL2(
                dimension
            )

        if self.METADATA_PATH.exists():

            with open(
                self.METADATA_PATH,
                "r",
                encoding="utf-8",
            ) as file:

                self.metadata = json.load(file)

        else:

            self.metadata = []
    
    def save(self):
        faiss.write_index(
            self.index,
            str(self.INDEX_PATH),
        )

        with open(
            self.METADATA_PATH,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                self.metadata,
                file,
                ensure_ascii=False,
                indent=4,
            )
    
    def add_embeddings(
        self,
        embeddings: List[List[float]],
        document_id: int,
        chunks: List[str],
    ):

        vectors = np.array(
            embeddings,
            dtype=np.float32,
        )

        self.index.add(vectors)

        for i, chunk in enumerate(chunks):

            self.metadata.append(
                {
                    "document_id": document_id,
                    "chunk_index": i,
                    "text": chunk,
                }
            )

        self.save()

        logger.info(
            "%d chunks indexed.",
            len(chunks),
        )

    def search(
        self,
        embedding: List[float],
        top_k: int = 5,
    ):

        vector = np.array(
            [embedding],
            dtype=np.float32,
        )

        distances, indices = self.index.search(
            vector,
            top_k,
        )

        results = []

        for idx in indices[0]:

            if idx == -1:
                continue

            results.append(
                self.metadata[idx]
            )

        return results
    
    