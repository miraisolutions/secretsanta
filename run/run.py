import os

from pathlib import Path
from secretsanta.main.funs import make_santa_dict

participants = {
    'Stephanie': 'stephanie',
    'Simon': 'simon',
    'Gustavo': 'gustavo',
    'Nicola': 'nicola',
    'Guido': 'guido',
    'Francesca': 'francesca',
    'Gabriel': 'gabriel',
    'Roland': 'roland',
    'Nikki': 'nicoletta',
    'Peter': 'peter',
    'Martin': 'martin',
    'Riccardo': 'riccardo'
}

for name in participants.keys():
    participants[name] += '@acme-example.com'

# remove previously created file
file_to_rm = list(Path("./log_files").iterdir())
file_to_rm[0].unlink()

log_level = os.environ.get('log_level', "DEBUG").upper()
print(make_santa_dict(participants, seed=None, verbose=True, level=log_level))
