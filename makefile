export PYTHONPATH := ${PYTHONPATH}:/Users/yash/Desktop/work/fam-llm/src

# Recipe to run frontend
run_frontend:
	chainlit run src/frontend.py --port 3001 --headless --host 0.0.0.0


# Recipe to generate embeddings
embeddings_generate:
	python src/vector_storage/chroma.py

build:
	docker build -t oracle . --platform=linux/amd64


