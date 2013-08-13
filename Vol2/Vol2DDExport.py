import sys, argparse, urllib.request

class DDExporter:

    def __init__(self, input_items, dict_url, verbose):
        self.verbose = verbose
        self.input_items = input_items
        self.dict_url = dict_url

    def write_custom_dd(self, output_file):
        custom_dd_file = open(output_file, 'w', encoding='utf-8')

        if self.verbose:
            print ('Writing output file to ' + output_file)

        custom_dd_file.write(self.custom_dd)
        custom_dd_file.close()

        if self.verbose:
            print ('Finished writing.')

    def build_custom_dd(self):
        if self.verbose:
            print ('Building custom Data Dictionary...')
            
        missing_items = []
        items_html = ''
        start_html = self.dict_html[:self.dict_html.find("<body>")].replace('../','http://www.naaccr.org/Applications/')
        start_html += self.dict_html[self.dict_html.find('<div id="Panel2"'):self.dict_html.find("<a name='")]

        end_html = '''
                </div>
            </body>
        </html>
        '''

        for item in self.items_list:
            if item in self.dict_entries:
                items_html += self.dict_entries[item]
            else:
                missing_items.append(item)

        if len(missing_items) > 0:
            print ('The following items were not found in the dictionary: ')
            print (missing_items)

        self.custom_dd = start_html + items_html + end_html
    
    def parse_dict_entries(self):
        if self.verbose:
            print ('Getting HTML from ' + self.dict_url)

        self.dict_html = str(urllib.request.urlopen(self.dict_url).read(), encoding='utf8')
        
        if self.verbose:
            print ('Parsing Data Dictionary entries from HTML file...')
            
        self.dict_entries = {}
        name_anchor = "<a name='"
        index = self.dict_html.find(name_anchor)

        while index > 0:
            item_start = index
            number_start = index + 9
            number_end = self.dict_html.find("'", number_start)
            next_anchor = self.dict_html.find(name_anchor, number_end)
            
            if next_anchor == -1:
                item_end = self.dict_html.find("</div></body>", number_end)
            else:
                item_end = next_anchor

            self.dict_entries[self.dict_html[number_start:number_end]] = self.dict_html[item_start:item_end]

            index = next_anchor

        if self.verbose:
            print ('Entries found: ' + str(len(self.dict_entries)))

    def parse_items(self):
        if self.verbose:
            print ('Reading items file...')

        items_file = open(self.input_items, 'r', encoding='utf-8')
        items_raw = items_file.read()
        items_file.close()
        
        if self.verbose:
            print ('Parsing items from CSV file...')

        items_raw = items_raw.replace("'","")
        items_raw = items_raw.replace('"','')
        items_raw = items_raw.replace('\n',',')
        items_raw = items_raw.replace(',,',',')
        items_raw = items_raw.replace(' ','')
        items_raw = items_raw.strip()
        self.items_list = items_raw.split(',')

        if self.items_list[-1] == '':
            self.items_list.pop()

def main():
    verbose = False
    dict_url = "http://www.naaccr.org/Applications/ContentReader/Default.aspx?c=10"
    output_file = 'custom_dd.html'

    parser = argparse.ArgumentParser()
    parser.add_argument("items", help="Name of CSV file containing comma-separated list of item numbers to extract from Data Dictionary.")
    parser.add_argument("-d", "--dictionary", help="URL of HTML file containing a copy of the Volume II Data Dictionary. Default: http://www.naaccr.org/Applications/ContentReader/Default.aspx?c=10.")
    parser.add_argument("-o", "--output", help="Name of HTML file for output of custom data dictionary. Default: custom_dd.html")
    parser.add_argument("-v", "--verbose", help="Turn on verbose logging.", action="store_true")
    args = parser.parse_args()

    input_items = args.items

    if args.dictionary is not None:
        dict_url = args.dictionary

    if args.output is not None:
        output_file = args.output

    if args.verbose:
        verbose = True

    ddexp = DDExporter(input_items, dict_url, verbose)
    ddexp.parse_dict_entries()
    ddexp.parse_items()
    ddexp.build_custom_dd()
    ddexp.write_custom_dd(output_file)

    if verbose:
        print ('Exiting...')

if __name__ == '__main__':
    main()
