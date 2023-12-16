from shortuuid import uuid

def random_file_name(file_name):
    return uuid() + '_' + file_name