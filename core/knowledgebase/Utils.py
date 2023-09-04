from typing import List

import os
import glob

class Utils:
    @staticmethod
    def collection_name_from_repo_path(repo_path: str) -> str:
        return os.path.basename(os.path.normpath(repo_path))
    
    @staticmethod
    def repo_path_from_file_path(file_path: str) -> str:
        return os.path.dirname(file_path)
    
    @staticmethod
    def collection_name_from_file_path(file_path: str) -> str:
        return Utils.collection_name_from_file_path(Utils.repo_path_from_file_path(file_path))

    @staticmethod
    def get_all_files_recursive(path_to_root: str) -> List[str]:
        search_path = os.path.join(path_to_root, '**', '*')
        return [os.path.abspath(f) for f in glob.glob(search_path, recursive=True) if os.path.isfile(f)]

    @staticmethod
    def edge_to_dict(edge):
        return {
            "id": edge.id,
            "start": edge.start_id,
            "end": edge.end_id,
            "label": edge.type,
            "properties": edge.properties,
            "type": type(edge).__name__.lower(),
        }

    @staticmethod
    def node_to_dict(node):
        return {
            "id": node.id,
            "labels": list(node.labels),
            "properties": node.properties,
            "type": type(node).__name__.lower(),
        }

    @staticmethod
    def results_to_dictlist(results, return_name):
        l = list(results)
        nodes = l[0][return_name]['nodes']
        edges = l[0][return_name]['edges']

        # new_results =  [{
        #     return_name : {
        #         'nodes': [Utils.node_to_dict(n) for n in nodes],
        #         'edges': [Utils.edge_to_dict(e) for e in edges]
        #     }
        # }]

        new_results = [Utils.node_to_dict(n) for n in nodes] + [Utils.edge_to_dict(e) for e in edges]

        return new_results