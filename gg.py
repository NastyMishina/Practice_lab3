import os
import json


def get_programs_in_path(path):
    '''
    Данная функция принимает путь к каталогу
    и возвращает список программ в этом
    каталоге и его подкаталогах
    '''
    programs = []
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            programs.append(os.path.join(dirpath, filename))
    return programs


def get_system_path_programs():
    '''
    Данная функция возвращает
    список программ из системного пути
    '''
    system_path = os.getenv('PATH')
    system_path_list = system_path.split(os.pathsep)
    programs = []
    for path in system_path_list:
        programs.extend(get_programs_in_path(path))
    return programs


def create_programs_json_file(filename):
    '''
    Данная функция создает JSON файл с информацией
    о системных программах
    '''
    programs = get_system_path_programs()

    data = {}
    for program in programs:
        folder, program_name = os.path.split(program)
        folder_data = data
        for subfolder in folder.split(os.sep):
            folder_data = folder_data.setdefault(subfolder, {})
        folder_data[program_name] = None

    with open(filename, 'w') as file:
        json.dump(data, file, indent=4) #indent - количество отступов при сериализации


create_programs_json_file('programs.json')
