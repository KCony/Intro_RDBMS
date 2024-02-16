import csv

STATES_INPUT = 'state_abbr.csv'
CSV_INPUT = 'Export.csv'
MARKETS_OUTPUT = 'markets.csv'
CITIES_OUTPUT = 'cities.csv'
STATES_OUTPUT = 'states.csv'
CATGEORIES_OUTPUT = 'categories.csv'
MARKETS_CATGEORIES_OUTPUT = 'markets_categories.csv'


def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


state_abbreviations = {}
with open(STATES_INPUT, 'r') as file:
    csv_reader = csv.DictReader(file)
    states_data = [row for row in csv_reader]
for state in states_data:
    state_abbreviations[state['State']] = state['Abbreviation']
# print(state_abbreviations)

with open(CSV_INPUT, 'r') as file:
    csv_reader = csv.DictReader(file)
    market_list = [row for row in csv_reader]

category_names_list = list(market_list[0].keys())[28:-1]
categories_dict = {category_names_list[idx]: {'category_id': idx, 'category':
                   category_names_list[idx]} for idx in range(len(category_names_list))}
print(categories_dict)
states_dict = {}
ctr_states = 0
cities_dict = {}
ctr_cities = 0
markets_dict = {}
ctr_markets = 0
ctr_markets_categories = 0
markets_categories_list = []
for market in market_list:
    market['State'] = market['State'].strip()
    market['city'] = market['city'].strip()
    if market['State'] != '' and market['State'] not in states_dict:
        states_dict[market['State']] = {'state_id': ctr_states, 'state_full': market['State'],
                                        'state_abbr': state_abbreviations[market['State']]}
        ctr_states += 1
    if market['city'].strip() != '' and market['State'].strip() != '' and market['city'] not in cities_dict:
        cities_dict[market['city']] = {'city_id': ctr_cities, 'city': market['city'],
                                       'state_id': states_dict[market['State']]['state_id']}
        ctr_cities += 1
    market['FMID'] = market['FMID'].strip()
    if market['FMID'] != '' and market['city'] != '' and market['State'] != '':
        market['FMID'] = int(market['FMID'])
        markets_dict[market['FMID']] = {'market_id': market['FMID'],
                                        'market_name': market['MarketName'].strip(),
                                        'street': market['street'].strip(),
                                        'city': cities_dict[market['city']]['city_id'],
                                        'state': states_dict[market['State']]['state_id'],
                                        'zip': int(market['zip']) if market['zip'].isnumeric() else None,
                                        'lat': float(market['y']) if isfloat(market['y']) else None,
                                        'lon': float(market['x']) if isfloat(market['x']) else None}
    for category in category_names_list:
        if market[category].lower() == 'y':
            markets_categories_list.append({'market_category_id': ctr_markets_categories, 'market_id': market['FMID'],
                                            'category_id': categories_dict[category]['category_id']})
            ctr_markets_categories += 1

# print(markets_dict[1008961])
# print(states_dict)
# print(list(market_list[0].keys())[28:-1])
# print(markets_categories_list)

states_list = list(states_dict.values())
# print(states_list)
with open(STATES_OUTPUT, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=states_list[0].keys())
    writer.writeheader()
    for row in states_list:
        writer.writerow(row)

cities_list = list(cities_dict.values())
# print(cities_list)
with open(CITIES_OUTPUT, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=cities_list[0].keys())
    writer.writeheader()
    for row in cities_list:
        writer.writerow(row)

markets_list = list(markets_dict.values())
# print(markets_list)
with open(MARKETS_OUTPUT, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=markets_list[0].keys())
    writer.writeheader()
    for row in markets_list:
        writer.writerow(row)

categories_list = list(categories_dict.values())
with open(CATGEORIES_OUTPUT, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=categories_list[0].keys())
    writer.writeheader()
    for row in categories_list:
        writer.writerow(row)


with open(MARKETS_CATGEORIES_OUTPUT, 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=markets_categories_list[0].keys())
    writer.writeheader()
    for row in markets_categories_list:
        writer.writerow(row)
