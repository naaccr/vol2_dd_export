# Author: Joshua Whitley - NAACCR, Inc.
# Created: 8/13/2013
# Modified: 8/13/2013
#
# This file is part of vol2_dd_export.
#
# vol2_dd_export is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# vol2_dd_export is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with vol2_dd_export.  If not, see <http://www.gnu.org/licenses/>.

import os
from Vol2.Vol2DDExport import DDExporter
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.ttk import *

class Vol2CustomDD(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   

        self.parent = parent
        self.parent.resizable(0,0)
        self.advanced_open = False
        self.os = os.name

        self.items_file = StringVar()
        
        self.output_file = StringVar()
        self.output_file.set(os.path.abspath(os.path.dirname(__file__)) + os.sep + "custom_dd.html")

        self.chap_x_url = StringVar()
        self.chap_x_url.set("http://www.naaccr.org/Applications/ContentReader/Default.aspx?c=10")

        self.init_ui()
        self.center_window()
    
    def init_ui(self):
        self.parent.title("Volume II Custom Data Dictionary Exporter")
        self.style = Style()

        if self.os == 'nt':
            self.style.theme_use("winnative")
            self.textbox_width = 64
        else:
            self.style.theme_use("default")
            self.textbox_width = 47

        self.pack(fill=BOTH, expand=1)

        Label(self, text="Items File:").grid(column=1, row=1, sticky=E)
        Label(self, text="Output File:").grid(column=1, row=2, sticky=E)
        Label(self, text="Chapter X URL:").grid(column=1, row=4, sticky=E)
        self.status = Label(self.parent, text="", relief=SUNKEN, anchor=W)
        self.status.place(anchor=SW, relwidth=1.0, rely=1.0)

        Button(self, text="Browse...", command=self.items_browse_click).grid(column=3, row=1)
        Button(self, text="Browse...", command=self.output_browse_click).grid(column=3, row=2)
        self.advanced_button = Button(self, text="Advanced " + u"\u25BC", command=self.advanced_click)
        self.advanced_button.grid(column=1, row=3)
        Button(self, text="Generate", command=self.generate_click).grid(column=3, row=3)

        self.items_file_entry = Entry(self, textvariable=self.items_file, width=self.textbox_width)
        self.items_file_entry.grid(column=2, row=1)

        self.output_file_entry = Entry(self, textvariable=self.output_file, width=self.textbox_width)
        self.output_file_entry.grid(column=2, row=2)

        self.chap_x_entry = Entry(self, textvariable=self.chap_x_url, width=self.textbox_width)
        self.chap_x_entry.grid(column=2, row=4)

        for child in self.winfo_children():
            child.grid_configure(padx=7, pady=7)

    def center_window(self):
        w = 600
        h = 140
        
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()

        x = (sw - w) / 2
        y = (sh - h) / 2
        self.parent.geometry('%dx%d+%d+%d' % (w, h, x, y))

    def items_browse_click(self):
        fname = askopenfilename(parent=self,
                                filetypes=(("CSV files", "*.csv"), ("All files", "*.*")),
                                defaultextension='csv')

        if fname != '':
            try:
                self.items_file.set(os.path.normpath(fname))
            except:
                messagebox.showerror("Open Items File", "Failed to read file\n'%s'" % fname)

    def output_browse_click(self):
        fname = asksaveasfilename(parent=self,
                                  initialfile=self.output_file.get(),
                                  filetypes=(("HTML files", "*.html;*.htm"), ("All files", "*.*")),
                                  defaultextension='html')

        if fname != '':
            try:
                self.output_file.set(os.path.normpath(fname))
            except:
                messagebox.showerror("Set Output File", "Failed to set file\n'%s'" % fname)

    def advanced_click(self):
        current_geo = self.parent.geometry()
        current_w = int(current_geo[:current_geo.find('x')])
        current_h = int(current_geo[current_geo.find('x')+1:current_geo.find('+')])

        if self.advanced_open:
            self.advanced_button["text"] = "Advanced " + u"\u25BC"
            self.parent.geometry('%dx%d' % (current_w, current_h - 40))
            self.advanced_open = False
        else:
            self.advanced_button["text"] = "Advanced " + u"\u25B2"
            self.parent.geometry('%dx%d' % (current_w, current_h + 40))
            self.advanced_open = True

    def generate_click(self):
        if self.items_file.get() == '':
            messagebox.showerror("File Error", "You must select an items file.")
        elif self.output_file.get() == '':
            messagebox.showerror("File Error", "You must select an output file.")
        elif self.chap_x_url.get() == '':
            messagebox.showerror("URL Error", "Chapter X URL cannot be empty.")
        else:
            self.status["text"] = "Generating document..."
            self.status.update()

            ddexp = DDExporter(self.items_file.get(), self.chap_x_url.get(), False)
            ddexp.parse_dict_entries()
            ddexp.parse_items()
            ddexp.build_custom_dd()
            ddexp.write_custom_dd(self.output_file.get())

            self.status["text"] = "Document complete!"

def main():
    root = Tk()
    app = Vol2CustomDD(root)
    root.mainloop()

if __name__ == '__main__':
    main()
