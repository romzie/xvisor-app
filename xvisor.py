import configparser
import itertools
import os
import csv
import re
import sys


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
        if os.path.isfile(self.csv_path) and not sys.argv[1] == "-y":
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

        with open(self.test_path, 'r') as testfile, \
                open(self.ref_path, 'r') as reffile, \
                open(self.csv_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile,
                                    delimiter=csv_delimiter)
            testbody = testfile.read()

            # Find prefixes in output file
            addr_p = self.config['FORMAT']['prefix_addr']
            addr_reg = re.compile(addr_p + "[0-9A-Fa-f]{8}")
            addrs = addr_reg.findall(testbody)
            cycle_p = self.config['FORMAT']['prefix_cycle']
            cyc_reg = re.compile(cycle_p + " \d+")
            cycles = cyc_reg.findall(testbody)
            res_p = self.config['FORMAT']['prefix_result']
            res_reg = re.compile(res_p + ".*")
            results = res_reg.findall(testbody)

            # Remove prefixes
            addrs = [a[len(addr_p)-2:] for a in addrs]
            cycles = [c[len(cycle_p):].replace(' ', '') for c in cycles]
            results = [r[len(res_p)+1:] for r in results]

            for i, rline in \
                    itertools.zip_longest(range(len(addrs)), reffile):

                csvline = [addrs[i], cycles[i]]
                csv_config = self.config['CSV_FILE']
                rte_tag = self.config['FORMAT']['prefix_err']
                dl_tag = self.config['FORMAT']['deadlock_tag']

                # ERROR
                if results[i].startswith(rte_tag) and \
                        not rline.startswith(rte_tag):
                    csv_writer.writerow(csvline
                            + [csv_config['runtime_error_tag']])

                # DEADLOCK
                elif results[i] == dl_tag:
                    csv_writer.writerow(csvline
                            + [csv_config['deadlock_tag']])

                # CORRECT
                elif results[i] == rline[:-1]:
                    csv_writer.writerow(csvline
                            + [csv_config['correct_tag']])
                # WRONG VALUE
                else:
                    csv_writer.writerow(csvline
                            + [csv_config['wrong_value_tag']])


if __name__ == '__main__':
    parser = Parser()
    parser.generate_csv()
