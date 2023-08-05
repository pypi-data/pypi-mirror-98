from abc import ABC, ABCMeta
from typing import Union, List

from filedatasource.datafile import DataReader, DataFile, DataWriter, ReadMode


def open_xls(fname: str):
    """  Open an Excel file in the old xls format importing the module.

    :param fname: The path to the xls file.
    :return: The workbook which is a instance of xlrd.book.Book class.
    """
    try:
        xlrd = __import__('xlrd')
    except ImportError:
        raise ModuleNotFoundError('xlrd is required. Please, install it with:\n\npip install xlrd')
    return xlrd.open_workbook(fname)


def open_xlsx(fname: str):
    """  Open an Excel file in xlsx format importing the module.

    :param fname: The path to the xlsx file.
    :return: The workbook which is a instance of Workbook class.
    """
    try:
        openpyxl = __import__('openpyxl')
    except ImportError:
        raise ModuleNotFoundError('openpyxl is required. Please, install it with:\n\npip install openpyxl')
    return openpyxl.load_workbook(fname)


def create_xlsx(fname: str):
    """  Create an Excel file in the xlsx format importing the module.

    :param fname: The path to save the xlsx file.
    :return: The workbook which is a instance of Workbook class.
    """
    try:
        xlsxwriter = __import__('xlsxwriter')
    except ImportError:
        raise ModuleNotFoundError('xlsxwriter is required. Please, install it with:\n\npip install xlsxwriter')
    return xlsxwriter.Workbook(fname)


def create_xls():
    """  Create an Excel file in the old xls format importing the module.

    :return: The workbook which is a instance of xlrd.book.Book class.
    """
    try:
        xlwt = __import__('xlwt')
    except ImportError:
        raise ModuleNotFoundError('xlwt is required. Please, install it with:\n\npip install xlwt')
    return xlwt.Workbook()


class ExcelData(DataFile, ABC):
    """ Abstract class to define the common attributes of the Excel files. """
    __metaclass__ = ABCMeta

    @property
    def fieldnames(self) -> List[str]:
        """
        :return: The list of fieldnames.
        """
        return self._fieldnames

    @property
    def sheet_name(self) -> str:
        """
        :return:  The sheet name.
        """
        return self.__sheet_name

    @property
    def sheet(self):
        """
        :return: The sheet object.
        """
        return self._sheet

    def __init__(self, fname: str, sheet: Union[str, int] = None) -> None:
        """ Constructor.
        :param fname: The file path to the Excel file.
        :param sheet: The sheet to read/write.
        """
        super().__init__(fname)
        self.__sheet_name = sheet if sheet else 0
        self._sheet = None
        self._fieldnames = []


class ExcelReader(ExcelData, DataReader):
    """ The class to read an Excel file easily. """
    def __init__(self, fname: str, sheet: Union[str, int] = 0, mode: ReadMode = ReadMode.OBJECT) -> None:
        """ Constructor.
        :param fname: The file path to the Excel file.
        :param sheet: The sheet to read/write.
        :param mode: The default mode to read the rows. When the reader is iterated,
        it will return objects, dictionaries or lists depending on if the value of this parameter is ReadMode.OBJECT,
        ReadMode.DICTIONARY or ReadMode.LIST, respectively.
        """
        super(ExcelReader, self).__init__(fname, sheet=sheet)
        DataReader.__init__(self, fname, mode=mode)
        if fname.endswith('.xlsx'):
            self.__doc = open_xlsx(fname)
            self._sheet = self.__doc[sheet] if isinstance(sheet, str) else self.__doc[self.__doc.sheetnames[sheet]]
            self._fieldnames = [cell.value for cell in next(self.sheet.rows)]
            self.__type = 'xlsx'
        elif fname.endswith('.xls'):
            doc = open_xls(fname)
            self.__doc = doc
            self._sheet = doc.sheet_by_name(sheet) if isinstance(sheet, str) else doc.sheet_by_index(sheet)
            self._fieldnames = [cell.value for cell in self.sheet.row(0)]
            self.__type = 'xls'
        else:
            raise ValueError(f'The file name {fname} has to end in .xls or .xlsx.')

        self.__row = 1

    def read_row(self) -> object:
        """ Read a row of the Excel file as a dict.

        :return: A dictionary where the keys are the fieldnames, and their values the row values.
        """
        sheet = self.sheet
        if self.__row < (sheet.max_row if self.__type == 'xlsx' else sheet.nrows):
            self.__row += 1
            if self.__type == 'xlsx':
                return self.__read_xlsx_row(sheet)
            else:
                return self.__read_xls_row(sheet)
        raise StopIteration()

    def close(self) -> None:
        """ Nothing to do. """
        pass

    def __read_xlsx_row(self, sheet) -> dict:
        """ Write a row using openpyxl module.
        :param sheet: The sheet to write the row.
        :return: A dict with the fieldnames as keys.
        """
        return {self.fieldnames[i]: sheet.cell(row=self.__row, column=i + 1).value for i in range(sheet.max_column)}

    def __read_xls_row(self, sheet) -> dict:
        """ Write a row using xlrd module.
        :param sheet: The sheet to write the row.
        :return: A dict with the fieldnames as keys.
        """
        return {self.fieldnames[i]: cell.value for i, cell in enumerate(sheet.row(self.__row - 1))}

    def __len__(self) -> int:
        """
        :return: The number of rows.
        """
        return (self.sheet.max_row if self.__type == 'xlsx' else self.sheet.nrows) - 1


class ExcelWriter(ExcelData, DataWriter):
    """ The class to create an Excel file easily """
    def __init__(self, fname: str, sheet: Union[str, int] = None, fieldnames: Union[List[str], type, object] = None):
        """ Constructor.
        :param fname: The file path to the Excel file.
        :param sheet: The sheet to read/write.
        :param fieldnames: The list of fieldnames. It could be given as a list or a type or object with properties or
        attributes.
        """
        super().__init__(fname, sheet)
        self._fieldnames = self._parse_fieldnames(fieldnames)
        if fname.endswith('.xlsx'):
            self._doc = create_xlsx(fname)
            self._sheet = self._doc.add_worksheet(sheet if sheet else 'Sheet')
            self.__type = 'xlsx'
        else:
            self._doc = create_xls()
            self._sheet = self._doc.add_sheet(sheet if sheet else 'Sheet')
            self.__type = 'xls'
        self.__num_row = 0
        self.write_list(self.fieldnames)

    def write_row(self, **row) -> None:
        """ Append a row to the sheet.

        :param row: The row to append.
        """
        sheet_row = self.sheet.row(self.__num_row) if self.__type == 'xls' else self.sheet
        for i, field in enumerate(self.fieldnames):
            if field in row:
                if self.__type == 'xls':
                    sheet_row.write(i, row[field])
                else:
                    sheet_row.write(self.__num_row, i, row[field])
        self.__num_row += 1

    def close(self) -> None:
        """ Close saving the file. """
        if self.__type == 'xls':
            self._doc.save(self.file_name)
        else:
            self._doc.close()

    def __len__(self) -> int:
        """
        :return: The number of rows.
        """
        return self.__num_row - 1
