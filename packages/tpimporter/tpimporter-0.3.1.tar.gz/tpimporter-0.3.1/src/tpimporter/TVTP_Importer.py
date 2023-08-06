from .Excel_Importer import Excel_Importer
from openpyxl import Workbook
from typing import List, Dict, Tuple, Set


class TVTP_Importer(Excel_Importer):
    callback_status_signal = None
    callback_progress_signal = None

    # SPECIFY FIELDNAMES AND CORRESPONDING EXCEL COLUMN NUMBERs HERE
    tv_series_map = {
        "titel_local": 5,
        "titel_ov": 16,
        "vendor_id": 4,
        "vendor_id_amazon": 60,
        "vendor_id_google": 63,
        "vendor_id_videoload": 66,
        "vendor_id_hollystar": 72,
        "channel_type": 9999,  # wird nicht aus Excel gelesen
    }

    tv_season_map = {
        "status": 0,
        "tnr": 1,
        "titel_local": 6,
        "number": 7,
        "mandant": 27,
        "est_start": 37,
        "genre": 19,
        "rating": 20,
        "licensor": 14,
        "production_year": 17,
        "production_country": 18,
        "quality": 21,
        "tv_network": 32,
        "vendor_id": 3,
        "vendor_id_itunes": 57,
        "vendor_id_amazon": 59,
        "vendor_id_google": 62,
        "vendor_id_videoload": 65,
        "vendor_id_maxdome": 68,
        "vendor_id_hollystar": 71,
        "initialprice_hd": 26,
        "initialprice_sd": 25,
        "initialprice_wsp_itunes_hd": 79,
        "initialprice_wsp_itunes_sd": 78,
        "initialprice_wsp_amazon_hd": 83,
        "initialprice_wsp_amazon_sd": 82,
        "country_de": 33,
        "country_at": 34,
        "country_ch": 35,
        "right_est": 36,
        "right_tvod": 39,
        "channel_type": 9999,  # wird nicht aus Excel gelesen
    }

    tv_episode_map = {
        "titel_local": 10,
        "number": 12,
        "est_start": 37,
        "tv_air_date": 31,
        "runtime": 13,
        "vendor_id": 2,
        "vendor_id_itunes": 56,
        "vendor_id_amazon": 58,
        "vendor_id_google": 61,
        "vendor_id_videoload": 64,
        "vendor_id_maxdome": 67,
        "vendor_id_hollystar": 70,
        "initialprice_hd": 24,
        "initialprice_sd": 23,
        "initialprice_wsp_itunes_hd": 77,
        "initialprice_wsp_itunes_sd": 76,
        "initialprice_wsp_amazon_hd": 81,
        "initialprice_wsp_amazon_sd": 80,
        "channel_type": 9999,  # wird nicht aus Excel gelesen
    }

    def __init__(self, valid_statuses=("ok", "change", "new")):
        super().__init__(valid_statuses)

    def _get_data_from_wb(self,
                          workbook: Workbook,
                          first_row: int = 4,
                          worksheet_name: str = "TPTV",
                          channel_type='transactional') -> Tuple[List[dict], List[dict], List[dict]]:
        """
        fetches data from the given Excel Workbook instance
        :param workbook: a Workbook instance
        :param first_row: the first row where we should expect the data to begin
        :param worksheet_name: name of the worksheet that should be read
        :param channel_type: possible values: transactional/filmtastic/arthousecnma/homeofhorror
        :return: Series Data, Season Data, Episodes Data
        """
        series_data = []
        season_data = []
        episode_data = []
        ws = workbook[worksheet_name]
        i = first_row
        for row in ws['A' + str(first_row):'HB20000']:
            try:
                # nur valide Items mit aktivem Status und einer Titelnummer nehmen
                if row[self.tv_season_map.get('tnr')].value and row[
                    self.tv_season_map.get('status')].value in self.valid_statuses:
                    # EPISODES
                    episode_data.append(self._get_row_data(row=row,
                                                           item_map=self.tv_episode_map,
                                                           channel_type=channel_type))
                    # SEASONS
                    if str(row[8].value).lower().strip() == 'x':
                        season_data.append(self._get_row_data(row=row,
                                                              item_map=self.tv_season_map,
                                                              channel_type=channel_type))

                        # SERIES
                        series_data.append(self._get_row_data(row=row,
                                                              item_map=self.tv_series_map,
                                                              channel_type=channel_type))
                i += 1

            except:
                self.callback_status(f'ERRROR reading in row nr: {i}')

        # doppelte Einträge in Serien löschen
        series_data = list({series['vendor_id']: series for series in series_data}.values())

        self.callback_progress(100)
        self.callback_status('reading data from TP - COMPLETE')
        return series_data, season_data, episode_data

    def _get_row_data(self, row, item_map: dict, channel_type: str) -> dict:
        """
        reads in data from an Excel-row; specify the data you want within the item_map dictionary
        (field_name:Column-Number in Excel);
        :param row: an Excel row
        :param item_map: a dictionary (field_name:Column-Number in Excel)
        :param channel_type: String; possible values: transactional/filmtastic/arthousecnma/homeofhorror
        :return: dictionary with the keys from item_map and the corresponding values from the Excel row
        """
        row_data = dict()
        for key, col_nr in item_map.items():
            if key == 'channel_type':
                row_data[key] = channel_type
            else:
                try:
                    row_data[key] = row[col_nr].value
                    if row[col_nr].value == '#N/A':
                        row_data[key] = None
                except:
                    row_data[key] = ""
        return row_data
