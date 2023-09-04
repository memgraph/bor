from __future__ import annotations

from typing import List, Optional, Any

import os

from core.knowledgebase.notes.Embeddings import Embeddings
from core.knowledgebase.MemgraphManager import MemgraphManager
from core.knowledgebase.notes.CollectionManager import CollectionManager


class Searcher:
    def __init__(self: Searcher, repo_path: str) -> None:
        self.repo_path = repo_path
        self.mm = MemgraphManager()
        return

    def search_graph(self: Searcher, query_text: Optional[str] = None, query_embeddings: Optional[List[float]] = None) -> List[Any]:
        assert (query_text is not None) or (query_embeddings is not None)
        if query_text is not None:
            emb_vector = Embeddings.get_embedding(query_text)
        else:
            emb_vector = query_embeddings
            
        self.mm.create_temp_nodes(emb_vector)
        results = None
        try:
            results = self.mm.vector_search_query()
        finally:
            self.mm.delete_temp_nodes()
        return list(results)


    def search_graph_tool(self: Searcher, query: str) -> str:
        results = self.search_graph(query_text=query)
        out = ""
        for res in results:
            out += self.mm.describe_node(res['ID(node1)'])
            out += "-------------\n"
        return out
    
    def search_text(self: Searcher, query_text: Optional[str] = None, query_embeddings: Optional[List[float]] = None) -> List[str]:
        cm = CollectionManager(self.repo_path)
        res = cm.collection.query(
            query_texts=query_text,
            query_embeddings=query_embeddings,
            n_results=3,
        )
        return res['documents'][0]
    
    def search_text_tool(self: Searcher, query: str) -> str:
        return '\n'.join(self.search_text(query_text=query))
    

    def node_id_to_sentences(self: Searcher, id: int) -> List[str]:
        emb = self.mm.embeddings_for_node(id)
        return self.search_text(query_embeddings=emb)

    def sentence_to_node_ids(self: Searcher, sentence: str) -> List[int]:
        cm = CollectionManager(self.repo_path)
        res = cm.collection.query(
            query_texts=sentence,
            n_results=1,
            include=['embeddings']
        )
        emb = res['embeddings'][0][0]
        return [node['ID(node1)'] for node in self.search_graph(query_embeddings=emb)]
    
    def most_probable_filename_for_text(self: Searcher, query_text: Optional[str] = None) -> str:
        cm = CollectionManager(self.repo_path)
        res = cm.collection.query(
            query_texts=query_text,
            query_embeddings=None,
            n_results=1
        )
        fname = res['metadatas'][0][0]['file_path']
        return fname
        

if __name__ == '__main__':
    query_text = "counsul"
    example_reponame = 'History'
    example_repopath = os.path.join(os.path.dirname(__file__), '..', 'examples', example_reponame)
    searcher = Searcher(example_reponame)

    print(searcher.search_graph(query_text=query_text))
    print(searcher.search_text(query_text=query_text))
    print(searcher.most_probable_filename_for_text(query_text))
    print(searcher.node_id_to_sentences(searcher.sentence_to_node_ids('Napoleon bonaparte was born')[0]))