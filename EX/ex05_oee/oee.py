"""EX05 - OEE."""
import csv


def read_production_data(filename: str) -> dict:
    """
    Open the file in the provided path, read in values and return them as a dictionary,.

    where the key is the machine name and value is a list of integers for the production data for each shift.

    {
    'Machine Name': [Run Time (minutes), Ideal Run Rate (pcs/min), Total Count (pcs), Good Count (pcs)]
    }

    :param filename: string file path for the CSV file to be read
    :return: dictionary with the production data per machine
    """
    try:
        production_data = {}
        with open(filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                production_data[row[0]] = list(map(int, row[1:]))
    except FileNotFoundError:
        return {}
    return production_data


def calculate_quality(production_data: dict) -> dict:
    """
    Go through the input dictionary and for each machine, calculate the Quality percentage (as a float, e.g. 98.1).

    Save each value in a new dictionary, where the key is the machine name and value is the calculated Quality.
    Return the newly created dictionary.

    :param production_data: dictionary with production data
    :return: dictionary with OEE Quality value per machine
    """
    machine_quality = {}
    for keys, values in production_data.items():
        if float(values[2]) == 0:
            quality = 0.0
        else:
            quality = round(float(values[3]) / float(values[2]) * 100, 1)
        machine_quality[keys] = quality
    return machine_quality


def calculate_availability(production_data: dict) -> dict:
    """
    Go through the input dictionary and for each machine, calculate the Availability percentage (as a float, e.g. 98.1).

    Save each value in a new dictionary, where the key is the machine name and value is the calculated Availability.
    Return the newly created dictionary.

    :param production_data: dictionary with production data
    :return: dictionary with OEE Availability value per machine
    """
    machine_availability = {}
    for keys, values in production_data.items():
        availability = round((float(values[0]) / 420 * 100), 1)
        machine_availability[keys] = availability
    return machine_availability


def calculate_performance(production_data: dict) -> dict:
    """
    Go through the input dictionary and for each machine, calculate the Performance percentage (as a float, e.g. 98.1).

    Save each value in a new dictionary, where the key is the machine name and value is the calculated Performance.
    Return the newly created dictionary.

    :param production_data: dictionary with production data
    :return: dictionary with OEE Performance value per machine
    """
    machine_performance = {}
    for keys, values in production_data.items():
        if float(values[0]) == 0 or float(values[1]) == 0:
            performance = 0.0
        else:
            performance = round(((float(values[2]) / float(values[0])) / float(values[1]) * 100), 1)
        machine_performance[keys] = performance
    return machine_performance


def calculate_oee(production_data: dict) -> dict:
    """
    Using the previously defined functions, calculate the final OEE percentage for each machine.

    Save each value in a new dictionary, where the key is the machine name and value is the calculated Performance.
    Return the newly created dictionary.

    :return: dictionary with OEE percentage value per machine
    """
    machine_quality = calculate_quality(production_data)
    machine_performance = calculate_performance(production_data)
    machine_availability = calculate_availability(production_data)
    machine_oee = {}
    for line in production_data.keys():
        oee = round(((machine_quality[line] * machine_availability[line] * machine_performance[line]) / 10000), 1)
        machine_oee[line] = oee
    return machine_oee


def write_results_to_file(production_data: dict, filename: str):
    """
    Write the calculation results to a CSV formatted file.

    :param filename: string file path for the CSV file to be written to
    :param production_data: dictionary with production data
    """
    performance = calculate_performance(production_data)
    quality = calculate_quality(production_data)
    availability = calculate_availability(production_data)
    oee = calculate_oee(production_data)
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Liin", "Saadavus", "Tootlus", "Kvaliteet", "OEE"])
        for line in production_data.keys():
            writer.writerow([line, availability[line], performance[line], quality[line], oee[line]])


if __name__ == '__main__':
    prod_data = read_production_data("reedene_vahetus.csv")
    print('\n- Production data -')
    print('[Run Time (minutes), Ideal Run Rate (pcs/min), Total Count (pcs), Good Count (pcs)]')
    for key, value in prod_data.items():
        print(f"{key}: {value}")

    # Sildistaja: [358, 57, 18602, 18388]
    # Hapukurgipurgitaja: [415, 12, 4800, 2013]
    # Autoklaav: [450, 10, 4500, 4500]
    # Supivillija: [402, 36, 14230, 14214]
    # Makaronikeetja: [410, 25, 10230, 10230]
    # Kartulikoorija: [420, 111, 46620, 44123]
    # Mahlapress: [0, 0, 0, 0]

    quality_dict = calculate_quality(prod_data)
    print('\n- Quality calculation results -')
    for key, value in quality_dict.items():
        print(f"{key}: {value}")

    # Sildistaja: 98.8
    # Hapukurgipurgitaja: 41.9
    # Autoklaav: 100.0
    # Supivillija: 99.9
    # Makaronikeetja: 100.0
    # Kartulikoorija: 94.6
    # Mahlapress: 0.0

    availability_dict = calculate_availability(prod_data)
    print('\n- Availability calculation results -')
    for key, value in availability_dict.items():
        print(f"{key}: {value}")

    # Sildistaja: 85.2
    # Hapukurgipurgitaja: 98.8
    # Autoklaav: 107.1
    # Supivillija: 95.7
    # Makaronikeetja: 97.6
    # Kartulikoorija: 100.0
    # Mahlapress: 0.0

    performance_dict = calculate_performance(prod_data)
    print('\n- Performance calculation results -')
    for key, value in performance_dict.items():
        print(f"{key}: {value}")

    # Sildistaja: 91.2
    # Hapukurgipurgitaja: 96.4
    # Autoklaav: 100.0
    # Supivillija: 98.3
    # Makaronikeetja: 99.8
    # Kartulikoorija: 100.0
    # Mahlapress: 0.0

    oee_dict = calculate_oee(prod_data)
    print('\n- Total OEE calculation results -')
    for key, value in oee_dict.items():
        print(f"{key}: {value}")

    # Sildistaja: 76.8
    # Hapukurgipurgitaja: 39.9
    # Autoklaav: 107.1
    # Supivillija: 94.0
    # Makaronikeetja: 97.4
    # Kartulikoorija: 94.6
    # Mahlapress: 0.0

    write_results_to_file(prod_data, 'reedene_oee.csv')

    # contents of 'reedene_oee.csv':
    # Liin, Saadavus, Tootlus, Kvaliteet, OEE
    # Sildistaja, 85.2, 91.2, 98.8, 76.8
    # Hapukurgipurgitaja, 98.8, 96.4, 41.9, 39.9
    # Autoklaav, 107.1, 100.0, 100.0, 107.1
    # Supivillija, 95.7, 98.3, 99.9, 94.0
    # Makaronikeetja, 97.6, 99.8, 100.0, 97.4
    # Kartulikoorija, 100.0, 100.0, 94.6, 94.6
    # Mahlapress, 0.0, 0.0, 0.0, 0.0
