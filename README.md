# Doctrin Assignment
All code is the [Main.py](Main.py) file and can be run as long as the repository of the json files is changed to the desired location. Below are explainations for all the important functions.

## func group_by_anamnesis
- Groups data by anamnesis_id
- Adds columns for end time, start time and anamnesis status (completed or not)

## func find_fever
- Counts the number of patients that had a fever temperature between two given values

## func stiff_neck
- Counts the number of patients with neck/chest pain, who also did not travel abroad

## func main
- Reads all json files and concatenates them
- Runs group_by_anamnesis
- Exports new dataset to a csv file


