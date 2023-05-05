"""Formula One."""
import re


class Driver:
    """Driver class."""

    def __init__(self, name: str, team: str):
        """
        Driver constructor.

        Here you should save driver's results as dictionary,
        where key is race number and value is points from that race.
        You must also save driver's points into a variable "points".

           :param name: Driver name
        :param team: Driver team
        """
        self.name = name
        self.team = team
        self.results = {}
        self.points = 0

    def get_results(self) -> dict:
        """
        Get all driver's results.

        :return: Results as dictionary
        """
        return self.results

    def get_points(self):
        """
        Return calculated driver points.

        :return: Calculated points
        """
        self.set_points()
        return self.points

    def set_points(self):
        """Set points for driver."""
        results = 0
        for points in self.results.values():
            results += points
        self.points = results

    def add_result(self, race_number: int, points: int):
        """
        Add new result to dictionary of results.

        Dictionary is located in the constructor.

        :param race_number: Race number
        :param points: Number of points from the race
        """
        self.results[race_number] = points


class Race:
    """Race class."""

    def __init__(self, file):
        """
        Race constructor.

        Here you should keep data collected from file.
        You must read file rows to list.

        :param file: File with race data
        """
        self.file = file
        self.file_lines = self.read_file_to_list()
        self.race_amount = self.read_race_amount()

    def read_file_to_list(self):
        """
        Read file data to list in constructor.

        First line shows number of races in data file.
        Rest of the data follows same rules. Each line consists of 'Driver Team Time Race'.
        There are 2 or more spaces between each 'category'.
        E.g. "Mika Häkkinen  McLaren-Mercedes      42069   3"

        If file does NOT exist, throw FileNotFoundError with message "No file found!".
        """
        try:
            file = open(self.file, "r")
            return file.readlines()[1:]
        except FileNotFoundError:
            raise FileNotFoundError("No file found!")

    def read_race_amount(self):
        """A."""
        try:
            file = open(self.file, "r")
            return int(file.readlines()[0])
        except FileNotFoundError:
            raise FileNotFoundError("No file found!")

    @staticmethod
    def extract_info(line: str) -> dict:
        """
        Helper method for read_file_to_list.

        Here you should convert one data line to dictionary.
        Dictionary must contain following key-value pairs:
            'Name': driver's name as string
            'Team': driver's team as string
            'Time': driver's time as integer (time is always in milliseconds)
            'Diff': empty string
            'Race': race number as integer

        :param line: Data string
        :return: Converted dictionary
        """
        line_list = re.split("  +", line)
        info = {'Name': line_list[0],
                'Team': line_list[1],
                'Time': int(line_list[2]),
                'Diff': "",
                'Race': int(line_list[3])
                }
        return info

    def filter_data_by_race(self, race_number: int) -> list:
        """
        Filter data by race number.

        :param race_number: Race number
        :return: Filtered race data
        """
        file = self.read_file_to_list()
        file = map(Race.extract_info, file)
        return list(filter(lambda x: x['Race'] == race_number, file))

    @staticmethod
    def format_time(time: str) -> str:
        """
        Format time from milliseconds to M:SS.SSS.

        format_tim   e('12') -> 0:00.012
        format_time('1234') -> 0:01.234
        format_time('123456') -> 2:03.456

        :   param time: Time in milliseconds
        :return: Time as M:SS.SSS string
        """
        minutes = int(time) // 1000 // 60
        seconds = (int(time) - 60 * minutes * 1000) // 1000
        milliseconds = int(time) - 1000 * seconds - (60 * minutes * 1000)
        minutes = str(minutes)
        seconds = str(seconds)
        milliseconds = str(milliseconds)
        if len(seconds) == 1:
            seconds = "0" + seconds
        if len(milliseconds) == 1:
            milliseconds = "00" + milliseconds
        if len(milliseconds) == 2:
            milliseconds = "0" + milliseconds
        time_string = minutes + ":" + seconds + "." + milliseconds
        return time_string

    @staticmethod
    def calculate_time_difference(first_time: int, second_time: int) -> str:
        """
        Calculate difference between two times.

        First time is always smaller than second time. Both times are in milliseconds.
        You have to return difference in format +M:SS.SSS

        calculate_time_difference(4201, 57411) -> +0:53.210

        :param first_time: First time in milliseconds
        :param second_time: Second time in milliseconds
        :return: Time difference as +M:SS.SSS string
        """
        difference = str(second_time - first_time)
        return "+" + Race.format_time(difference)

    @staticmethod
    def sort_data_by_time(results: list) -> list:
        """
        Sort results data list of dictionaries by 'Time'.

        :param results: List of dictionaries
        :return: Sorted list of dictionaries
        """
        return sorted(results, key=lambda x: x['Time'])

    def get_results_by_race(self, race_number: int) -> list:
        """
        Final results by race number.

        This method combines the rest of the methods.
        You have to filter data by race number and sort them by time.
        You must also fill 'Diff' as time difference with first position.
        You must add 'Place' and 'Points' key-value pairs for each dictionary.

        :param race_number: Race number for filtering
        :return: Final dictionary with complete data
        """
        save = self.filter_data_by_race(race_number)
        save2 = self.sort_data_by_time(save)
        first_time = save2[0]['Time']
        points = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1] + [0] * 1000000
        for i, dictionary in enumerate(save2):
            dictionary['Diff'] = self.calculate_time_difference(first_time, dictionary['Time'])
            dictionary['Place'] = i + 1
            dictionary['Points'] = points[i]
            dictionary['Time'] = Race.format_time(dictionary['Time'])
        save2[0]['Diff'] = ''
        return save2


class FormulaOne:
    """FormulaOne class."""

    def __init__(self, file):
        """
        FormulaOne constructor.

        It is reasonable to create Race instance here to collect all data from file.

        :param file: File with race data
        """
        self.file = file
        self.race = Race(self.file)

    def write_race_results_to_file(self, race_number: int):
        """
        Write one race results to a file.

        File name is 'results_for_race_{race_number}.txt'.
        Exact specifications are described in the text.

        :param race_number: Race to write to file
        """
        results = open(f'results_for_race_{race_number}.txt', 'w')
        results.write(f"{'PLACE':10}{'NAME':25}{'TEAM':25}{'TIME':15}{'DIFF':15}{'POINTS':6}\n")
        results.write('-' * 96 + '\n')
        results2 = self.race.get_results_by_race(race_number)
        for d in results2:
            results.write(f"{str(d['Place']):10}{d['Name']:25}{d['Team']:25}{d['Time']:15}{d['Diff']:15}{str(d['Points']):6}\n")

    def write_race_results_to_csv(self, race_number: int):
        """
        Write one race results to a csv file.

        File name is 'race_{race_number}_results.csv'.
        Exact specifications are described in the text.

        :param race_number: Race to write to file
        """
        results = open(f'race_{race_number}_results.csv', 'w')
        results.write("Place,Name,Team,Time,Diff,Points,Race\n")
        results2 = self.race.get_results_by_race(race_number)
        for d in results2:
            p = str(d['Place'])
            n = d['Name']
            t = d['Team']
            ti = d['Time']
            di = d['Diff']
            po = str(d['Points'])
            rn = str(race_number)
            results.write(f"{p},{n},{t},{ti},{di},{po},{rn}\n")

    def write_championship_to_file(self):
        """
        Write championship results to file.

        It is reasonable to create Driver class instance for each unique driver name and collect their points
        using methods from Driver class.
        Exact specifications are described in the text.
        """
        drivers = {}
        for i in range(self.race.race_amount):
            results = self.race.get_results_by_race(i + 1)
            for result in results:
                if result['Name'] not in drivers.keys():
                    drivers[result['Name']] = Driver(result['Name'], result['Team'])
                drivers[result['Name']].add_result(i + 1, result['Points'])

        drivers = list(sorted(drivers.values(), key=lambda driver: 1 / driver.get_points()))
        results = open('championship_results.txt', 'w')
        results.write(f"{'PLACE':10}{'NAME':25}{'TEAM':25}{'POINTS':6}\n")
        results.write('-' * 66 + '\n')
        for i, d in enumerate(drivers):
            results.write(
                f"{str(i + 1):10}{d.name:25}{d.team:25}{str(d.get_points()):6}\n")
