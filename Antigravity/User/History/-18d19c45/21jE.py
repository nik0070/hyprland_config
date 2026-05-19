from pathlib import Path

def get_path(base_path: str) -> Path:
    """ Returns the project file path """

    project_root = Path(__file__).resolve().parent.parent
    return project_root / base_path


if __name__ == "__main__":
    print('.')
