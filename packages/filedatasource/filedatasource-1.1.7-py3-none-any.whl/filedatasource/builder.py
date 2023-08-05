from typing import Union, List, TextIO, BinaryIO, Any, Dict

from filedatasource import CsvReader, ExcelReader, CsvWriter, ExcelWriter, Mode, ReadMode, DataWriter, DataReader
from filedatasource.utils import attributes2list, dict_keys2list


def open_reader(fname: str, mode: ReadMode = ReadMode.OBJECT) -> DataReader:
    """ Create a CsvReader or a ExcelReader with the parameters by default only from the file path and the extension
    of the file name. If it ends with .csv.gz or .gz, then a CSV file is created, however, if the extension
    is .xls or .xlsx, then an Excel file is read.

    :param fname: The path to the Excel or CSV file.
    :param mode: The default mode to read the rows. When the reader is iterated,
        it will return objects, dictionaries or lists depending on if the value of this parameter is ReadMode.OBJECT,
        ReadMode.DICTIONARY or ReadMode.LIST, respectively.
    :return: A CsvReader or a ExcelReader depending on the file extension.
    """
    if fname.endswith('.csv') or fname.endswith('.csv.gz'):
        return CsvReader(fname, mode=mode)
    if fname.endswith('.xls') or fname.endswith('.xlsx'):
        return ExcelReader(fname, mode=mode)
    raise ValueError(f'The file name {fname} has to finish in .csv, .csv.gz, .xls, or .xlsx to use this function')


def open_writer(fname: str, fieldnames: List[str]) -> DataWriter:
    """ Create a CsvWriter or a ExcelWriter with the parameters by default only from the file path with a given
     extension, and the fieldnames. If the file extension ends with .csv.gz or .gz, then a CSV file is created,
     however, if the extension is .xls or .xlsx, then an Excel file is created.

    :param fname: The path to the Excel or CSV file.
    :param fieldnames: The name of the fields.
    :return: A CsvWriter or a ExcelWriter depending on the file extension.
    """
    if fname.endswith('.csv') or fname.endswith('.csv.gz'):
        return CsvWriter(fname, fieldnames=fieldnames)
    if fname.endswith('.xls') or fname.endswith('.xlsx'):
        return ExcelWriter(fname, fieldnames=fieldnames)
    raise ValueError(f'The file name {fname} has to finish in .csv, .csv.gz, .xls, or .xlsx to use this function')


def list2csv(file_or_io: Union[str, TextIO, BinaryIO], data: List[List[Any]],
             fieldnames: Union[List[str], type, object] = None,
             mode: Mode = Mode.WRITE, encoding: str = 'utf-8') -> None:
    """ Write a sequences of lists as a sequence of rows in a CSV file.

    :param file_or_io: The file path or an opened stream to use. If it is a file path and it ends in .gz, then
    :param data: The sequence of rows as lists.
    :param fieldnames: The field names of this CSV.
    :param mode: The writing mode: Mode.APPEND or Mode.WRITE. By default Mode.WRITE.
    :param encoding: The encoding (it is only used if the parameter file_or_io is a file path).
    """
    with CsvWriter(file_or_io, fieldnames, mode, encoding) as writer:
        writer.write_lists(data)


def dict2csv(file_or_io: Union[str, TextIO, BinaryIO], data: List[Dict],
             fieldnames: Union[List[str], type, object] = None,
             mode: Mode = Mode.WRITE, encoding: str = 'utf-8') -> None:
    """ Write a list of dictionaries in a CSV file.

    :param file_or_io: The file path or an opened stream to use. If it is a file path and it ends in .gz, then
        a compressed file is created using gzip.
    :param data: The list of dictionaries. Each dictionary has to contain as keys the fieldnames and as value
        the row data to store.
    :param fieldnames: The field names of this CSV.
    :param mode: The writing mode: Mode.APPEND or Mode.WRITE. By default Mode.WRITE.
    :param encoding: The encoding (it is only used if the parameter file_or_io is a file path).
    """
    with CsvWriter(file_or_io, fieldnames, mode, encoding) as writer:
        writer.write_dicts(data)


def objects2csv(file_or_io: Union[str, TextIO, BinaryIO], data: List[object],
                fieldnames: Union[List[str], type, object] = None,
                mode: Mode = Mode.WRITE, encoding: str = 'utf-8') -> None:
    """ Write a sequence of objects in a CSV file.

    :param file_or_io: The file path or an opened stream to use. If it is a file path and it ends in .gz, then
        a compressed file is created using gzip.
    :param data: The sequence of objects to write with public attributes or properties.
    :param fieldnames: The field names of this CSV.
    :param mode: The writing mode: Mode.APPEND or Mode.WRITE. By default Mode.WRITE.
    :param encoding: The encoding (it is only used if the parameter file_or_io is a file path).
    """
    with CsvWriter(file_or_io, fieldnames, mode, encoding) as writer:
        writer.write_objects(data)


def list2excel(fname: str, data: List[List[Any]], sheet: Union[str, int] = 0,
               fieldnames: Union[List[str], type, object] = None) -> None:
    """ Write a sequences of lists as a sequence of rows in an Excel file.

    :param fname: The file path to the Excel file.
    :param data: The sequence of rows as lists.
    :param sheet: The sheet to write.
    :param fieldnames: The list of fieldnames. It could be given as a list or a type or object with properties or
    attributes.
    """
    with ExcelWriter(fname, sheet, fieldnames) as writer:
        writer.write_lists(data)


def dict2excel(fname: str, data: List[Dict], sheet: Union[str, int] = 0,
               fieldnames: Union[List[str], type, object] = None) -> None:
    """ Write a list of dictionaries in an Excel file.

    :param fname: The file path to the Excel file.
    :param data: The list of dictionaries. Each dictionary has to contain as keys the fieldnames and as value
        the row data to store.
    :param sheet: The sheet to write.
    :param fieldnames: The list of fieldnames. It could be given as a list or a type or object with properties or
    attributes.
    """
    with ExcelWriter(fname, sheet, fieldnames) as writer:
        writer.write_dicts(data)


def objects2excel(fname: str, data: List[object], sheet: Union[str, int] = 0,
                  fieldnames: Union[List[str], type, object] = None) -> None:
    """ Write a sequence of objects in an Excel file.

    :param fname: The file path to the Excel file.
    :param data: The sequence of objects to write with public attributes or properties.
    :param sheet: The sheet to write.
    :param fieldnames: The list of fieldnames. It could be given as a list or a type or object with properties or
    attributes.
    """
    with ExcelWriter(fname, fieldnames, sheet) as writer:
        writer.write_objects(data)


def csv2list(file_or_io: Union[str, TextIO, BinaryIO], encoding: str = 'utf-8') -> List[List[Any]]:
    """ Read a CSV file (compressed or not) and return a list of lists with the file rows.

    :param file_or_io: The file path or the file stream.
    :param encoding: The file encoding.
    :return: A List of lists with the file rows. Each column value is stored as list element.
    """
    with CsvReader(file_or_io, ReadMode.LIST, encoding) as reader:
        return reader.read_lists()


def csv2dict(file_or_io: Union[str, TextIO, BinaryIO], encoding: str = 'utf-8') -> List[Dict]:
    """ Read a CSV file (compressed or not) and return a list of dictionaries with the file content..

    :param file_or_io: The file path or the file stream.
    :param encoding: The file encoding.
    :return: A list of dictionaries. Each dictionary represents a row and it contains as keys the column name and
    its value the column value.
    """
    with CsvReader(file_or_io, ReadMode.DICT, encoding) as reader:
        return reader.read_rows()


def csv2objects(file_or_io: Union[str, TextIO, BinaryIO], encoding: str = 'utf-8') -> List[object]:
    """ Read a CSV file (compressed or not) and return a list of objects.

    :param file_or_io: The file path or the file stream.
    :param encoding: The file encoding.
    :return: A list of objects. Each object is a file row with the attributes as column names and its value.
    """
    with CsvReader(file_or_io, ReadMode.OBJECT, encoding) as reader:
        return reader.read_objects()


def excel2list(fname: str, sheet: Union[str, int] = 0) -> List[List[Any]]:
    """ Read a Excel file (xlsx or xls) and return a list of lists with the file rows.

    :param fname: The file path to the Excel file..
    :param sheet: The sheet name or the sheet number (starting by 0).
    :return: A List of lists with the file rows. Each column value is stored as list element.
    """
    with ExcelReader(fname, sheet, ReadMode.LIST) as reader:
        return reader.read_lists()


def excel2dict(fname: str, sheet: Union[str, int] = 0) -> List[Dict]:
    """ Read a Excel file (xlsx or xls) and return a list of dictionaries with the file content..

    :param fname: The file path to the Excel file.
    :param sheet: The sheet name or the sheet number (starting by 0).
    :return: A list of dictionaries. Each dictionary represents a row and it contains as keys the column name and
    its value the column value.
    """
    with ExcelReader(fname, sheet, ReadMode.DICT) as reader:
        return reader.read_rows()


def excel2objects(fname: str, sheet: Union[str, int] = 0) -> List[object]:
    """ Read a Excel file (xlsx or xls) and return a list of objects.

    :param fname: The file path to the Excel file.
    :param sheet: The sheet name or the sheet number (starting by 0).
    :return: A list of objects. Each object is a file row with the attributes as column names and its value.
    """
    with ExcelReader(fname, sheet, ReadMode.OBJECT) as reader:
        return reader.read_objects()


def load(fname: str, mode: ReadMode = ReadMode.OBJECT) -> Union[List[object], List[Dict], List[List]]:
    """
    Load an Excel or CSV file and return a list of objects with the file content.
    :param fname: The file path to the file.
    :param mode: The default mode to read the rows. When the reader is iterated,
        it will return objects, dictionaries or lists depending on if the value of this parameter is ReadMode.OBJECT,
        ReadMode.DICTIONARY or ReadMode.LIST, respectively.
    :return: A list of objects. Each object is a file row with the attributes as column names and the attribute values
    as column values.
    """
    if mode == ReadMode.OBJECT:
        return load_objs(fname)
    elif mode == ReadMode.DICT:
        return load_dicts(fname)
    elif mode == ReadMode.LIST:
        return load_lists(fname)


def load_objs(fname: str) -> List[object]:
    """
    Load an Excel or CSV file and return a list of objects with the file content.
    :param fname: The file path to the file.
    :return: A list of objects. Each object is a file row with the attributes as column names and the attribute values
    as column values.
    """
    with open_reader(fname) as reader:
        return [obj for obj in reader]


def load_dicts(fname) -> List[Dict]:
    """
    Load an Excel or CSV file and return a list of dictionaries with the file content.
    :param fname: The file path to the file.
    :return: A list of dictionaries. Each dictionary is a file row with the keys as column names
    and with the dictionary values as column values.
    """
    with open_reader(fname, mode=ReadMode.DICT) as reader:
        return [d for d in reader]


def load_lists(fname) -> List[List]:
    """
    Load an Excel or CSV file and return a list of lists with the file content.
    :param fname: The file path to the file.
    :return: A list of lists. Each list is a file row with the column values.
    """
    with open_reader(fname, mode=ReadMode.LIST) as reader:
        return [lst for lst in reader]


def save(fname: str, objs: List[object]) -> None:
    """
    Save a list of objects as a rows of an Excel or CSV file.
    :param fname: the file path to the file.
    :param objs: The list of objects to write. All objects must have the same attribute or property names.
    """
    save_objs(fname, objs)


def save_objs(fname: str, objs: List[object]) -> None:
    """
    Save a list of objects as a rows of an Excel or CSV file.
    :param fname: the file path to the file.
    :param objs: The list of objects to write. All objects must have the same attribute or property names.
    """
    if not objs:
        raise ValueError('The list of objects has to contain at least one object to use this method.')
    with open_writer(fname, fieldnames=attributes2list(objs[0])) as writer:
        writer.write_objects(objs)


def save_dicts(fname: str, dicts: List[Dict]) -> None:
    """
    Save a list of dictionaries as a rows of an Excel or CSV file.
    :param fname: the file path to the file.
    :param dicts: The list of dictionaries to write. All the dictionaries must have the same key names.
    """
    if not dicts:
        raise ValueError('The list of dictionaries has to contain at least one dictionary to use this method.')
    with open_writer(fname, fieldnames=dict_keys2list(dicts[0])) as writer:
        writer.write_dicts(dicts)


def save_lists(fname: str, lists: List[List], fieldnames: List[str]) -> None:
    """
    Save a list of lists as a rows of an Excel or CSV file.
    :param fname: the file path to the file.
    :param fieldnames: the list of column names.
    :param lists: The list of lists to write.
    """
    if not lists:
        raise ValueError('The list of list has to contain at least one list to use this method.')
    with open_writer(fname, fieldnames=fieldnames) as writer:
        writer.write_lists(lists)
