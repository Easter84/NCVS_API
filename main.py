"""
This project queries the DOJ National Criminal Victim Survey 1993-2023
This module is responsible for launching the application.
Created by: Timothy Easter
"""
from models import NcvsForm
import tkinter as tk


def main():
    root = tk.Tk()
    app = NcvsForm(root)
    app.root.mainloop()


if __name__ == '__main__':
    main()
