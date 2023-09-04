import os
import pathlib

from core.knowledgebase.MemgraphManager import MemgraphManager
from core.knowledgebase.notes.CollectionManager import CollectionManager

class Initializer:
    @staticmethod
    def init_vault_mock_data() -> None:
        mm = MemgraphManager()
        cm = CollectionManager()

        mm.delete_all()
        cm.delete_all()

        history_repo_name = 'History'
        tech_repo_name =  'Technology'

        mock_repos_path = os.path.join(os.path.dirname(__file__), 'mock_repos')
        mock_cypherls_path = os.path.join(os.path.dirname(__file__), 'mock_cypherls')

        history_repo_path = os.path.join(mock_repos_path, history_repo_name)
        tech_repo_path = os.path.join(mock_repos_path, tech_repo_name)

        cm_history = CollectionManager(history_repo_path)
        cm_tech = CollectionManager(tech_repo_path)

        history_notes = ['alexander', 'caesar', 'napoleon']
        tech_notes = ['generator', 'steam_engine']

        mm = MemgraphManager()

        for note in history_notes:
            note_path = (os.path.join(history_repo_path, note) + '.md').replace("\\","/")
            cypherl_path = os.path.join(mock_cypherls_path, history_repo_name, note) + '_cypherl.txt'
            cm_history.add_file(note_path)
            mm.run_update_query(pathlib.Path(cypherl_path).read_text())
            mm.update_embeddings(note_path)

        for note in tech_notes:
            note_path = (os.path.join(tech_repo_path, note) + '.md').replace("\\","/")
            cypherl_path = os.path.join(mock_cypherls_path, tech_repo_name, note) + '_cypherl.txt'
            cm_tech.add_file(note_path)
            mm.run_update_query(pathlib.Path(cypherl_path).read_text())
            mm.update_embeddings(note_path)

        return

if __name__ == '__main__':
    Initializer.init_vault_mock_data()