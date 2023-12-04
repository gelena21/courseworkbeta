from pathlib import Path

ROOT_PATH = Path(__file__).parent
DATA_PATH = ROOT_PATH.joinpath(ROOT_PATH, 'data')
OPERATIONS_PATH = DATA_PATH.joinpath(DATA_PATH, "operations.xls")

OPERATIONS_PATH_2 = Path(__file__).parent.joinpath("config.json")
