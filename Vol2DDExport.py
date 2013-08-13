import sys, argparse, urllib.request

class DDExporter:

    def __init__(self, input_items, dict_url, output_file, verbose):
        self.verbose = verbose

        if self.verbose:
            print ('Getting HTML from ' + dict_url)

        dict_html = str(urllib.request.urlopen(dict_url).read(), encoding='utf8')

        items_file = open(input_items, 'r', encoding='utf-8')
        items_raw = items_file.read()
        items_file.close()

        dict_entries = self.parse_dict_entries(dict_html)
        items_list = self.parse_items(items_raw)

        custom_dd = self.build_custom_dd(dict_html, dict_entries, items_list)
        custom_dd_file = open(output_file, 'w', encoding='utf-8')

        if self.verbose:
            print ('Writing output file to ' + output_file)

        custom_dd_file.write(custom_dd)
        custom_dd_file.close()

        if self.verbose:
            print ('Exiting...')

    def build_custom_dd(self, dict_html, dict_entries, items_list):
        if self.verbose:
            print ('Building custom Data Dictionary...')
            
        missing_items = []
        items_html = ''
        start_html = dict_html[:dict_html.find("<body>")].replace('../','http://www.naaccr.org/Applications/')
        start_html += dict_html[dict_html.find('<div id="Panel2"'):dict_html.find("<a name='")]

        end_html = '''
                </div>
            </body>
        </html>
        '''

        for item in items_list:
            if item in dict_entries:
                items_html += dict_entries[item]
            else:
                missing_items.append(item)

        if len(missing_items) > 0:
            print ('The following items were not found in the dictionary: ')
            print (missing_items)

        return start_html + items_html + end_html

    def parse_dict_entries(self, dict_html):
        if self.verbose:
            print ('Parsing Data Dictionary entries from HTML file...')
            
        dict_entries = {}
        name_anchor = "<a name='"
        index = dict_html.find(name_anchor)

        while index > 0:
            item_start = index
            number_start = index + 9
            number_end = dict_html.find("'", number_start)
            next_anchor = dict_html.find(name_anchor, number_end)
            
            if next_anchor == -1:
                item_end = dict_html.find("</div></body>", number_end)
            else:
                item_end = next_anchor

            dict_entries[dict_html[number_start:number_end]] = dict_html[item_start:item_end]

            index = next_anchor

        if self.verbose:
            print ('Entries found: ' + str(len(dict_entries)))

        return dict_entries

    def parse_items(self, items_raw):
        if self.verbose:
            print ('Parsing items from CSV file...')

        items_raw = items_raw.replace("'","")
        items_raw = items_raw.replace('"','')
        items_raw = items_raw.replace('\n',',')
        items_raw = items_raw.replace(',,',',')
        items_raw = items_raw.replace(' ','')
        items_raw = items_raw.strip()
        items_list = items_raw.split(',')

        if items_list[-1] == '':
            items_list.pop()
        
        return items_list

if __name__ == '__main__':
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

    ddexp = DDExporter(input_items, dict_url, output_file, verbose)
