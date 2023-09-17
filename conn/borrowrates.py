import pandas as pd
import logging
import ftplib
from io import StringIO
import pdb


class BorrowScraper:

    @staticmethod
    def get_ib_borrow_rates():

        ib_host = 'ftp3.interactivebrokers.com'
        ib_user = 'shortstock'
        ib_password = ''

        rates_fname = 'usa.txt'

        io_stream = StringIO()

        # Connect FTP Server
        ftp_server = ftplib.FTP(ib_host, ib_user, ib_password)

        # force UTF-8 encoding
        ftp_server.encoding = "utf-8"

        # Retrieve the file
        ftp_cmd = f"RETR {rates_fname}"
        ftp_server.retrlines(ftp_cmd, lambda x: io_stream.write(x + '\n'))

        io_stream.seek(0)

        # In pandas DataFrame
        df = pd.read_csv(io_stream, delimiter='|', skiprows=0, header=1, skipfooter=1, engine='python')

        # Clean-up
        df.columns = [
            'symbol', 'currency', 'name', 'con_id', 'isin', 'rebate_rate', 'fee_rate', 'available', 'dummy'
        ]
        df = df.drop(['isin', 'dummy'], axis=1)

        # Close FTP connection
        ftp_server.quit()

        return df


if __name__ == '__main__':

    logging.getLogger().setLevel(logging.WARNING)

    df_borrow_rates = BorrowScraper.get_ib_borrow_rates()

    # pdb.set_trace()

