"""
A GUI class that generates a form for the user to interact with as well as the line graph the user will see.
This form has a radio button for genders, racial drop-downs, education drop-downs, start and end year drop-downs.
Once all items are selected and the user hits search, a line graph will appear with the relevant data.
"""
from business import data_validation, get_data, verify_items_selected
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import threading
from tkinter import filedialog
from tkinter import IntVar
import tkinter as tk
from tkinter import ttk
matplotlib.use('Agg')


class NcvsForm:
    def __init__(self, root):
        self.root = root
        self.root.title('NCVS Search')

        self.education_levels = ['No Schooling', 'Grade School', 'Middle School', 'High School', 'College']
        self.race_options = ['White', 'Black', 'American Indian', 'Asian', 'More than One', 'Hispanic']
        self.year_options = ['1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003',
                             '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014',
                             '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022']
        self.gender_group = IntVar()

        self.male_radio_button = ttk.Radiobutton(
            root, text='Male', variable=self.gender_group, value=0, command=NotImplemented)
        self.female_radio_button = ttk.Radiobutton(
            root, text='Female', variable=self.gender_group, value=1, command=NotImplemented)
        self.education_combo_box = ttk.Combobox(root, values=self.education_levels)
        self.education_combo_box.configure(state='readonly')
        self.education_combo_box.set('Select Education Level')
        self.race_combo_box = ttk.Combobox(root, values=self.race_options)
        self.race_combo_box.configure(state='readonly')
        self.race_combo_box.set('Select Race')
        self.year_start_combo_box = ttk.Combobox(root, values=self.year_options)
        self.year_start_combo_box.configure(state='readonly')
        self.year_start_combo_box.set('Select Start Year')
        self.year_end_combo_box = ttk.Combobox(root, values=self.year_options)
        self.year_end_combo_box.configure(state='readonly')
        self.year_end_combo_box.set('Select End Year')
        self.search_button = ttk.Button(root, text='Search', command=self.search_button, width=10)
        self.export_button = ttk.Button(root, text='Export', command=self.export_graph_data, width=10)
        self.close_button = ttk.Button(root, text='Exit', command=self.close_app, width=10)
        self.graph_spot = ttk.Notebook(root, width=500, height=300)
        self.graph_tab = ttk.Frame(self.graph_spot)
        self.graph_spot.add(self.graph_tab, text='Graph Tab')
        self.status_label = ttk.Label(root, text="")
        self.export_filename = None
        self.fig = None

        self.male_radio_button.grid(column=0, row=2, sticky='w')
        self.female_radio_button.grid(column=0, row=3, sticky='w')
        self.education_combo_box.grid(column=1, row=2, columnspan=2)
        self.year_start_combo_box.grid(column=3, row=2, padx=5)
        self.year_end_combo_box.grid(column=3, row=3, padx=5)
        self.race_combo_box.grid(column=1, row=3, columnspan=2)
        self.search_button.grid(column=0, row=4)
        self.export_button.grid(column=1, row=4)
        self.close_button.grid(column=3, row=4)
        self.status_label.grid(column=2, row=4)
        self.graph_spot.grid(column=0, row=5, columnspan=4)

    @staticmethod
    def close_app():
        exit()

    def search_button(self):
        start_year = self.year_start_combo_box.get()
        end_year = self.year_end_combo_box.get()

        # if not start_year_str or not end_year_str:
        #     return
        # try:
        #     start_year = int(start_year_str)
        #     end_year = int(end_year_str)
        # except ValueError:
        #     return
        gender = 1 if self.gender_group.get() == 0 else 2
        race_mapping = {
            'White': 1,
            'Black': 2,
            'American Indian': 3,
            'Asian': 4,
            'More than One': 5,
            'Hispanic': 6
        }
        race = race_mapping.get(self.race_combo_box.get(), None)
        if race is None:
            return

        education_mapping = {
            'No Schooling': 1,
            'Grade School': 2,
            'Middle School': 3,
            'High School': 4,
            'College': 5
        }
        education = education_mapping.get(self.education_combo_box.get(), None)
        if education is None:
            return

        if verify_items_selected(start_year, end_year, race, education):
            if data_validation.check_dates(start_year, end_year):
                self.status_label.configure(text='Data retrieved')
                data = get_data(start_year, end_year, gender, race, education)
                for widget in self.graph_tab.winfo_children():
                    widget.destroy()
                self.create_and_display_graph(data)
                self.graph_spot.select(self.graph_tab)
            else:
                self.status_label.configure(text='Invalid date, start date must be greater than end date')
        else:
            self.status_label.configure(text='Invalid data, check combo boxes.')

    def create_and_display_graph(self, data):
        years = list(data.keys())
        counts = list(data.values())

        self.fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(years, counts)
        ax.set_xlabel('Year')
        ax.set_ylabel('Victims')
        ax.set_title('Victims Over Time')

        canvas = FigureCanvasTkAgg(self.fig, self.graph_tab)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        toolbar = NavigationToolbar2Tk(canvas, self.graph_tab)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def export_graph_data(self):
        if not self.export_filename:
            self.export_filename = tk.filedialog.asksaveasfilename(defaultextension=".png",
                                                                   filetypes=[("PNG files", "*.png")])
            if not self.export_filename:
                return
        if self.fig:
            self.fig.savefig(self.export_filename)
