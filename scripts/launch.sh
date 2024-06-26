#!/bin/bash

export PYTHONPATH=$PYTHONPATH:/code/src

rm -rf /code/data/processed
make embeddings_generate
make run_frontend
