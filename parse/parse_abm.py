"""
Parse ABM data into the database. Should generate the agents, trips, and household tables.
steps:
"""

from parse.load_abm.abm_abstract import MagAbmLoader


def parse_abm(abm_data: str, database_url: str, dataname: str) -> None:
    mag_loader = MagAbmLoader(abm_data, database_url, dataname)
    if mag_loader.load_data():
        mag_loader.store_to_db()
    else:
        print('pass')


if __name__ == '__main__':
    database_link = r'C:\test_codes_delete_later\db_test\db_test.db'
    abm_data = [{
                    'abm_data': r'E:\Dropbox (ASU)\UAHS Team Share\Data\MAG\MAG ABM 2018\KYUNGHWI JEON - output_disaggPersonList.csv',
                    'dataname': 'AbmPerson'},
                {
                    'abm_data': r'E:\Dropbox (ASU)\UAHS Team Share\Data\MAG\MAG ABM 2018\Originals - Do not delete\KYUNGHWI JEON - adjusted_disaggTripList_in_tripListCarAllocation.csv',
                    'dataname': 'AbmTrip'},
                {
                    'abm_data': r'E:\Dropbox (ASU)\UAHS Team Share\Data\MAG\MAG ABM 2018\Originals - Do not delete\KYUNGHWI JEON - adjusted_disaggTripList_in_tripListCarAllocation.csv',
                    'dataname': 'AbmTrip'}
    ]

    for _ in abm_data:
        parse_abm(_['abm_data'], database_link, _['dataname'])
