import csv
import json


class StoreAdapter():
    '''
    '''

    def __init__(self, method):
        self.method = method


    def store(self, data, url, delimiter, overwrite):
        if self.method == 'CSV':
            self.to_csv(data, url, delimiter)
        elif self.method == 'JSON':
            self.to_json(data, url, overwrite)
        elif self.method in ['TXT', 'HTML']:
            self.to_text_file(data, url)
        elif self.method == ['PDF', 'IMG']:
            self.to_binary_file(data, url)


    def to_csv(self, data, url, delimiter):
        with open(url, 'w', newline='', encoding='utf-8') as output_file:
            writer = csv.writer(output_file, delimiter=delimiter)
            for row in data:
                writer.writerow(row)


    def to_json(self, data, url, overwrite):
        if not overwrite:
            d = self.load_json(url)
            data.update(d)
        with open(url, 'w') as output_file:
            json.dump(data, output_file)

    
    def to_binary_file(self, data, url):
        '''
        Prints binary data into a binary file (ie. '.pdf').
        '''
        with open(url, 'wb') as output_file:
            output_file.write(data)


    def to_text_file(self, data, url):
        '''
        Prints text data into a text file (ie. '.txt', '.html').
        '''
        with open(output_path, 'w') as output_file:
            output_file.write(data)


    def load_json(self, url):
        with open(url, 'r') as input_file:
            d = json.load(input_file)
        return d
