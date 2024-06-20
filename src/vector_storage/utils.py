def get_text_from_file(path: str) -> str:
    with open(path, 'r') as file:
        return file.read()
