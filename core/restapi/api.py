from typing import Union, List

from enum import Enum
from core.knowledgebase.Utils import Utils

from fastapi import FastAPI, status, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse 
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from core.knowledgebase import constants

from core.knowledgebase.Initializer import Initializer
from core.knowledgebase.MemgraphManager import MemgraphManager
from core.knowledgebase.TextAnalizer import TextAnalizer
from core.knowledgebase.QueryAgents import NotesQueryAgent, CodeQueryAgent

from core.knowledgebase.notes.VaultManager import VaultManager
from core.knowledgebase.notes.CollectionManager import CollectionManager
from core.knowledgebase.notes.Searcher import Searcher

from core.knowledgebase.code.APIRepoManager import APIRepoManager
from core.knowledgebase.code.LocalRepoManager import LocalRepoManager

class Type(Enum):
    NOTES = "Notes"
    CODE = "Code"

class Repo(BaseModel):
    path: str
    type: Union[Type, None] = None

class RemoteRepo(BaseModel):
    owner: str
    repo: str

class File(BaseModel):
    path: str
    type: Union[Type, None] = None
    content: Union[str, None] = None

class Question(BaseModel):
    repo: Repo
    prompt: str
    type: Union[Type, None] = None

class Answer(BaseModel):
    content: str


class Node(BaseModel):
    repo: Repo
    id: int

class Sentence(BaseModel):
    repo: Repo
    content: str

class Paragraph(BaseModel):
    content: str


app = FastAPI()
mm = MemgraphManager()
ta = TextAnalizer()


@app.on_event("startup")
def startup() -> None:
    if constants.MOCK and mm.check_if_db_empty():
        Initializer.init_vault_mock_data()
    return


@app.post("/knowledge_base/general/get_all_for_repo")
def get_all_for_repo(repo: Repo) -> Response:
    data = mm.export_data_for_repo_path(repo.path)
    if data:
        json_data = jsonable_encoder(data)
        return JSONResponse(content=json_data)
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
@app.delete("/knowledge_base/general/delete_all_for_repo")
def delete_all_for_repo(repo: Repo) -> None:
    mm.delete_all_for_repo(repo.path)
    if repo.type == Type.NOTES:
        cm = CollectionManager(repo.path)
        cm.delete_all_from_collection()
    return

@app.post("/knowledge_base/general/ask")
def ask_repo(question: Question) -> Answer:
    if question.type == Type.NOTES:
        na = NotesQueryAgent(question.repo.path)
        return Answer(content=na.ask(question.prompt))

    ca = CodeQueryAgent(question.repo.path)
    return Answer(content=ca.ask(question.prompt))

@app.post("/knowledge_base/general/get_schema")
def get_schema(repo: Repo) -> Answer:
    return Answer(content=mm.get_schema_for_repo(repo.path))

# TODO: test with GPT4
@app.post("/knowledge_base/general/init_local_repo")
def init_repo(repo: Repo) -> None:
    if repo.type == Type.CODE:
        lrm = LocalRepoManager(repo.path)
        cypher = lrm.generate_cypher()
        mm.run_update_query(cypher)
        return
    vm = VaultManager(repo.path)
    vm.populate_vault()
    return

@app.post("/knowledge_base/general/delete_all")
def delete_all() -> None:
    cm = CollectionManager()
    mm.delete_all()
    cm.delete_all()
    return



@app.post("/knowledge_base/text_analizer/code/optimize_style")
def optimize_syle(paragraph: Paragraph) -> Answer:
    ta = TextAnalizer()
    return Answer(content=ta.optimize_code_style(paragraph.content))

@app.post("/knowledge_base/text_analizer/code/explain")
def explain_code(paragraph: Paragraph) -> Answer:
    ta = TextAnalizer()
    return Answer(content=ta.explain_code(paragraph.content))

@app.post("/knowledge_base/text_analizer/code/debug")
def debug_code(paragraph: Paragraph) -> Answer:
    ta = TextAnalizer()
    return Answer(content=ta.debug_code(paragraph.content))

@app.post("/knowledge_base/text_analizer/notes/generate_questions")
def generate_questions(paragraph: Paragraph) -> Answer:
    ta = TextAnalizer()
    return Answer(content=ta.generate_questions(paragraph.content))



@app.post("/knowledge_base/notes/get_for_path")
def get_for_path(file: File) -> Response:
    mm = MemgraphManager()
    data = mm.export_data_for_file_path(file.path)
    if data:
        json_data = jsonable_encoder(data)
        return JSONResponse(content=json_data)
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)    

# TODO: test with GPT4
@app.put("/knowledge_base/notes/update_file")
def update_file(file: File) -> None:
    mm = MemgraphManager()
    repo_path = Utils.repo_path_from_file_path(file.path)

    cm = CollectionManager(repo_path)
    ta = TextAnalizer()

    data = mm.export_data_for_repo_path(repo_path)

    mm.delete_graph_for_file(file.path)
    cm.delete_file(file.path)

    if isinstance(data, list) and len(data) == 0:
        res_queries = ta.text_to_cypher_create(file.content, repo_path, file.path)
    else:
        res_queries = ta.data_and_text_to_cypher_update(data, file.content, repo_path, file.path)
    
    mm.run_update_query(res_queries)
    cm.add_file(file.path)

    for path in Utils.get_all_files_recursive(repo_path):
        mm.update_embeddings(path)

    return

# TODO: test with GPT4
@app.put("/knowledge_base/notes/add_file")
def add_file(file: File) -> None:
    mm = MemgraphManager()
    repo_path = Utils.repo_path_from_file_path(file.path)

    cm = CollectionManager(repo_path)
    ta = TextAnalizer()

    data = mm.export_data_for_repo_path(repo_path)

    if isinstance(data, list) and len(data) == 0:
        res_queries = ta.text_to_cypher_create(file.content, repo_path, file.path)
    else:
        res_queries = ta.data_and_text_to_cypher_update(data, file.content, repo_path, file.path)

    mm.run_update_query(res_queries)
    cm.add_file(file.path)

    for path in Utils.get_all_files_recursive(repo_path):
        mm.update_embeddings(path)

    return

@app.delete("/knowledge_base/notes/delete_file")
def delete_file(file: File) -> None:
    repo_path = Utils.repo_path_from_file_path(file.path)
    mm = MemgraphManager()
    cm = CollectionManager(repo_path)
    mm.delete_graph_for_file(file.path)
    cm.delete_file(file.path)
    return

@app.post("/knowledge_base/notes/rename_file")
def rename_file(old_file: File, new_file: File) -> None:
    repo_path = Utils.repo_path_from_file_path(old_file.path)
    mm = MemgraphManager()
    cm = CollectionManager(repo_path)
    mm.rename_file(old_file.path, new_file.path)
    cm.rename_file(old_file.path, new_file.path)
    return

@app.post("/knowledge_base/notes/node_to_sentences")
def node_to_sentences(node: Node) -> List[Sentence]:
    searcher = Searcher(node.repo.path)
    return [Sentence(repo=node.repo, content=c) for c in searcher.node_id_to_sentences(node.id)]

@app.post("/knowledge_base/notes/sentence_to_nodes")
def sentence_to_nodes(sentence: Sentence) -> List[Node]:
    searcher = Searcher(sentence.repo.path)
    return [Node(repo=sentence.repo, id=i) for i in searcher.sentence_to_node_ids(sentence.content)]

@app.post("/knowledge_base/notes/suggest_link")
def suggest_link(sentence: Sentence) -> File:
    searcher = Searcher(sentence.repo.path)
    return File(path=searcher.most_probable_filename_for_text(query_text=sentence.content))



@app.post("/knowledge_base/code/init_repo_from_api")
def init_repo_from_api(remote_repo: RemoteRepo) -> None:
    mm = MemgraphManager()
    arm = APIRepoManager(remote_repo.owner, remote_repo.repo)
    cypher = arm.generate_cypher()
    mm.run_update_query(cypher)
    return


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)