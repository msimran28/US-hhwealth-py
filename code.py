import csv
from pprint import pprint
import statistics
import matplotlib.pyplot as plt

head = ['weight', 'year', 'age', 'sex', 'education', 'race', 'asset_total', 'asset_housing', 'debt_total', 'debt_housing', 'income']
data = []

# Read the data file
with open("RA_21_22_noheads.csv") as fp:
    reader = csv.reader(fp, delimiter=",", quotechar='"')
    for row in reader:
        diction = {}
        for i in range(len(row)):
            diction[head[i]] = row[i]
        
        data.append(diction)
    
# Convert relevant numbers to appropriate format from strings.
for diction in data:
    diction['asset_total'] = float(diction['asset_total'])
    diction['asset_housing'] = float(diction['asset_housing'])
    diction['debt_total'] = float(diction['debt_total'])
    diction['debt_housing'] = float(diction['debt_housing'])
    diction['income'] = float(diction['income'])
    diction['age'] = float(diction['age'])
    diction['weight'] = float(diction['weight'])

# Precompute the race and education data to store them in an easy to use format.
race = {'Hispanic': {}, 'black': {}, 'white': {}, 'other': {}}
for diction in data:
    year = diction['year']
    race_t = diction['race']
    wealth = diction['asset_total'] - diction['debt_total']
    if year not in race[race_t]:
        race[race_t][year] = []
    race[race_t][year].append(wealth)


education = {'college degree':{}, 'no college':{}, 'some college':{}}
for diction in data:
    edu_t = diction['education']
    year = diction['year']
    wealth = diction['asset_total'] - diction['debt_total']
    if year not in education[edu_t]:
        education[edu_t][year] = []
    education[edu_t][year].append(wealth)

# Q1
# Calculate the median wealth in race_median and edu_median
race_median = {'Hispanic': [[], []], 'black': [[], []], 'white': [[], []], 'other': [[], []]}
for race_t, race_data in race.items():
    for year, wealth_list in race_data.items():
        median = statistics.median(wealth_list)
        race_median[race_t][0].append(year)
        race_median[race_t][1].append(median)

edu_median = {'college degree':[[], []], 'no college':[[], []], 'some college':[[], []]}
for edu_t, edu_data in education.items():
    for year, wealth_list in edu_data.items():
        median = statistics.median(wealth_list)
        edu_median[edu_t][0].append(year)
        edu_median[edu_t][1].append(median)

# Plot graphs
years = race_median['Hispanic'][0]
plt.figure()
plt.plot(race_median['Hispanic'][1], c = 'royalblue', ls = '-', marker = '*')
plt.plot(race_median['black'][1], c = 'indianred', ls = '-', marker = '*')
plt.plot(race_median['white'][1], c = 'sandybrown', ls = '-', marker = '*')
plt.plot(race_median['other'][1], c = 'darkseagreen', ls = '-', marker = '*')
plt.legend(('Hispanic','Black', 'White', 'Other'))
plt.xticks(range(len(years)), years)
plt.ylabel("Median wealth")
plt.xlabel("Years")
plt.title("Median wealth across races")
plt.savefig('Q1_race.png')

plt.figure()
plt.plot(edu_median['college degree'][1], c = 'lightseagreen', ls = '-', marker = '.')
plt.plot(edu_median['no college'][1], c = 'mediumvioletred', ls = '-', marker = '.')
plt.plot(edu_median['some college'][1], c = 'darkorchid', ls = '-', marker = '.')
plt.legend(('College degree', 'No college', 'Some college'))
plt.xticks(range(len(years)), years)
plt.ylabel("Median wealth")
plt.xlabel("Years")
plt.title("Median wealth across education levels")
plt.savefig('Q1_edu.png')

# Q2
# Calculate the median housing wealth in race_housing_median
race_housing = {'Hispanic': {}, 'black': {}, 'white': {}, 'other': {}}
for diction in data:
    year = diction['year']
    race_t = diction['race']
    housing_wealth = diction['asset_housing'] - diction['debt_housing']
    if year not in race_housing[race_t]:
        race_housing[race_t][year] = []
    race_housing[race_t][year].append(housing_wealth)

race_housing_median = {'Hispanic': [[], []], 'black': [[], []], 'white': [[], []], 'other': [[], []]}
for race_t, race_data in race_housing.items():
    for year, housing_wealth_list in race_data.items():
        median = statistics.median(housing_wealth_list)
        race_housing_median[race_t][0].append(year)
        race_housing_median[race_t][1].append(median)

# Plot graph 
years = race_housing_median['black'][0]
plt.figure()
plt.plot(race_housing_median['black'][1], c = 'lightslategrey', ls = '-', marker = '*')
plt.plot(race_housing_median['white'][1], c = 'cornflowerblue', ls = '--', marker = '.')
plt.legend(('Black', 'White'))
plt.xticks(range(len(years)), years)
plt.ylabel("Median housing wealth")
plt.xlabel("Years")
plt.title("Median housing wealth across blacks and whites")
plt.savefig('Q2.png')

# Q3
# Calculate the median housing and non-housing wealth only for homeowners in the age group 25 or above in race_filter_median
race_filter = {'Hispanic': {}, 'black': {}, 'white': {}, 'other': {}}
for diction in data:
    year = diction['year']
    race_t = diction['race']
    age = diction['age']
    housing_wealth = diction['asset_housing'] - diction['debt_housing']
    nonhousing_wealth = diction['asset_total'] - diction['debt_total'] - housing_wealth
    housing_wealth_criteria = diction['asset_housing'] + diction['debt_housing']
    if age >= 25 and housing_wealth_criteria > 0: 
        if year not in race_filter[race_t]:
            race_filter[race_t][year] = [[],[]]
        race_filter[race_t][year][0].append(housing_wealth)
        race_filter[race_t][year][1].append(nonhousing_wealth)

race_filter_median = {'Hispanic': [[], [], []], 'black': [[], [], []], 'white': [[], [], []], 'other': [[], [], []]}
for race_t, race_data in race_filter.items():
    for year, year_data in race_data.items():
        housing_wealth, nonhousing_wealth = year_data[0], year_data[1]
        median_housing = statistics.median(housing_wealth)
        median_nonhousing = statistics.median(nonhousing_wealth)
        race_filter_median[race_t][0].append(year)
        race_filter_median[race_t][1].append(median_housing)
        race_filter_median[race_t][2].append(median_nonhousing)

# Plot graph 
years = race_filter_median['black'][0]
plt.figure()
plt.plot(race_filter_median['black'][1], c = 'lightslategrey', ls = '-', marker = '*')
plt.plot(race_filter_median['white'][1], c = 'cornflowerblue', ls = '--', marker = '.')
plt.legend(('Black', 'White'))
plt.xticks(range(len(years)), years)
plt.ylabel("Median housing wealth")
plt.xlabel("Years")
plt.title("Median housing wealth across blacks and whites")
plt.savefig('Q3_median_housing.png')

years = race_filter_median['black'][0]
plt.figure()
plt.plot(race_filter_median['black'][2], c = 'lightslategrey', ls = '-', marker = '*')
plt.plot(race_filter_median['white'][2], c = 'cornflowerblue', ls = '--', marker = '.')
plt.legend(('Black', 'White'))
plt.xticks(range(len(years)), years)
plt.ylabel("Median non-housing wealth")
plt.xlabel("Years")
plt.title("Median non-housing wealth across blacks and whites")
plt.savefig('Q3_median_nonhousing.png')

