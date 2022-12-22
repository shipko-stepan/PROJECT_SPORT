import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description='File processor CLI')
    parser.add_argument('--filepath', '-f', help='Path to the file to be processed', required=True)
    parser.add_argument('--output', '-out', help='Filename for output results', required=False)

    group = parser.add_mutually_exclusive_group()  # Next arguments are mutually exclusive
    group.add_argument('--medals', '-m', nargs=2, help='Get data on the 10 medalists for a specific country in a'
                                                       ' specific year')
    group.add_argument('--total', '-t', help='Get data about countries which got at least one medal in specific year')
    group.add_argument('--overall', '-o', nargs='+', help='Get the year for specific countries when they won the'
                                                          ' most medals')
    group.add_argument('--interactive', '-i', help='Interactive mode', action='store_true')

    args = parser.parse_args()


def write_output_medals_to_file(filename: str, data: list):
    with open(filename, 'w') as f:
        for line in data:
            if 'Medals' not in line:
                f.write(f'{line["Record"]}\n')
            else:
                f.write(f'Medals: {line["Medals"]}')

def print_medals(result: list):
    for line in result:
        if 'Medals' not in line:
            print(f'{line["Record"]}')
        else:
            print(f'Medals: {line["Medals"]}')


def task1(filepath, medals, output=None):
    requested_country, requested_year = medals

    result = []

    bronze = 0
    silver = 0
    gold = 0

    all_years = set()
    all_countries = set()

    with open(filepath) as f:
        f.readline()  # skip header
        next_line = f.readline()
        count = 0
        while next_line:
            record = next_line.split('\t')
            name = record[1].strip()
            country = record[6].strip()
            year = int(record[9].strip())
            sport = record[12].strip()
            noc = record[7].strip()
            medal = record[14].strip()

            countries = {country, noc}

            all_years.add(year)
            all_countries.add(country)
            all_countries.add(noc)

            if not all([int(requested_year) == year, requested_country in countries]):
                next_line = f.readline()
                continue

            if requested_country in (country, noc):
                if medal != 'NA':
                    count += 1
                    result.append({"Record": f'{count} - {name} - {sport} - {medal}'})

                    if medal == 'Bronze':
                        bronze += 1
                    elif medal == 'Silver':
                        silver += 1
                    else:
                        gold += 1

            if count == 10:
                result.append({'Medals': f'Gold: {gold}, Silver: {silver}, Bronze: {bronze}'})
                print_medals(result)
                if output:
                    write_output_medals_to_file(output, result)
                break

            next_line = f.readline()

        if int(requested_year) not in all_years:
            print(f'In {requested_year} Olympics were not conducted')
        elif requested_country not in all_countries:
            print(f'{requested_country} didn\'t participate in Olympics')
        elif len(result) < 10:
            print('There are less than 10 medals')
