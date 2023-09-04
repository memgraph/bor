from __future__ import annotations

from typing import Optional, Tuple

import os
import ctypes
import yaml
from gitignore_parser import parse_gitignore

class LocalRepoManager:

    def __init__(self: LocalRepoManager, root_path: str) -> None:
        self.root_path = LocalRepoManager.remove_trailing_slash(root_path)
        return

    @staticmethod
    def detect_language(file_path: str) -> Optional[str]:
        with open(os.path.join(os.path.dirname(__file__), 'languages.yml'), 'r') as file:
            languages = yaml.load(file, Loader=yaml.FullLoader)
            file_extension = os.path.splitext(file_path)[1]

            for lang, data in languages.items():
                if 'extensions' in data and file_extension in data['extensions']:
                    return lang

        return None

    @staticmethod
    def analyze_file(file_path: str) -> Tuple[int, bool]:
        loc = 0
        marked_todo = False
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    loc += 1
                    if 'TODO:' in line:
                        marked_todo = True
        except UnicodeDecodeError:
            pass

        return loc, marked_todo

    @staticmethod
    def escape_cypher_value(file_path: str) -> str:
        return file_path.replace("\\", "\\\\").replace("'", "\\'")

    @staticmethod
    def node_with_hash(file_path: str) -> str:
        return f'node{str(ctypes.c_size_t(hash(file_path)).value)}'
    
    @staticmethod
    def remove_trailing_slash(file_path: str) -> str:
        if file_path.endswith('/'):
            return file_path[:-1]
        return file_path
    
    def generate_cypher(self: LocalRepoManager) -> str:
        queries = []
        repo_path = LocalRepoManager.escape_cypher_value(self.root_path)

        gitignore_path = os.path.join(self.root_path, '.gitignore')
        matches = parse_gitignore(gitignore_path)

        visited_dirs = []

        for root, dirs, files in os.walk(self.root_path):
            if '.git' in dirs:
                dirs.remove('.git')

            root = LocalRepoManager.remove_trailing_slash(root)
            dirs[:] = [LocalRepoManager.remove_trailing_slash(d) for d in dirs if not matches(os.path.join(root, d))]
            files = [f for f in files if not matches(os.path.join(root, f))]

            root_escaped = LocalRepoManager.escape_cypher_value(root)
            nn_root = LocalRepoManager.node_with_hash(f'dir_{root_escaped}')
            
            if nn_root not in visited_dirs:
                queries.append(f"MERGE ({nn_root}:Dir {{path: '{root_escaped}', repo_path: '{repo_path}'}})")
                visited_dirs.append(nn_root)

            for directory in dirs:
                directory_path = os.path.join(root, directory)
                directory_escaped = LocalRepoManager.escape_cypher_value(directory_path)

                nn_dir = LocalRepoManager.node_with_hash(f'dir_{directory_escaped}')

                if nn_dir not in visited_dirs:    
                    queries.append(f"MERGE ({nn_dir}:Dir {{path: '{directory_escaped}', repo_path: '{repo_path}'}})")
                    queries.append(f"CREATE ({nn_dir})-[:IN]->({nn_root})")
                    visited_dirs.append(nn_dir)

            for file in files:
                file_path = os.path.join(root, file)
                file_escaped = LocalRepoManager.escape_cypher_value(file_path)

                language = LocalRepoManager.detect_language(file_path)
                loc, marked_todo = LocalRepoManager.analyze_file(file_path)

                nn_file = LocalRepoManager.node_with_hash(f'file_{file_escaped}')

                attributes = f"path: '{file_escaped}', repo_path: '{repo_path}'"
                if language:
                    attributes += f", language: '{language}', LOC: {loc}, MARKED_TODO: {marked_todo}"
                queries.append(f"MERGE ({nn_file}:File {{{attributes}}})")
                queries.append(f"CREATE ({nn_file})-[:IN]->({nn_root})")

        return '\n'.join(queries)



if __name__ == '__main__':
    example_repo_path = '/home/patrik/Drive/Current/Memgraph/Projects/magic-graph/'
    rm = LocalRepoManager(example_repo_path)
    print(rm.generate_cypher())
