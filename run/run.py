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
    
print(make_santa_dict(participants, seed=None, verbose=True))

