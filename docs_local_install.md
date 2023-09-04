# Setup

1. Make a conda venv using Python 3.9.16:
```
conda create --name bor_env python=3.9.16
```
2. Activate the environment:
```
source activate bor_env
```
3. To install all requirements and setup all packages, run:
```
pip install -e .
```
4. You have to have an .env file which looks like this:
```
OPENAI_API_KEY="..."
MEMGRAPH_HOST="127.0.0.1"
MEMGRAPH_PORT=7687
CHROMA_DATA_DIR="/path/to/dir/chroma"
CHROMA_VECTOR_SPACE="cosine"
EMBEDDING_MODEL_NAME="text-embedding-ada-002"
LLM_MODEL_NAME="gpt-3.5-turbo-0613"
LLM_MODEL_TEMPERATURE=0.2
```

5. Run & install Memgraph with `run_memgraph_290.sh`

6. Run the FastAPI backend with `run_server.sh`

7. If you want to populate Memgraph with previously prepared mock Obsidian Vaults inside `core/knowledgebase/mock_repos`:

    1. Change every every `file_path` and `repo_path` value inside `core/knowledgebase/mock_cypherls` to match the one you want on your system (currently it's set to `/home/patrik/something`, which obviously isn't correct in your case)

    2. Do:
    ```
    cd backend/core/knowledgebase
    python Initializer.py
    ```

