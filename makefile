export PYTHONPATH := ${PYTHONPATH}:/Users/yash/Desktop/work/fam-llm/src

# Recipe to run frontend
run_frontend:
	chainlit run src/frontend.py


# Recipe to generate embeddings
embeddings_generate:
	python src/vector_storage/chroma.py
