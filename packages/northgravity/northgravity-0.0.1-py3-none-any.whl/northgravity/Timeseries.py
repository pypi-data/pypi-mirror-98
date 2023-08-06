from .HTTPCalller import HTTPCaller
from .DatalakeHandler import *
import csv
from datetime import datetime

log = logging.getLogger('NG SDK')


class Timeseries:
    def __init__(self):
        self.caller = HTTPCaller()
        self.uploader = DatalakeHandler()

    def retrieve_data_as_csv(self, file_name: str, symbols: dict, columns, group_name: str,
                             start_date: str = None, end_date: str = None):

        '''
        The method retrieves the data from NG Timeseries based on symbols and columns.
        Optionally start and end dates can be specified. If no dates specified, all the available data are taken.

        :param file_name: the name of file locally to save data to
        :param symbols: symbols to identify data in Timeseries. Must dictionary {"symbolName": "symbolValue", ...}
        :param columns: name of column or list of columns to retrieve
        :param group_name: name of the group
        :param start_date: start date of data in the format YYYY-MM-DD. If time is included, it must follow ISO format:
        YYYY-MM-DDTHH:mm:ss (note the 'T' letter separating the date and time part)
        :param end_date: end date of the data in the format YYYY-MM-DD. If time is included, it must follow ISO format:
        YYYY-MM-DDTHH:mm:ss (note the 'T' letter separating the date and time part)
        :return: saves file with data
        '''

        # start_date is optional: if not provided, the data are taken from the very beginning
        if start_date is not None:
            # date only
            try:
                datetime.strptime(start_date, "%Y-%m-%d")
                start_date = start_date + "T00:00:00"
            except:
                # if cannot parse to date only, it may contain time
                try:
                    datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S")
                except:
                    raise Exception(f'Wrong format of date is passed for start date.'
                                    f'The accepted datetime formats are: YYYY-MM-DD or YYYY-MM-DDTHH:mm:ss. '
                                    f'E.g., 2021-02-05 or 2021-02-05T12:30:00')

        # start_date is optional: if not provided, the data are taken from the very beginning
        if end_date is not None:
            # date only
            try:
                datetime.strptime(end_date, "%Y-%m-%d")
                # till the end of day
                end_date = end_date + "T23:59:59"
            except:
                # if cannot parse to date only, it may contain time
                try:
                    datetime.strptime(end_date, "%Y-%m-%dT%H:%M:%S")
                except:
                    raise Exception(f'Wrong format of date is passed for end date.'
                                    f'The accepted datetime formats are: YYYY-MM-DD or YYYY-MM-DDTHH:mm:ss.'
                                    f'E.g., 2021-02-05 or 2021-02-05T12:30:00'
                                    )

        if not isinstance(columns, list):
            columns = [columns]

        body = {
            "startDate": start_date,
            "endDate": end_date,
            "keys": [
                {
                    "symbols": symbols,
                    "groupName": group_name,
                    "columns": columns
                }
            ],
            "formatType": "NCSV"
        }

        log.debug(f'Retrieving data for symbols: {symbols} '
                  f'\nand columns: {columns}'
                  f'\nfrom date: {start_date}'
                  f'\nto date: {end_date}')

        r = self.caller.post(path='/ts', payload=body)
        log.debug(f'Response: {r.text}')

        with open(file_name, "w") as text_file:
            text_file.write(r.text)

        log.debug(f'Data are saved to file: {file_name}')


    def upload_data(self, file_name, symbols_columns, date_column, group_name):
        '''
        The methods uploads data to Timeseries by re-arranging the columns order and uploading the new file as NCSV.
        :param file_name: csv file to be upload to Timeseries
        :param symbols_columns: columns to be used as symbols
        :param date_column: date column in the file; is renamed to DateTime as expected by NCSV
        :param group_name: group name for the NCSV file to upload
        :return: id of the NCSV file uploaded
        '''

        # get all column names form csv file
        with open(file_name) as csv_file:
            csv_reader = csv.DictReader(csv_file)
            dict_from_csv = dict(list(csv_reader)[0])
            all_cols = list(dict_from_csv.keys())

        log.debug(f'Original file {file_name} contains columns: {all_cols}')

        assert len(all_cols) != 0, "No columns in csv"
        assert all([x in all_cols for x in symbols_columns]), f"Symbols are not in columns list {symbols_columns}"
        assert date_column in all_cols, f"No column {date_column} in the list"

        # create new order of columns => symbols, date column, value columns
        key = symbols_columns + ['DateTime']
        value_columns = [x for x in all_cols if x not in key and x != date_column]
        final_cols = key + value_columns

        log.debug(f'Columns will be re-ordered to NCSV format: {final_cols}')

        # to keep file in the same place where the original file is
        parent_folder = os.path.dirname(file_name)
        temp_file = os.path.join(parent_folder, 'temp.csv')

        # write reordered csv to the temporary file
        with open(file_name, 'r') as infile, open(temp_file, 'a') as outfile:
            reader = csv.DictReader(infile)
            writer = csv.writer(outfile)

            # write header
            writer.writerow(final_cols)
            for row in reader:
                # change date_column to DateTime
                row['DateTime'] = row.pop(date_column)

                # prepare new line as per new columns order
                line = [row[x] for x in final_cols]
                writer.writerow(line)
        log.debug(f'File with re-ordered column is saved as {temp_file}')

        # upload file as NCSV to the specified group
        fid = self.uploader.upload_file(file_path=temp_file, group_name=group_name, file_type='NCSV')
        log.debug(f'File is uploaded as NCSV: {fid}')

        os.remove(temp_file)
        log.debug(f'Temporal file {temp_file} is removed.')

        return fid
