from os import system
import os
import tkinter as tk
from controlers import Data, Migrations, Project, Time, Tracks, Clock
# okokoko

class MainView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.migrations()
        self.projects = Project().get_all()
        self.layout_config()
        self.layout()
        self.config_wigets()
        self.timer = False
        self.start = 0
        self.stop = 0
        self.clock = 0

    def layout(self):
        self.master.geometry('600x450+0+0')
        self.master.config(bg='white')
        self.master.grid()
        self.master.grid_columnconfigure((0, 1, ), weight=1)

        self.project_pick = tk.StringVar()
        self.project_pick.set("Wybierz projekt")

        self.communication = tk.Label(self.master, text='CENTRUM KOMUNIKACJI')
        self.communication.grid(row=0, columnspan=2, column=0, padx=0, ipadx=0,
                                ipady=8)
        self.option_label = tk.Label(self.master, text='Wybierz projekt:')
        self.option_label.grid(row=1, column=0, padx=0, ipadx=0, pady=(22, 2))
        self.drop_menu = tk.OptionMenu(self.master, self.project_pick,
                                       *self.projects,)
        self.drop_menu.grid(row=2, column=0, padx=10, ipadx=2, ipady=2,)
        self.menu = self.master.nametowidget(self.drop_menu.menuname)

        self.start_button = tk.Button(self.master, text='START',
                                      command=self.timer_clock)
        self.start_button.grid(row=2, column=1, ipadx=0, ipady=2)

        self.label_add = tk.Label(self.master, text='Dodaj projekt:')
        self.label_add.grid(row=3, column=0, padx=0, ipadx=0, pady=(22, 2),)
        self.add_project_entry = tk.Entry(self.master)
        self.add_project_entry.grid(row=4, column=0, padx=2, ipadx=2, ipady=5,)
        self.add_button = tk.Button(self.master, text='DODAJ',
                                    command=self.add_project)
        self.add_button.grid(row=4, column=1, ipadx=2, ipady=2)
        self.clock_label = tk.Label(self.master, text='0:00:00')
        self.clock_label.grid(row=5, column=0, columnspan=2, ipadx=10,
                              ipady=0, padx=0, pady=20)
        self.project_time = tk.Label(self.master, text='0:00:00')
        self.project_time.grid(row=6, column=0, padx=0, ipadx=0, ipady=5,)

        self.show_time = tk.Button(self.master, text='Pokaż czas',
                                   command=self.show_time_for_picked_project)
        self.show_time.grid(row=6, column=1, ipadx=0, ipady=2)
        self.export_to_csv = tk.Button(self.master,
                                       text='Zapisz do pliku',
                                       command=self.save_csv)
        self.export_to_csv.grid(row=7, column=0, ipadx=0, ipady=2,
                                padx=0, pady=20)

    def config_wigets(self):
        self.master.configure(bg='#333', relief='flat', padx=10, pady=10)
        self.communication.config(**self.options, width=300,)
        self.option_label.config(**self.options_labels, width=15,)
        self.drop_menu.config(**self.options, width=25, highlightthickness=0)
        self.start_button.config(**self.options, width=25,)
        self.menu.config(**self.options)
        self.label_add.config(**self.options_labels, width=25,)
        self.add_project_entry.config(**self.options, width=29,)
        self.add_button.config(**self.options, width=25,)
        self.clock_label.config(bg=self.bg, fg=self.fg, relief='flat',
                                font=self.font_clock, width=455)
        self.project_time.config(**self.options, width=29,)
        self.show_time.config(**self.options, width=25,)
        self.export_to_csv.config(**self.options, width=25,)

    def layout_config(self):
        self.master.title('Time Tracker')
        self.master.iconbitmap(self.resource_path('./icon/timer.ico'))

        self.font = ('helvetica', 12)
        self.font_clock = ('PT Mono', 25)
        self.font_labels = ('helvetica', 11, 'italic')
        self.fg = '#f1f1f1'
        self.bg = '#444'
        self.options = dict(bg=self.bg, fg=self.fg,
                            relief='flat', font=self.font)
        self.options_labels = dict(bg='#333', fg=self.fg,
                                   relief='flat', font=self.font_labels)

    def timer_clock(self):
        if self.project_pick.get() == "Dodaj projekt poniżej":
            self.communication.config(text='DODAJ PROJEKT', fg='#F00')
            return
        elif self.project_pick.get() == "Wybierz projekt":
            self.communication.config(text='Najpierw WYBIERZ', fg='#F00')
            self.communication.after(5000, self.default_comunicator_setter)
            return
        elif not self.timer:
            self.communication.config(text='Rozpoczęto mierzenie')
            self.timer = True
            self.start = Clock.starting_track()
            self.start_button['text'] = 'STOP'
            print(self.project_pick.get())
            self.clock_shower()
            self.communication.after(10000, self.default_comunicator_setter)
            return
        self.timer = False
        project_id = Project().get_id_by_name(self.project_pick.get())
        print(project_id)
        self.end = Clock.endinging_track()
        time_diff = Time(self.start, self.end).save()
        Tracks().save(project_id, self.start, self.end, time_diff)
        self.start_button['text'] = 'START'
        self.communication['text'] = 'Zakończono mierzenie'
        self.show_time_for_picked_project()
        self.communication.after(10000, self.default_comunicator_setter)

    def add_project(self):
        name = self.add_project_entry.get()
        comment = Project().save(name)
        print(comment)
        self.communication.config(text=comment)
        self.projects = Project().get_all()
        print('uzupelniono liste projektow')
        self.add_project_entry.delete(0, "end")
        self.update_project_list()

    def update_project_list(self):
        menu = self.drop_menu["menu"]
        menu.delete(0, "end")
        for project in self.projects:
            menu.add_command(label=project,
                             command=lambda i=project:
                                 self.project_pick.set(i))

    def clock_shower(self):
        if self.timer:
            print(Clock.timing(self.clock))
            self.clock_label.config(text=Clock.timing(self.clock))
            self.clock_label.after(1000, self.clock_shower)
            self.clock += 1
            return
        self.clock = 0

    def show_time_for_picked_project(self):
        if self.project_pick.get() == "Wybierz projekt":
            self.communication.config(text='Najpierw WYBIERZ', fg='#F00')
            self.communication.after(5000, self.default_comunicator_setter)
            return
        project_id = Project().get_id_by_name(self.project_pick.get())
        actual_time = Tracks().show_time_for_current(project_id)
        self.project_time['text'] = actual_time

    def default_comunicator_setter(self):
        self.communication.config(text='CENTRUM KOMUNIKACJI', fg=self.fg)

    def save_csv(self):
        Data.saving_to_csv()
        self.communication.config(text='Zapisano plik CSV', fg=self.fg)

    def migrations(self):
        Migrations.make_database_migration()

    def do_nothing(self):
        self.timer_clock()
        self.master.destroy()
        print('zapisane i ubite :P')

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = system._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)


if __name__ == '__main__':
    root = tk.Tk()
    myapp = MainView(root)
    root.protocol('WM_DELETE_WINDOW', myapp.do_nothing)
    myapp.mainloop()
