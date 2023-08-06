import os

def list_all_files(path_dir:str)-> [str]:
    files = []
    for (dirpath, dirnames, filenames) in os.walk(path_dir):
        for filename in filenames:
            files.append(os.path.join(dirpath, filename))
    return files

def write_response_to_file(filename:str, r):
    """writefile.

        writefile is an utility function which create filename's parent folders
        if not exists and write r.content into filename

    Args:
        filename (str): filename
        r:
    """
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    with open(filename, 'wb') as f:
        f.write(r.content)

