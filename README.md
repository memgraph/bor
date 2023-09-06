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

## Installation

You can install and setup BOR and Memgraph using Docker or by running it manually.

### Docker installation

Before you start, make sure you have a running [Docker](https://www.docker.com/) instance and [Docker compose](https://docs.docker.com/compose/install/) installed.

1. Download BOR
    - Clone the repository in your folder of choice:

    ```
    git clone https://github.com/memgraph/bor.git
    ```
    
    - Navigate to the BOR root directory:
    ```
    cd bor
    ```

2. 
    You will need to set the ```OPENAI_API_KEY``` environment variable in a `.env` file in the BOR root directory to your OpenAI API key. It should look like this:

    ```
    OPENAI_API_KEY=YOUR_API_KEY
    ```

    Where YOUR_API_KEY is a key you can get [here](https://openai.com/).

3.  
    - Open your terminal or command prompt.
    - Run:
        ```docker compose up```

The installation process can take up to ten minutes. After successful installation, you can proceed to set up your frontend - [ODIN](https://github.com/memgraph/odin) or [RUNE](https://github.com/memgraph/rune).

### Manual installation

For the manual installation make sure you have [conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html) and [Python](https://www.python.org/) installed on your system.

1. Download BOR
    - Clone the repository in your folder of choice:

    ```
    git clone https://github.com/memgraph/bor.git
    ```
    
    - Navigate to the BOR root directory:
    ```
    cd bor
    ```

2. Create a new conda virtual environment using Python 3.9.16:
    ```
    conda create --name bor_env python=3.9.16
    ```

3. Activate the environment:
    ```
    source activate bor_env
    ```

4. To install all dependencies and setup all packages, run:

    ```
    pip install -e .
    ```

    This process might take a few minutes.

5. You will need a `.env` file with your OpenAI API key. It should look like this:

    ```
    OPENAI_API_KEY=YOUR_API_KEY
    MEMGRAPH_HOST="127.0.0.1"
    MEMGRAPH_PORT=7687
    CHROMA_DATA_DIR="/path/to/dir/chroma"
    CHROMA_VECTOR_SPACE="cosine"
    EMBEDDING_MODEL_NAME="text-embedding-ada-002"
    LLM_MODEL_NAME="gpt-3.5-turbo-0613"
    LLM_MODEL_TEMPERATURE=0.2
    ```

    Where YOUR_API_KEY is your API key you can get [here](https://openai.com/). You can replace "/path/to/dir/chroma" with preferred path to an empty folder where BOR will store all embedding search data.

6. If you don't have [Memgraph](https://memgraph.com/docs/memgraph/installation) installed, you can run:
    - `bash core/run_memgraph_290.sh`

7. Start the FastAPI backend by running: 
    - `bash core/run_server.sh`

    Alternatively, you can just run the script directly in your conda environment:
    - `uvicorn core.restapi.api:app --reload`

After successful initialization, you can proceed to set up your frontend - [ODIN](https://github.com/memgraph/odin) or [RUNE](https://github.com/memgraph/rune).

## Documentation

When BOR is running, you can access the endpoint documentation at http://localhost:8000/docs#/
