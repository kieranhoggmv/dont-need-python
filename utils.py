import io
import os
from msoffcrypto import OfficeFile
from msoffcrypto.format.ooxml import OOXMLFile
import pandas as pd
from xlrd import XLRDError


def remove_password(file_path: str, password: str) -> io.BytesIO:
    """Takes a MS office file and removes the given password for it

    Parameters:
        file_path (str): The location of a file
        password (list): The password to use

    Returns:
        decrypted_file (io.BytesIO): the in-memory file with the password removed
    """
    with open(file_path, "rb") as f:
        msoffcryptoobj = OfficeFile(f)
        msoffcryptoobj.load_key(password=password)
        decrypted_file = io.BytesIO()
        msoffcryptoobj.decrypt(decrypted_file)
    return decrypted_file


def add_password(file_path: str, password: str, file_suffix="-pp"):
    """Adds a password to an Office file

    Parameters:
        file_path (str): The location of a file
        password (list): The password to use

    Returns:
        filename (str): The new filename of the file saved with the password
    """
    file_parts = file_path.split(".")

    # Wedge the file_suffix before the final "."
    new_file_path = "".join(file_parts[:-1]) + file_suffix + "." + file_parts[-1]
    new_filename = new_file_path.split(os.sep)[-1]
    with open(file_path, "rb") as previous_file:
        new_file = OOXMLFile(previous_file)

        with open(new_file_path, "wb") as f:
            new_file.encrypt(password, f)

    os.remove(file_path)
    return new_filename


def folder_to_dataframes(
    folder_path: str = None, file_types: list = ["csv", "xlsx"], password_map: dict = {}, rename_func=None
) -> list[pd.DataFrame]:
    """Opens a folder of file and converts them into pandas DataFrames

    Parameters:
        folder_path (str): The location of a directory to look for the files in
        file_types (list): A list of file extensions to open from the folder
        password_map (dict): A dictionary mapping of filename to passwords to use
        rename_func (func): A function to rename the file based on its dataframe

    Returns:
        df_list: A list of pandas DataFrames
    """
    df_list = []
    if folder_path is not None:
        path = folder_path
    else:
        path = os.getcwd()

    for file in os.listdir(path):
        df = None
        file_path = os.path.join(path, file)
        if file.endswith(tuple(file_types)):
            if file.endswith("csv"):
                df = pd.read_csv(file_path)
            elif file.endswith("xlsx"):
                try:
                    df = pd.read_excel(file_path)
                except XLRDError:
                    # File has a password on it, try the password map, ask if not present
                    if password_map and file in password_map.keys():
                        password = password_map[file]
                        print(f"Using password provided for {file}")
                    else:
                        password = input(f'Enter password for "{file_path}": ')
                    df_list.append(pd.read_excel(remove_password(file_path, password)))
            else:
                raise NotImplementedError(
                    f"File type {file.split(".")[-1]} not supported yet"
                )
        if df and rename_func:
            df.to_excel(rename_func(df))
    return df_list
