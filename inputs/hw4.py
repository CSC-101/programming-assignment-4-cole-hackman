import data
import county_demographics
import build_data
import sys
import hw3functions
from inputs.hw3functions import education_greater_than, ethnicity_greater_than, filter_by_state, ethnicity_less_than, percent_below_poverty_line, percent_by_education, percent_by_ethnicity, population_by_education, population_by_ethnicity, population_total

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
                if "Education" in field:
                   filtered_data = education_greater_than(filtered_data, field_label, value)
                elif "Ethnicities" in field:
                    filtered_data = ethnicity_greater_than(filtered_data, field_label, value)
            elif operation == "filter-lt":
                field = lines_split[1]
                value = float(lines_split[2])
                field_parts = field.split(".")
                field_label = field_parts[1] if len(field_parts) > 1 else field_parts[0]
                if "Education" in field:
                    filtered_data = education_less_than(filtered_data, field_label, value)
                elif "Ethnicities" in field:
                    filtered_data = ethnicity_less_than(filtered_data, field_label, value)
            elif operation == "population":
                  field = lines_split[1]
                  if "Education" in field:
                      sub_population = population_by_education(filtered_data, field)
                  elif "Ethnicities" in field:
                      sub_population = population_by_ethnicity(filtered_data, field)
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