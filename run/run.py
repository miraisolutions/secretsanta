import os
from secretsanta.main.funs import make_santa_dict

participants = {
    'Stéphanie': 'stephanie',
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

for name in participants.keys() :
    participants[name] += '@acme-example.com'

# remove previously created file
file_to_rm = os.listdir("./log_file")
file_rm = "./log_file/" + str(file_to_rm[0])
os.remove(file_rm)

# set logging level as environment variable
os.environ["level"] = "DEBUG"
log_level = os.environ.get('log_level', os.getenv("level")).upper()
print(make_santa_dict(participants, seed = None, verbose = True, level = log_level))

