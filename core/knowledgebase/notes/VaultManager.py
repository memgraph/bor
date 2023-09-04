from __future__ import annotations

import pathlib

from core.knowledgebase import constants
from core.knowledgebase.Utils import Utils
from core.knowledgebase.TextAnalizer import TextAnalizer
from core.knowledgebase.MemgraphManager import MemgraphManager
from core.knowledgebase.notes.CollectionManager import CollectionManager

class VaultManager:
    def __init__(self: VaultManager, vault_path: str) -> None:
        self.vault_path = vault_path
        self.ta = TextAnalizer()
        self.mm = MemgraphManager()
        self.cm = CollectionManager(self.vault_path)

    def populate_vault(self: VaultManager) -> None:

        file_paths = Utils.get_all_files_recursive(self.vault_path)
        for i, file_path in enumerate(file_paths):

            file_text = pathlib.Path(file_path).read_text()
            if i == 0:
                res_queries = self.ta.text_to_cypher_create(file_text, self.vault_path, file_path)
            else:
                data = self.mm.export_data_for_repo_path(self.vault_path)
                res_queries = self.ta.data_and_text_to_cypher_update(str(data), file_text, self.vault_path, file_path)
            
            self.mm.run_update_query(res_queries)
            self.cm.add_file(file_path)
            
        for i, file_path in enumerate(file_paths):
            self.mm.update_embeddings(file_path)
        return