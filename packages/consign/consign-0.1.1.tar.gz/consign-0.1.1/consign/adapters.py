import csv
import json


class StoreAdapter():
    '''
    '''

    def __init__(self, method):
        self.method = method


    def store(self, data, url, delimiter, update):
        if self.method == 'CSV':
            self.to_csv(data, url, delimiter)
        elif self.method == 'JSON':
            self.to_json(data, url, update)


    def to_csv(self, data, url, delimiter):
        with open(url, 'w', newline='', encoding='utf-8') as output_file:
            writer = csv.writer(output_file, delimiter=delimiter)
            for row in data:
                writer.writerow(row)


    def to_json(self, data, url, update):
        if update:
            d = self.load_json(url)
            data.update(d)
        with open(url, 'w') as output_file:
            json.dump(data, output_file)


    def load_json(self, url):
        with open(url, 'r') as input_file:
            d = json.load(input_file)
        return d
