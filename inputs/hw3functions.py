import data
import county_demographics
import build_data

# Part 1: Calculates the total population across a list of counties
# Parameters:
# target_counties (list of CountyDemographics): List of county demographics objects

# Returns:
# int: The total 2014 population for all counties in the list.
def population_total(target_counties: list[county_demographics]) -> int:
    total_pop = sum(county.population["2014 Population"] for county in target_counties)
    return total_pop


# Part 2: Filters counties by the specified state abbreviation
# Parameters:
# target_counties (list of CountyDemographics): List of county demographics objects
# state (str): Two-letter state abbreviation to filter counties by

# Returns:
# list of CountyDemographics: A list of counties that match the specified state
def filter_by_state(target_counties: list[county_demographics], state: str) -> list[county_demographics]:
    filtered_counties = []
    for county in target_counties:
        if county.state == state:
            filtered_counties.append(county)
    return filtered_counties


# Part 3: Calculates the total subpopulation for a given education level or ethnicity or the population below the poverty line
# Parameters:
# target_counties (list of CountyDemographics): List of county demographics objects
# education (str): Education key of interest (for education-related functions)
# ethnicity (str): Ethnicity key of interest (for ethnicity-related functions)

# Returns:
# float: Total sub-population for the specified key (education, ethnicity, or poverty level)
def population_by_education(target_counties: list[county_demographics], education: str) -> float:
    population_number = 0
    for county in target_counties:
        if education in county.education:
            population_number += (county.education[education] / 100 * county.population['2014 Population'])
    return population_number

def population_by_ethnicity(target_counties: list[county_demographics], ethnicity: str) -> float:
    population_number = 0
    for county in target_counties:
        if ethnicity in county.ethnicities:
            population_number += (county.ethnicities[ethnicity] / 100 * county.population['2014 Population'])
    return population_number

def population_below_poverty_level(target_counties: list[county_demographics]) -> float:
    population_number = 0
    for county in target_counties:
        population_number += (county.income["Persons Below Poverty Level"] / 100 * county.population['2014 Population'])
    return population_number


# Part 4: Calculates the percentage of the total population based on the given education level, ethnicity, or poverty level
# Parameters:
# target_counties (list of CountyDemographics): List of county demographics objects
# education (str): Education key of interest (for education-related functions).
# ethnicity (str): Ethnicity key of interest (for ethnicity-related functions)

# Returns:
# float: The specified sub-population as a percentage of the total population.
def percent_by_education(target_counties: list[county_demographics], education: str) -> float:
    total_population = population_total(target_counties)
    education_population = population_by_education(target_counties, education)
    if total_population == 0:
        return 0.0
    return education_population / total_population * 100

def percent_by_ethnicity(target_counties: list[county_demographics], ethnicity: str) -> float:
    total_population = population_total(target_counties)
    ethnicity_population = population_by_ethnicity(target_counties, ethnicity)
    if total_population == 0:
        return 0.0
    return ethnicity_population / total_population * 100

def percent_below_poverty_line(target_counties: list[county_demographics]) -> float:
    total_population = population_total(target_counties)
    poverty_population = population_below_poverty_level(target_counties)
    if total_population == 0:
        return 0.0
    return poverty_population / total_population * 100

# Part 5: Filters counties based on education or ethnicity thresholds or poverty level criteria

# Parameters:
# target_counties (list of CountyDemographics): List of county demographics objects
# education (str): Education key of interest (for education threshold functions).
# ethnicity (str): Ethnicity key of interest (for ethnicity threshold functions).
# poverty_threshold (float): Threshold value for the population below poverty level

# Returns:
# list of CountyDemographics: List of counties meeting the threshold criteria for education, ethnicity, or poverty level.
def education_greater_than(target_counties: list[county_demographics], education: str, education_threshold: float) -> list[county_demographics]:
    filtered_counties= []
    for county in target_counties:
        if county.education[education] >= education_threshold:
            filtered_counties.append(county)
    return filtered_counties

def education_less_than(target_counties: list[county_demographics], education: str, education_threshold: float) -> list[county_demographics]:
    filtered_counties= []
    for county in target_counties:
        if county.education[education] <= education_threshold:
            filtered_counties.append(county)
    return filtered_counties

def ethnicity_greater_than(target_counties: list[county_demographics], ethnicity: str, ethnicity_threshold: float) -> list[county_demographics]:
    filtered_counties= []
    for county in target_counties:
        if county.ethnicities[ethnicity] >= ethnicity_threshold:
            filtered_counties.append(county)
    return filtered_counties

def ethnicity_less_than(target_counties: list[county_demographics], ethnicity: str, ethnicity_threshold: float) -> list[county_demographics]:
    filtered_counties= []
    for county in target_counties:
        if county.ethnicities[ethnicity] <= ethnicity_threshold:
            filtered_counties.append(county)
    return filtered_counties

def below_poverty_level_greater_than(target_counties: list[county_demographics], poverty_threshold: float) -> list[county_demographics]:
    filtered_counties= []
    for county in target_counties:
        if county.income['Persons Below Poverty Level'] >= poverty_threshold:
            filtered_counties.append(county)
    return filtered_counties

def below_poverty_level_less_than(target_counties: list[county_demographics], poverty_threshold: float) -> list[county_demographics]:
    filtered_counties= []
    for county in target_counties:
        if county.income['Persons Below Poverty Level'] <= poverty_threshold:
            filtered_counties.append(county)
    return filtered_counties
