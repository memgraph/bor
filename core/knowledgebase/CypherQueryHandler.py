from typing import List

class CypherQueryHandler:

    @staticmethod
    def get_check_if_db_empty_query() -> str:
        return (f"MATCH (n)"
                f"RETURN count(n) AS nodes")

    @staticmethod
    def get_export_for_repo_path_query(repo_path: str) -> str:
        return (f"MATCH p=(n {{ repo_path: '{repo_path}' }})-[r]->(m {{ repo_path: '{repo_path}' }}) "
                f"WITH project(p) AS repo_specific_subgraph "
                f"RETURN repo_specific_subgraph")
    
    @staticmethod
    def get_export_for_file_path_query(file_path: str) -> str:
        return (f"MATCH p=(n {{ file_path: '{file_path}' }})-[r]->(m {{ file_path: '{file_path}' }}) "
                f"WITH project(p) AS file_specific_subgraph "
                f"RETURN file_specific_subgraph")
    
    @staticmethod
    def get_delete_all_query() -> str:
        return (f"MATCH (n) "
                "DETACH DELETE n")

    @staticmethod
    def get_delete_all_for_repo_query(repo_path: str) -> str:
        return (f"MATCH (n) "
                f"WHERE n.repo_path = '{repo_path}' "
                f"DETACH DELETE n")
    
    @staticmethod
    def get_delete_graph_for_file_query(file_path: str) -> str:
        return (f"MATCH (n) "
                f"WHERE n.file_path = '{file_path}' "
                f"DETACH DELETE n")

    @staticmethod
    def get_rename_file_query(old_file_path: str, new_file_path: str) -> str:
        return (f"MATCH (n)"
                f"WHERE n.file_path = '{old_file_path}'"
                f"SET n.file_path = '{new_file_path}'")
    
    @staticmethod
    def get_strings_to_embed_query(file_path: str) -> str:
        return (f"MATCH (n) "
                f"OPTIONAL MATCH (n)-[r]->(m) "
                f"WHERE n.file_path = '{file_path}' "
                f"RETURN ID(n) as Node_ID, " 
                f"n.name as Node_Name, "
                f"labels(n)[0] as Node_Type, "
                f"collect({{Neighbour_Name: m.name, Neighbour_Type: labels(m)[0], Relationship_Type: type(r)}}) as Connections")

    @staticmethod
    def get_node_description_query(node_id: int) -> str:
        return  (f"MATCH (n) "
                f"WHERE ID(n) = {node_id} "
                f"OPTIONAL MATCH (n)-[r1]->(m) "
                f"OPTIONAL MATCH (p)-[r2]->(n) "
                f"RETURN ID(n) as Node_ID,  "
                f"n.name as Node_Name, "
                f"labels(n)[0] as Node_Type, "
                "collect({ Neighbour_Name: m.name, Neighbour_Type: labels(m)[0], Relationship_Type: type(r1) }) as In_Connections, "
                "collect({ Neighbour_Name: p.name, Neighbour_Type: labels(p)[0], Relationship_Type: type(r2) }) as Out_Connections")

    @staticmethod
    def get_set_embeddings_query(node_id: str, embeddings: List[float]) -> str:
        return (f"MATCH (n) "
                f"WHERE ID(n) = {node_id} "
                f"SET n.embeddings =  {embeddings} ")
    
    @staticmethod
    def get_tmp_create_query(embeddings: List[float]) -> str:
        return (f"MATCH (n) "
                f"WITH count(n) as N "
                f"UNWIND range(1, N) as id "
                f"CREATE (:Temp {{name: 'temp_'+id, embeddings: {embeddings} }}) ")
    
    @staticmethod
    def get_tmp_delete_query() -> str:
        return (f"MATCH (n:Temp) "
                f"DETACH DELETE n ")

    @staticmethod
    def get_schema_for_repo_query(repo_path: str) -> str:
        return (f"MATCH p=(n {{ repo_path: '{repo_path}' }})-[r]->(m {{ repo_path: '{repo_path}' }}) "
                f"WITH project(p) AS repo_specific_subgraph "
                f"CALL llm_util.schema(repo_specific_subgraph, 'prompt_ready') "
                f"YIELD schema "
                f"RETURN schema")
    
    @staticmethod
    def get_vector_search_query() -> str:
        return ("MATCH (m) "
                "WHERE (NOT m.name STARTS WITH 'temp') OR (m.name IS NULL) "
                "WITH COLLECT(m) as nodes "
                "MATCH (tmp) "
                "WHERE tmp.name STARTS WITH 'temp' "
                "WITH COLLECT(tmp) as temps, nodes "
                "CALL node_similarity.cosine_pairwise('embeddings', nodes, temps) YIELD node1, node2, similarity as cosine_similarity "
                "RETURN ID(node1), cosine_similarity "
                "ORDER BY cosine_similarity DESC "
                "LIMIT 3")
    
    @staticmethod
    def get_embeddings_for_node_query(node_id: int) -> str:
        return (f"MATCH (m) "
                f"WHERE ID(m) = {node_id} "
                f"RETURN m.embeddings as embeddings")
