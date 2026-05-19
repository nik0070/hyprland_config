from pathlib import Path

def get_path(base_path: str) -> Path:
    """ Returns the project file path """

    project_root = Path(__file__).resolve().parent.parent
    return project_root / base_path

def normalize_company_name(name:str) -> str:
    return name.lower().replace(" ", "")


if __name__ == "__main__":
    print('.')
