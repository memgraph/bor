#!/bin/bash
docker run -it \
-p 7687:7687 \
-p 7444:7444 \
-p 3000:3000 \
-e MEMGRAPH="--log-level=TRACE" \
-v mg_lib:/var/lib/memgraph \
memgraph/memgraph-platform:2.9.0-memgraph2.9.0-lab2.7.1-mage1.8