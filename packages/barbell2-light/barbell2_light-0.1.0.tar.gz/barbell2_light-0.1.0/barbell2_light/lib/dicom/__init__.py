import os

from pydicom._dicom_dict import DicomDictionary


def is_dicom_file(file_path_or_obj):
    file_obj = file_path_or_obj
    if isinstance(file_obj, str):
        if not os.path.isfile(file_obj):
            return False
        if file_obj.startswith('._'):
            return False
        file_obj = open(file_obj, "rb")
    try:
        return file_obj.read(132).decode('ASCII')[-4:] == 'DICM'
    except UnicodeDecodeError:
        return False


def is_tag_file(file_path):
    return file_path.endswith('.tag') and not file_path.startswith('._')


def tag_for_name(name):
    for key, value in DicomDictionary.items():
        if name == value[4]:
            return hex(int(key))
    return None


def get_dictionary_items():
    return DicomDictionary.items()
