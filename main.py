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



def print_totals(result: dict):
    for k, v in result.items():
        print(f'{k} - Gold: {v["Gold"]} - Silver: {v["Silver"]} - Bronze: {v["Bronze"]}')


def write_totals_to_file(filename: str, data: dict):
    with open(filename, 'w') as f:
        for k, v in data.items():
            f.write(f'{k} - Gold: {v["Gold"]} - Silver: {v["Silver"]} - Bronze: {v["Bronze"]}\n')


def task2(filepath, total, output=None):
    requested_year = int(total.strip())

    countries = {}
    years = set()

    with open(filepath) as f:
        f.readline()  # skip header
        next_line = f.readline()
        while next_line:
            record = next_line.split('\t')
            country = record[7].strip()
            year = int(record[9].strip())
            medal = record[14].strip()

            years.add(year)

            if requested_year != year:
                next_line = f.readline()
                continue

            if medal != 'NA':
                if country not in countries:
                    bronze = 1 if medal == 'Bronze' else 0
                    silver = 1 if medal == 'Silver' else 0
                    gold = 1 if medal == 'Gold' else 0

                    countries.update(
                        {country: {'Bronze': bronze, 'Silver': silver, 'Gold': gold}}
                    )
                else:
                    countries[country][medal] += 1
            next_line = f.readline()
    if int(requested_year) not in years:
        print(f'In {requested_year} Olympics were not conducted')
    elif not countries:
        print(f'There is not champions in {requested_year}')
    print_totals(countries)
    if output:
        write_totals_to_file(output, countries)


def get_best_and_worst_year_for_country(data: dict):
    d = {k: v for k, v in sorted(data.items(), key=lambda item: item[1], reverse=True)}
    best_year = list(d.keys())[0]
    worst_year = list(d.keys())[-1]
    return f'{best_year}, {d[best_year]}', f'{worst_year}, {d[worst_year]}'


def task3(filepath: str, countries: list, output=None):

    countries_results = {}

    with open(filepath) as f:
        f.readline()  # skip header
        next_line = f.readline()
        while next_line:
            record = next_line.split('\t')
            country = record[6].strip()
            noc = record[7].strip()
            year = int(record[9].strip())
            medal = record[14].strip()

            countries_set = {country, noc}

            for c in countries:
                if c in countries_set:
                    if medal != 'NA':
                        if c not in countries_results:
                            countries_results[c] = {year: 1}
                        elif year not in countries_results[c]:
                            countries_results[c][year] = 1
                        else:
                            countries_results[c][year] += 1
            next_line = f.readline()
    for country in countries_results:
        best_year, _ = get_best_and_worst_year_for_country(countries_results[country])
        print(f'{country}: {best_year}')
    if output:
        with open(output, 'w') as f:
            for country in countries_results:
                best_year, _ = get_best_and_worst_year_for_country(countries_results[country])
                f.write(f'{country}: {best_year}\n')


def task4(filepath):
    while True:
        input_country = input('Please, enter country name or country code:\n')
        if input_country in ('x', 'X'):
            print('Bye')
            sys.exit(0)

        country_results = {}

        olympics = {}

        with open(filepath) as f:
            f.readline()  # skip header
            next_line = f.readline()
            while next_line:
                record = next_line.split('\t')
                country = record[6].strip()
                noc = record[7].strip()
                year = int(record[9].strip())
                medal = record[14].strip()
                place = record[11].strip()
                games = record[8].strip()

                countries = {country, noc}

                if input_country in countries:
                    if games not in olympics:
                        olympics[year] = [games, place]

                    if medal != 'NA':
                        if medal not in country_results:
                            country_results[medal] = 1
                        else:
                            country_results[medal] += 1

                        if year not in country_results:
                            country_results[year] = 1
                        else:
                            country_results[year] += 1
                next_line = f.readline()

        bronze_count = country_results.pop('Bronze')
        silver_count = country_results.pop('Silver')
        gold_count = country_results.pop('Gold')

        if olympics:
            average_bronze = bronze_count/len(olympics) if bronze_count else 0
            average_silver = silver_count/len(olympics) if silver_count else 0
            average_gold = gold_count/len(olympics) if gold_count else 0

        first_olympics = sorted(olympics.items())[0]
        print(f'First Oympics: {first_olympics[0]}, {first_olympics[1][1]}')

        best_olimpics, _ = get_best_and_worst_year_for_country(country_results)
        _, worst_olimpics = get_best_and_worst_year_for_country(country_results)

        print(f'The best Olympics: {best_olimpics} medals; {olympics[int(best_olimpics.split(",")[0])][1]}')
        print(f'The worst Olympics: {worst_olimpics} medals; {olympics[int(worst_olimpics.split(",")[0])][1]}')
        print(f'Avg bronze: {average_bronze}, Avg silver: {average_silver}, Avg gold: {average_gold}')


if __name__ == '__main__':
    main()
