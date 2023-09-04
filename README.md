[![python](https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![fastapi](https://img.shields.io/badge/fastapi-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)

[![openai](https://img.shields.io/badge/openai-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com/)
[![docker](https://img.shields.io/badge/docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

# BOR - The Backend for ODIN and RUNE

## Disclaimer

> **Warning**
> It is recommended that you have access to GPT-4 via the OpenAI API. GPT-3.5 will probably fail to make correct knowledge graphs from your data.
> Since we still don't have access to GPT-4 OpenAI API, although we made our account a month ago and generated >1$ in billing a week ago,
> the `init_repo`, `update_file` and `add_file` endpoints are still untested. We initialized knowledge graphs manually, through ChatGPT.
> **Here be dragons.**

## Development

If you made changes to the code, do:
1. ```docker build -t patrikkukic/bor:latest .```
2. ```docker push patrikkukic/bor:latest```

## Installation

### If you want to run BOR via Docker:

1. 
    Set the ```OPENAI_API_KEY``` environment variable to your OpenAI API key.
    Optionally, set the environment variable ```MOCK=True``` if you want to use mock repos included in the project (for testing purposes).

2.  ```docker compose up```
3. If you want to populate Memgraph with previously prepared mock Obsidian Vaults inside `core/knowledgebase/mock_repos`:

    1. Change every every `file_path` and `repo_path` value inside `core/knowledgebase/mock_cypherls` to match the one you want on your system (currently it's set to `/home/patrik/something`, which obviously isn't correct in your case)

    2. Do:
    ```
    cd core
    python init_vault_mock_data.py
    ```

### If you want to run BOR locally, check out: [docs_local_install.md](https://github.com/memgraph/bor/blob/main/docs_local_install.md)
