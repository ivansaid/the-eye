from dateutil import parser


class LogDatabase:
    logs = []

    def insert(self, log):
        print("Log: ", log)
        self.logs.append(log)


class EyeDatabase:
    table_by_session_id = {}
    table_by_category = {}
    table_by_time = []

    def __init__(self, logger):
        self.logger = logger

    @staticmethod
    def check_valid_date(data_list, new_element):
        date1 = parser.parse(data_list[-1]["timestamp"])
        date2 = parser.parse(new_element["timestamp"])
        if date1 > date2:
            return False
        return True

    def insert(self, data):
        mandatory_keys = ["session_id", "category", "name", "data", "timestamp"]
        if data in mandatory_keys:
            if data['session_id'] in self.table_by_session_id:
                if self.check_valid_date(table_by_session_id['session_id'], data):
                    self.table_by_session_id['session_id'].append(data)
                else:
                    self.logger.insert({"process": "saving in database", "error message": "invalid timestamp"})
                    return
            else:
                self.table_by_session_id['session_id'] = []
                self.table_by_session_id['session_id'].append(data)
            if data['category'] in self.table_by_category:
                if self.check_valid_date(table_by_category['category'], data):
                    self.table_by_category['category'].append(data)
            else:
                self.table_by_category['category'] = []
                self.table_by_category['category'].append(data)
            self.table_by_time.append(data)
        else:
            self.logger.insert({"process": "saving in database", "error message": "invalid data"})
