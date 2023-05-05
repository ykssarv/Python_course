import pytest
from formula_one import FormulaOne, Race, Driver

filename = 'example.txt'

def test_write_championship_to_file():
    d = FormulaOne(filename)
    d.write_championship_to_file()
    file = open('championship_results.txt', 'r')
    file2 = file.readlines()
    assert file2[0] == "PLACE     NAME                     TEAM                     POINTS\n"
    assert file2[1] == "------------------------------------------------------------------\n"
    assert file2[2] == "1         Jenson Button            Williams-BMW             50    \n"
    assert file2[3] == "2         Heinz-Harald Frentzen    Jordan-Mugen-Honda       45    \n"

def test_write_race_results_to_file():
    d = FormulaOne(filename)
    d.write_race_results_to_file(2)
    file = open('results_for_race_2.txt', 'r')
    file2 = file.readlines()
    assert file2[0] == "PLACE     NAME                     TEAM                     TIME           DIFF           POINTS\n"
    assert file2[1] == "------------------------------------------------------------------------------------------------\n"
    assert file2[2] == "1         David Coulthard          Mclaren-Mercedes         1:17.522                      25    \n"
    assert file2[3] == "2         Pedro de la Rosa         Arrows-Supertec          1:19.061       +0:01.539      18    \n"

def test_write_race_results_to_csv():
    d = FormulaOne(filename)
    d.write_race_results_to_csv(2)
    file = open('race_2_results.csv', 'r')
    file2 = file.readlines()
    assert file2[0] == "Place,Name,Team,Time,Diff,Points,Race\n"
    assert file2[1] == "1,David Coulthard,Mclaren-Mercedes,1:17.522,,25,2\n"
    assert file2[2] == "2,Pedro de la Rosa,Arrows-Supertec,1:19.061,+0:01.539,18,2\n"