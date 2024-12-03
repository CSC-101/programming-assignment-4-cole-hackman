import data
import county_demographics
import build_data
import sys

# The following 5 sets of functions are copied from programming assignment 3:

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
        if county.education[education] > education_threshold:
            filtered_counties.append(county)
    return filtered_counties

def education_less_than(target_counties: list[county_demographics], education: str, education_threshold: float) -> list[county_demographics]:
    filtered_counties= []
    for county in target_counties:
        if county.education[education] < education_threshold:
            filtered_counties.append(county)
    return filtered_counties

def ethnicity_greater_than(target_counties: list[county_demographics], ethnicity: str, ethnicity_threshold: float) -> list[county_demographics]:
    filtered_counties= []
    for county in target_counties:
        if county.ethnicities[ethnicity] > ethnicity_threshold:
            filtered_counties.append(county)
    return filtered_counties

def ethnicity_less_than(target_counties: list[county_demographics], ethnicity: str, ethnicity_threshold: float) -> list[county_demographics]:
    filtered_counties= []
    for county in target_counties:
        if county.ethnicities[ethnicity] < ethnicity_threshold:
            filtered_counties.append(county)
    return filtered_counties

def below_poverty_level_greater_than(target_counties: list[county_demographics], poverty_threshold: float) -> list[county_demographics]:
    filtered_counties= []
    for county in target_counties:
        if county.income['Persons Below Poverty Level'] > poverty_threshold:
            filtered_counties.append(county)
    return filtered_counties

def below_poverty_level_less_than(target_counties: list[county_demographics], poverty_threshold: float) -> list[county_demographics]:
    filtered_counties= []
    for county in target_counties:
        if county.income['Persons Below Poverty Level'] < poverty_threshold:
            filtered_counties.append(county)
    return filtered_counties


full_data = build_data.get_data()

# Function to get the file name from command-line arguments.
# Parameters:
#None
# Returns: The name of the file provided as a command-line argument (data type str).
def get_file_name() -> str:
    if len(sys.argv) != 2:
        print("Please provide one file name")
        sys.exit()
    filename = sys.argv[1]

    try:
        with open(filename, 'r'):
            pass
    except IOError:
        print("Please provide a valid file name")
        sys.exit()

    print(f"{len(full_data)} counties loaded")
    return filename

# Function to count the number of colons in a given input string
# Parameters:
# input_line: The string which colons are to be counted
# Returns: The count of colons in the string
def count_colons(input_line: str) -> int:
    count = 0
    for char in input_line:
        if char == ":":
            count += 1
    return count

# Function to read and validate lines from an operations file
# Parameters:
#filename: The name of the file to read operations from
# Returns: A list of valid operation lines
def read_file_lines(filename: str) -> list:
    valid_ops = ["display","filter-state","filter-gt","filter-lt","population-total","population","percent"]
    ops_colon_nums = {"display": 0,"filter-state": 1,"filter-gt": 2,"filter-lt": 2,"population-total": 0,"population": 1,"percent": 1}
    line_num = 1
    valid_lines = []

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()

            if not line:
                line_num += 1
                continue
            line_split = line.split(":")
            line_operation = line_split[0]
            if line_operation in valid_ops:
                if len(line_split) - 1 == ops_colon_nums[line_operation]:
                    valid_lines.append(line)
                else:
                    print(f"There is an error on line {line_num}, {count_colons(line)} is an incorrect number of colons for {line_operation}")
                    continue
            else:
                print(f"There is an error on line {line_num}: {line_operation} is an invalid operation")

            line_num += 1

    return valid_lines

# Function to display information for a list of counties.
# Parameters:
# list_counties: A list of county_demographics objects to display
# Returns: None
def display(list_counties: list[county_demographics]):
    for county in list_counties:
        print(f"County: {county.county}, State: {county.state}")
        print(f"    Education: {county.education}")
        print(f"    Ethnicities: {county.ethnicities}")
        print(f"    Income: {county.income}")
        print(f"    Population: {county.population}")
        print()

# Function to execute a series of operations based on a list of valid lines.
# Parameters:
# valid_lines: A list of validated operations to process
# Returns: A filtered dataset after applying all operations
def execute_operations(valid_lines):
    filtered_data = full_data

    for line in valid_lines:
        lines_split = line.split(":")
        operation = lines_split[0]
        try:
            if operation == "filter-state":
                state = lines_split[1]
                filtered_data = filter_by_state(filtered_data, state)
                print(f"Filter: state == {state} ({len(filtered_data)} entries)")
            elif operation == "filter-gt":
                field = lines_split[1]
                value = float(lines_split[2])
                field_parts = field.split(".")
                field_label = field_parts[1] if len(field_parts) > 1 else field_parts[0]

                if field_parts[0]== "Education":
                   filtered_data = education_greater_than(filtered_data, field_label, value)
                elif field_parts[0] == "Ethnicities":
                    filtered_data = ethnicity_greater_than(filtered_data, field_label, value)
                elif field_parts[0] == "Income":
                    if field_label == "Persons Below Poverty Level":
                        filtered_data = below_poverty_level_greater_than(filtered_data, value)
                print(f"Filter: {field} gt {value} ({len(filtered_data)} entries)")
            elif operation == "filter-lt":
                field = lines_split[1]
                value = float(lines_split[2])
                field_parts = field.split(".")
                field_label = field_parts[1] if len(field_parts) > 1 else field_parts[0]

                if field_parts[0] == "Education":
                    filtered_data = education_less_than(filtered_data, field_label, value)
                elif field_parts[0] == "Ethnicities":
                    filtered_data = ethnicity_less_than(filtered_data, field_label, value)
                elif field_parts[0] == "Income":
                    if field_label == "Persons Below Poverty Level":
                        filtered_data = below_poverty_level_less_than(filtered_data, value)
                print(f"Filter: {field} gt {value} ({len(filtered_data)} entries)")
            elif operation == "population":
                  field = lines_split[1]
                  field_parts = field.split(".")
                  if len(field_parts) > 1:
                      category = field_parts[0]
                      field_label = field_parts[1]
                  else:
                      category = field_parts[0]
                      field_label = field_parts[0]
                  if category == "Education":
                      sub_population = population_by_education(filtered_data, field_label)
                  elif category == "Ethnicities":
                      sub_population = population_by_ethnicity(filtered_data, field_label)
                  elif category == "Income" and field_label == "Persons Below Poverty Level":
                          sub_population = population_below_poverty_level(filtered_data)
                  else:
                      sub_population = 0
                  print(f"2014 {field} population: {sub_population}")
            elif operation == "population-total":
                total_population = population_total(filtered_data)
                print(f"2014 population: {total_population}")
            elif operation == "percent":
                field = lines_split[1]
                field_parts = field.split(".")
                field_label = field_parts[1] if len(field_parts) > 1 else field_parts[0]
                if "Education" in field:
                    percentage = percent_by_education(filtered_data, field_label)
                elif "Ethnicities" in field:
                    percentage = percent_by_ethnicity(filtered_data, field_label)
                elif "Income" in field and field_label == "Persons Below Poverty Level":
                    percentage = percent_below_poverty_line(filtered_data)
                else:
                    percentage = 0.0
                print(f"2014 {field} percentage: {percentage}")
            elif operation == "display":
                display(filtered_data)
            else:
                print(f"The operation you provided ({operation}) is not supported")

        except Exception as e:
            print(f"There was an error when processing the {line} line. Here are the details: {e}")

    return filtered_data

def main():
    filename = get_file_name()
    valid_lines = read_file_lines(filename)
    execute_operations(valid_lines)

main()