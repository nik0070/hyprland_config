from pathlib import Path

def get_path(base_path: str) -> Path:
    """ Returns the project file path """

    project_root = Path(__file__).resolve().parent.parent
    return project_root / base_path

def normalize(name:str) -> str:
    return name.lower().replace(" ", "")

def get_file_stem(get_file_names_from_path: str) -> str:
    data_path = get_path(get_file_names_from_path)  #project root / src/data/dynamic
    names = []
    # Traverse all subfolders recursively
    for file_path in data_path.rglob("*"):
        if file_path.is_file() and file_path.suffix.lower() in [".csv", ".json"]:
            name = file_path.stem  # filename without extension
            names.append(name)
    return names


if __name__ == "__main__":
    print(get_file_stem('src/data/dynamic'))
