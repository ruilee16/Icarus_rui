# This is the beginning of Icarus module
import networkx as nx

from databaseHandler import readdata


def create_nt(db_name):
    # Use a breakpoint in the code line below to debug your script.
    reader = readdata.LinkFetcher(db_name)
    return reader.fetch_data_to_df('links')


# Press the green button in the gutter to run the script.
temp = None
if __name__ == '__main__':
    temp = create_nt(r'C:\test_codes_delete_later\db_test\db_test.db')
    print('finish')