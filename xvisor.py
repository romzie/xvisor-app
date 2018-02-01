import configparser
import itertools
import os
import csv


class Parser():


    def __init__(self):

        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        self.test_path = self.config['TEST_FILE']['path']
        self.ref_path = self.config['REF_FILE']['path']
        self.csv_path = self.config['CSV_FILE']['path']

        if not os.path.isfile(self.test_path):
            print('Error: Invalid test file path')
        if not os.path.isfile(self.ref_path):
            print('Error: Invalid reference file path')
        if os.path.isfile(self.csv_path):
            answer = input('Warning: CSV file already exists, overwrite it? (y/n) ')
            while answer.lower() not in ['y', 'n', 'yes', 'no']:
                answer = input('Expected y/n ')
            if answer in ['n', 'no']:
                exit(1)
        else:
            f = open(self.csv_path, 'a')
            f.close()


    def generate_csv(self):

        csv_delimiter = self.config['CSV_FILE']['delimiter']
        x_delimiter = self.config['FORMAT']['x_delimiter']

        with open(self.test_path, 'r') as testfile, \
                open(self.ref_path, 'r') as reffile, \
                open(self.csv_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile,
                                    delimiter=csv_delimiter)

            order = self.config['FORMAT']['xvisor_order'].split(x_delimiter)
            index_result = order.index(self.config['FORMAT']['id'])

            for tline, rline in itertools.zip_longest(testfile, reffile):
                if x_delimiter == '\\n':
                    csvline = [tline.rstrip('\n')]
                    tline = next(testfile)
                    csvline += [tline.rstrip('\n')]
                    res = next(testfile).rstrip('\n')
                else:
                    tline = tline.split(x_delimiter)
                    csvline = tline[:-1]
                    res = tline[index_result]
                csv_config = self.config['CSV_FILE']

                # ERROR
                if res.startswith(self.config['FORMAT']['error_msg']):
                    csv_writer.writerow(csvline + [csv_config['runtime_error_tag']])
                # DEADLOCK
                elif res == self.config['FORMAT']['deadlock_tag']:
                    csv_writer.writerow(csvline + [csv_config['deadlock_tag']])
                # CORRECT
                elif res == rline[:-1]:
                    csv_writer.writerow(csvline + [csv_config['correct_tag']])
                # WRONG VALUE
                else:
                    csv_writer.writerow(csvline + [csv_config['wrong_value_tag']])


if __name__ == '__main__':
    parser = Parser()
    parser.generate_csv()
