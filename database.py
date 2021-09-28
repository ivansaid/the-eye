from dateutil import parser


class LogDatabase:
    logs = []

    def insert(self, log):
        print("Log: ", log)
        self.logs.append(log)


class EyeDatabase:


    def __init__(self, logger):
        self.logger = logger
        self.table_by_session_id = {}
        self.table_by_category = {}
        self.table_by_time = []

    @staticmethod
    def check_valid_date(data_list, new_element):
        date1 = parser.parse(data_list[-1]["timestamp"])
        date2 = parser.parse(new_element["timestamp"])
        if date1 > date2:
            return False
        return True

    def insert(self, data):
        mandatory_keys = ["session_id", "category", "name", "data", "timestamp"]
        valid = True
        for key in mandatory_keys:
            if key not in data.keys():
                valid = False
                break
        if valid:
            if data['session_id'] in self.table_by_session_id.keys():
                if self.check_valid_date(self.table_by_session_id[data['session_id']], data):
                    self.table_by_session_id[data['session_id']].append(data)
                else:
                    self.logger.insert(
                        {"process": "saving in database", "type": "Error", "message": "invalid timestamp"})
                    return
            else:
                self.table_by_session_id[data['session_id']] = []
                self.table_by_session_id[data['session_id']].append(data)
            if data['category'] in self.table_by_category.keys():
                if self.check_valid_date(self.table_by_category[data['category']], data):
                    self.table_by_category[data['category']].append(data)
                else:
                    self.logger.insert(
                        {"process": "saving in database", "type": "Error", "message": "invalid timestamp"})
                    return
            else:
                self.table_by_category[data['category']] = []
                self.table_by_category[data['category']].append(data)
            self.table_by_time.append(data)
            self.logger.insert(
                {"process": "saving in database", "type": "Process", "message": "saved successfully"})
        else:
            self.logger.insert({"process": "saving in database", "type": "Process", "message": "invalid data"})
