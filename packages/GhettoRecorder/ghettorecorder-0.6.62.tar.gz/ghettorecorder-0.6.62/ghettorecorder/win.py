# 0.1.2
import logging
from pathlib import Path
import os
from tkinter import ttk
from time import sleep

try:
    from ghettorecorder.lib.edit import UItextEditor
    from ghettorecorder.lib import term
except ImportError:
    from lib.edit import UItextEditor
    from lib import term

try:
    import tkinter as tk
except ImportError:
    print(f'\n\n  Please install --> python3-tk: on Ubuntu sudo apt-get install python3-tk\n\n')
try:
    from tkinter.filedialog import askdirectory, askopenfilename
except ImportError:
    print(f'\n error tkinter.filedialog import askdirectory, askopenfilename\n')


# logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s',)


class UIWindow(tk.Tk):
    box_list = []
    search_list = []
    entry_list = []
    lbl_li = []

    timer_val = ['', 1, 2, 4, 6, 12, 24]
    language_list = ['eng', 'deutsch']
    data_dir_set = False
    record_started = False
    search_started = False
    start_screen = True

    def __init__(self, radio_dir=None, settings_path=None):
        super().__init__()
        self.list_e = []
        self.gr_version = '0.6.6'
        self.radio_dir = radio_dir
        self.settings_path = settings_path

        self.title(f"Ghetto Recorder {self.gr_version} Concrete IT (by René Horn)")
        self.geometry('{}x{}'.format(700, 510))

        # main containers create
        self.top_frame = tk.Frame(master=self, bg='azure3', width=700, height=50, pady=3)
        self.center = tk.Frame(master=self, bg='white', width=700, height=410, padx=3, pady=3)
        self.btm_frame = tk.Frame(master=self, bg='azure3', width=700, height=50, pady=3)

        # main containers layout
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.top_frame.grid(row=0, sticky="ew")
        self.center.grid(row=1, sticky="nsew")
        self.btm_frame.grid(row=2, sticky="ew")

        # center widgets create
        self.center.grid_rowconfigure(0, weight=1)
        self.center.grid_columnconfigure(1, weight=1)

        self.ctr_left = tk.Frame(self.center, bg='blue', width=25, height=360)
        self.canvas = tk.Canvas(self.center, bg='cornflowerblue', width=570, height=410, bd=0)
        self.ctr_mid = tk.Frame(self.center, bg='azure3', width=570, height=410, padx=3, pady=3)
        self.ctr_right = tk.Frame(self.center, bg='green', width=25, height=410, padx=3, pady=3)
        self.progressbar = ttk.Progressbar(self.ctr_right, orient="vertical", length=400, mode="determinate")  # -10 ok
        # center grid
        self.ctr_left.grid(row=0, column=0, sticky="ns")
        self.canvas.grid(row=0, column=1, sticky="nsew")

        self.ctr_mid.grid(row=0, column=1, sticky="nsew")
        self.ctr_right.grid(row=0, column=2, sticky="ns")
        self.ctr_mid.grid_remove()  # call .grid again

        # upper frame Buttons
        self.lbl_ini = tk.Label(self.top_frame, bg='azure3')
        self.btn_ini = tk.Button(self.top_frame, text="Radio list", width=10, command=self.browse_file_button)
        self.lbl_browse = tk.Label(self.top_frame, bg='azure3')
        self.btn_browse = tk.Button(self.top_frame, text="Save to ...", width=10, command=self.browse_dir_button)
        self.lbl_timer = tk.Label(self.top_frame, text='Timer', bg='azure3', anchor="s")
        self.combo_timer = ttk.Combobox(self.top_frame, state="readonly", width=5, values=self.timer_val)
        self.lbl_lang = tk.Label(self.top_frame, text='Language', bg='azure3', anchor="s")
        self.combo_lang = ttk.Combobox(self.top_frame, state="readonly", width=5, values=self.language_list)

        self.entry_ini = tk.Entry(self.top_frame, background="white", borderwidth=1, relief=tk.FLAT, width=70)
        self.entry_ini.insert(0, ' Path to settings.ini')
        self.entry_bbr = tk.Entry(self.top_frame, background="white", borderwidth=1, relief=tk.FLAT, width=70)
        self.entry_bbr.insert(0, ' place to create a bunch of folders')

        # upper frame layout

        self.lbl_ini.grid(row=0, column=0, padx=2, pady=2, sticky="w")
        self.btn_ini.grid(row=0, column=1, padx=2, pady=2, sticky='w')
        self.entry_ini.grid(row=0, column=2, columnspan=3, padx=5, sticky='e')
        self.lbl_timer.grid(row=0, column=5, padx=10, sticky="s")
        self.lbl_lang.grid(row=0, column=6, padx=10, sticky="s")

        self.lbl_browse.grid(row=1, column=0, padx=2, pady=2, sticky="w")
        self.btn_browse.grid(row=1, column=1, padx=2, sticky='w')
        self.entry_bbr.grid(row=1, column=2, columnspan=3, padx=5, sticky='e')
        self.combo_timer.grid(row=1, column=5, padx=10, sticky='e')
        self.combo_timer.current(3)
        self.combo_lang.grid(row=1, column=6, padx=10, sticky='e')
        self.combo_lang.current(0)

        # Middle
        self.ghetto_canvas = tk.Canvas(self.ctr_mid, width=650, height=400, bg='azure3')
        # self.ghetto_canvas = tk.Canvas(self.ctr_mid, width=540, height=350, bg='azure3')
        self.ghetto_canvas.grid(row=0, column=1, sticky="nsew")

        self.canvas_frame = tk.Frame(self.ghetto_canvas, bg='azure3')
        self.ghetto_canvas.create_window(0, 0, window=self.canvas_frame, anchor='nw')

        self.canvas_frame.bind('<Enter>', self._bound_to_mousewheel)
        self.canvas_frame.bind('<Leave>', self._unbound_to_mousewheel)

        # center
        self.lbl_record_cb = tk.Label(self.canvas_frame, text='Record', underline=0, bg='azure3')
        self.lbl_search_entry = tk.Label(self.canvas_frame,
                                         text='Search multiple words (record if match): podcast concert elvis',
                                         underline=0, bg='azure3')
        self.lbl_search_cb = tk.Label(self.canvas_frame, text='Search', bg='azure3')
        self.lbl_radio_cb = tk.Label(self.canvas_frame, text='Radio', bg='azure3')
        self.lbl_search_middle = tk.Label(self.canvas_frame, text='Search option: Artist Title',
                                          bg='azure3', foreground='blue')

        # bottom

        self.lbl_rec = tk.Label(master=self.btm_frame, bg='azure3', anchor="s")
        self.btn_editor = tk.Button(master=self.btm_frame, text="Radio Editor",
                                    width=10, padx=2, pady=1, command=UItextEditor)
        self.btn_stop = tk.Button(master=self.btm_frame, text="Stop", width=10, padx=2, pady=1, command=self.exit_app)
        self.btn_rec = tk.Button(master=self.btm_frame, text="Record", width=10,
                                 padx=2, pady=1, command=self.list_checked)
        self.lbl_info = tk.Label(master=self.btm_frame, bg='azure3', anchor="s")

        # bottom grid
        self.lbl_rec.grid(row=0, column=0, padx=10, sticky="w")
        self.btn_editor.grid(row=0, column=1, sticky='e')
        self.btn_stop.grid(row=0, column=2, sticky='w')
        self.btn_rec.grid(row=0, column=3, sticky='w')
        self.lbl_info.grid(row=0, column=4, sticky='e')

        self.canvas.create_rectangle(0, 0, 250, 190, fill='cornflowerblue', width=0)
        self.canvas.create_line(0, 125, 2000, 125, fill='orange', width=10)
        self.canvas.bind("<Enter>", self.on_enter)
        self.canvas.bind("<Leave>", self.on_leave)

        # show path to settings.ini
        ini_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "settings.ini")
        term.GBase.settings_path = ini_file
        self.entry_ini.delete(0, tk.END)
        self.entry_ini.insert(0, ini_file)
        self.lbl_info.config(text='"Radio List" Starte oben links./ Start upper left. Web Radios.')

        term.GBase.pool.submit(self.language_select)

    def on_enter(self, event):
        self.canvas.create_line(0, 225, 2000, 225, fill='orange', width=10, tag="line")

    def on_leave(self, enter):
        self.canvas.delete("line")

    def _bound_to_mousewheel(self, event):
        self.ghetto_canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.ghetto_canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.ghetto_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def set_settings_path(self, settings_path):
        self.settings_path = settings_path

    def set_radio_dir(self, radio_dir):
        self.radio_dir = radio_dir

    def browse_dir_button(self):
        dir_name = askdirectory(title='Ghetto Recorder')
        if not dir_name:
            return
        self.set_radio_dir(dir_name)
        self.entry_bbr.delete(0, tk.END)
        self.entry_bbr.insert(0, dir_name)
        term.GBase.radio_base_dir = dir_name
        # self.lbl_browse.config(text=dir_name)
        self.data_dir_set = True
        return dir_name

    def browse_file_button(self):
        filepath = askopenfilename(
            filetypes=[("INI Files", "*.ini"), ("All Files", "*.*")],
            title='Ghetto Recorder',
            initialdir=os.path.dirname(os.path.abspath(__file__))
        )
        if not filepath:
            return
        self.set_settings_path(filepath)
        self.entry_ini.delete(0, tk.END)
        self.entry_ini.insert(0, filepath)

        term.GBase.settings_path = filepath  # set new path
        term.GIni.show_items_ini_file()
        # get the radios
        self.load_settings(term.GIni.list_items, self.canvas_frame)  # scrollbar
        self.btn_ini = tk.Button(self.top_frame, text="Radio list", width=10, state="disabled")
        self.btn_ini.grid(row=0, column=1, sticky='w')

        return filepath

    def print_dir(self):
        data_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "radiostations")
        test_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kreuzberg")
        try:
            with open(test_file, 'wb') as record_file:

                record_file.write(b'\x03')
            os.remove(test_file)

            if not self.data_dir_set:
                term.GBase.radio_base_dir = data_folder
                term.GBase.make_directory(data_folder)
                self.entry_bbr.delete(0, tk.END)
                self.entry_bbr.insert(0, data_folder)

        except Exception as ex:
            print(ex)
            self.entry_bbr.delete(0, tk.END)
            self.entry_bbr.insert(0, 'My directory is read only')

    def exit_app(self):
        term.GBase.exit_app = True
        sleep(term.GBase.sleeper + 1)  # threads sleep too, time for exit
        self.btn_rec = tk.Button(master=self.btm_frame, text="Record", width=10, command=self.list_checked)
        self.btn_rec.grid(row=0, column=3, sticky='w')
        term.GBase.exit_app = False

    def cb_checked(self):
        is_playlist_server = ''
        for ctr, int_var in enumerate(self.box_list):
            if int_var.get():  # IntVar not zero==checked
                self.lbl_li[ctr].configure(foreground='black')  # <widget>.configure(foreground='black',bg='red')

    def cb_search(self):
        for ctr, int_var in enumerate(self.search_list):
            # search checkbox selection
            if int_var.get():  # IntVar not zero==checked
                self.entry_list[ctr].delete(0, tk.END)
                # set the related record check box
                self.box_list[ctr].set(1)
                self.lbl_li[ctr].configure(foreground='red')  # <widget>.configure(foreground='black',bg='red')
                print(self.lbl_li[ctr].cget("text"))

    def load_settings(self, list_of_widgets, frame):

        self.start_screen = False
        self.print_dir()
        self.box_list = []
        self.search_list = []
        self.ctr_mid.grid()  # init scrollbar connected frame
        self.canvas.grid_remove()  # remove start screen

        self.lbl_search_middle.grid(row=0, column=1, sticky="ew")
        self.lbl_record_cb.grid(row=1, column=2, sticky="e")
        self.lbl_search_entry.grid(row=1, column=1, sticky="n")
        self.lbl_search_cb.grid(row=1, column=0, sticky="w")
        self.lbl_radio_cb.grid(row=1, column=3, sticky="w")

        # draw the scrollbar
        ghetto_scrolly = tk.Scrollbar(self.ctr_mid, orient=tk.VERTICAL)
        ghetto_scrolly.config(command=self.ghetto_canvas.yview)
        self.ghetto_canvas.config(yscrollcommand=ghetto_scrolly.set)
        ghetto_scrolly.grid(row=0, column=5, sticky="ns")

        ghetto_scrollx = tk.Scrollbar(self.ctr_mid, orient=tk.HORIZONTAL)
        ghetto_scrollx.config(command=self.ghetto_canvas.xview)
        self.ghetto_canvas.config(xscrollcommand=ghetto_scrollx.set)
        ghetto_scrollx.grid(row=1, column=1, sticky="ew")

        self.canvas_frame.bind("<Configure>", self.update_scrollregion)

        for idx, text in enumerate(list_of_widgets):
            self.box_list.append(tk.IntVar())  # auto var from python PY_VAR0 1 2 for finding check buttons
            self.search_list.append(tk.IntVar())
            lbl = tk.Label(frame, text=text, bg='azure3')
            lbl.grid(row=idx + 2, column=3, sticky="w")
            self.lbl_li.append(lbl)

            entry = tk.Entry(frame, width=60, bg='azure3')
            entry.grid(row=idx + 2, column=1, sticky="w")

            self.entry_list.append(entry)
            tk.Checkbutton(frame, variable=self.search_list[-1],
                           command=self.cb_search, bg='azure3').grid(row=idx + 2, column=0, sticky='e')

            tk.Checkbutton(frame, variable=self.box_list[-1],
                           command=self.cb_checked, bg='azure3').grid(row=idx + 2, column=2, sticky='e')

    def list_checked(self):

        term.GBase.pool.submit(self.display_info_text)

        for ctr, int_var in enumerate(self.box_list):
            # all checked rec.
            if int_var.get():

                # all get a string, that is never found
                term.GIni.search_dict[self.lbl_li[ctr].cget("text")] = "x!c?42"

                # SEARCH check only metadata, start rec. if found
                self.record_started = True
                if self.search_list[ctr].get():  # not zero = True
                    self.search_started = True
                    # update dict for threads going to search def GRecorder.search_pattern_start_record
                    term.GIni.search_dict[self.lbl_li[ctr].cget("text")] = self.entry_list[ctr].get()
                    term.GIni.search_title_keys_list.append(self.lbl_li[ctr].cget("text"))
                    sleep(2)
                    # update label with search content from entry
                    self.lbl_info.config(text=self.entry_list[ctr].get())

                # PLAYLIST is handled in add_server_to..UI, bit diff. than in terminal
                # self.add_server_to_data_base_ui(str(self.lbl_li[ctr].cget("text")),
                #                                str(term.GIni.find_ini_file(self.lbl_li[ctr].cget("text"))))

                term.add_server_to_data_base_auto(str(self.lbl_li[ctr].cget("text")),
                                                  str(term.GIni.find_ini_file(self.lbl_li[ctr].cget("text"))))

        self.btn_rec = tk.Button(master=self.btm_frame, text="Record", width=10, state="disabled")
        self.btn_rec.grid(row=0, column=3, sticky='w')

        # here updated list, zombies deleted
        for key in term.GIni.ini_keys:
            term.test_stream_server(key)
        # term.step2_test_stream_server(term.GIni.ini_keys) not yet

        for key in term.GIni.ini_keys:
            # term.GBase.pool.submit(term.record, key)
            term.GBase.pool.submit(self.start_records, key)

        term.GBase.pool.submit(self.display_title)

        # if selected, start timer
        if self.combo_timer.get():
            new_timer = int(self.combo_timer.get()) * 3600  # 60s * 60m = ?
            term.GBase.pool.submit(self.timer, new_timer)
            self.progressbar.grid(row=0, column=0, sticky='s')

    @staticmethod
    def start_records(key):

        # ----- no del -- term.GRecorder.thread_pull_song_name(url, key, None, None)
        stream_suffix = term.GIni.srv_param_dict[key + '_file']
        term.GRecorder.current_song_dict[key] = '_no-name-record_no_split_'  # init the dict for this thread
        term.GIni.start_stop_recording[key] = 'start'
        term.GIni.start_stop_recording[key + '_adv'] = 'start_from_here'

        for _ in term.GIni.search_title_keys_list:
            if _ == key:
                term.GIni.start_stop_recording[key] = 'stop'

        url = term.GIni.ini_keys[key]
        print(f'{key} {url}')
        dir_save = term.GBase.radio_base_dir + '//' + key
        # term.GRecorder.path_to_song_dict = term.GIni.song_dict
        # term.GBase.pool.submit(term.GRecorder.record_songs, url, dir_save, stream_suffix, key, None)
        term.GBase.pool.submit(term.GRecorder.thread_pull_song_name, url, key)
        term.GBase.pool.submit(term.GRecorder.ghetto_recorder_head, dir_save, stream_suffix, key)
        term.GBase.pool.submit(term.GRecorder.ghetto_recorder_tail, url, key, dir_save)

    def display_title(self):

        while not term.GBase.exit_app:
            for idx, var in enumerate(self.box_list):
                if var.get():
                    radio = str(self.lbl_li[idx].cget("text"))
                    self.entry_list[idx].delete(0, tk.END)
                    try:
                        title = term.GRecorder.current_song_dict[radio]
                        self.entry_list[idx].insert(0, title)
                    except Exception as ex:
                        print(ex)

            for sec in range(10):
                sleep(1)
                if term.GBase.exit_app:
                    break

    @staticmethod
    def add_server_to_data_base_ui(str_key, str_val):
        # sense of mirroring from term module is using "UIUtils.playlist_m3u(str_val) def" for auto select server
        is_playlist_server = ''
        term.GIni.ini_keys[str_key] = str_val  # append url to dictionary as value
        term.GBase.make_directory(term.GBase.radio_base_dir + '//' + str_key)
        # playlist url?
        if str_val[-4:] == '.m3u' or str_val[-4:] == '.pls':  # or url[-5:] == '.m3u8' or url[-5:] == '.xspf':
            # take first from the list
            is_playlist_server = UIUtils.playlist_m3u(str_val)
        if not is_playlist_server == '':  # update dictionary with new url
            term.GIni.ini_keys[str_key] = is_playlist_server  # append dictionary, test if it is alive
            if not term.GNet.is_server_alive(term.GIni.ini_keys[str_key], str_key):
                print('   --> playlist_server server failed, no recording')
                del term.GIni.ini_keys[str_key]
        # can not del
        term.GNet.is_server_alive(term.GIni.ini_keys[str_key], str_key)  # delete key from dict in terminal module

    def timer(self, time_left):
        combo_time = 0
        current_timer = 0
        while time_left - current_timer:
            current_timer += 1
            self.progress(current_timer, time_left)
            sleep(1)
            if self.combo_timer.get():
                combo_time = int(self.combo_timer.get()) * 3600
            if not combo_time == time_left:
                time_left = combo_time
            if term.GBase.exit_app:
                break
            if not self.record_started:
                break

        term.GBase.exit_app = True
        sleep(term.GBase.sleeper + 1)  # threads sleep too, give time for exit, reset exit_app
        term.GBase.exit_app = False
        self.btn_rec = tk.Button(master=self.btm_frame, text="Record", width=10, command=self.list_checked)
        self.btn_rec.grid(row=0, column=3, sticky='w')

    def progress(self, current_timer, max_value):
        # progressbar['value'] = 20 , is the percentage from 100, combobox returns string value
        # doing some math, p = (P * 100) / G, percent = (math.percentage value * 100) / base
        cur_percent = round((current_timer * 100) / max_value, 0)
        # print(f'cur_percent {cur_percent}  current_timer {current_timer} max {max_value}')
        self.progressbar['value'] = cur_percent
        self.update_idletasks()
        sleep(1)

    def update_scrollregion(self, event):
        self.ghetto_canvas.configure(scrollregion=self.ghetto_canvas.bbox("all"))

    def language_select(self):

        while not term.GBase.exit_app:

            lang = self.combo_lang.get()
            gl = GhettoLanguage()
            gl.process_switch_lang(lang)

            for sec in range(2):
                sleep(1)
                if term.GBase.exit_app:
                    break

    def display_info_text(self):

        while not term.GBase.exit_app:

            lang = uiw.combo_lang.get()

            if lang == 'eng':
                self.list_e = GhettoLanguage.info_eng
            if lang == 'deutsch':
                self.list_e = GhettoLanguage.info_ger

            for line in self.list_e:

                if self.record_started:
                    uiw.lbl_info.config(text=line)

                for _ in range(4):
                    if not term.GBase.exit_app:
                        sleep(1)


class GhettoLanguage(UIWindow):
    info_ger = [
        ' Die Zeilen in der Mitte sind für Suchbegriffe da.',
        ' Dein Lieblingslied im Radio gehört? Suche es.',
        ' Zuerst in einem linken Kasten den Haken setzen. "Suche"',
        ' Worte wie: Elvis Anthrax Heino Beton Kammermusik reinschreiben.',
        ' Es ist egal, ob das Wort GROSS oder klein geschrieben ist.',
        ' Das Radio spielt den Titel mit dem Wort, die Aufnahme startet und endet dann.',
        ' Bei Titelwechseln kann noch ein Teil des folgenden',
        ' Titels aufgenommen werden. Einfach löschen.',
        ' Die "Uhr" oben rechts, falls mal keine Zeit da ist "Stop" zu drücken.',
        ' Der Uhr ist wie eine Eieruhr. Nur in Stunden. Fertig! :)',
        ' Die Uhr kann man jederzeit ändern. Viel Spaß!',
    ]

    info_eng = [
        ' The lines in the middle area are used for searching phrases.',
        ' Your favorite song on air? Search the title or artist.',
        ' Please activate the corresponding box on the left. "Search"',
        ' Phrases like: Elvis Anthrax Heino concrete chamber music.',
        ' There is no rule for writing the words UPPER or lower case.',
        ' Radio station is playing a title with a search phrase! Record!',
        ' A "Timer" in the upper right corner. If you do not like ',
        ' pressing the "Stop" button yourself. One can change the value',
        ' every time. Have fun!'
    ]

    dict_eng = {'button-edit': 'Radio Editor',
                'button_ini': 'Radio List',
                'button_bbr': 'Save to ...',
                'entry_radio_dir': 'place to create a bunch of folders',
                'label_timer': 'Timer',
                'label_change_lang': 'Language',
                'label_bottom_info_start': ' Start upper left with "Radio List" and open "settings.ini" file, '
                                           'bottom left one can edit the list."',
                'label_bottom_info': ' Server down? Often under maintenance.',
                'label_bottom_info_else': ' xxxxxxxxxxexxxxxxxxx.',
                'label_search': 'Search',
                'Label_search_info': 'Search option: Artist Title',
                'entry_search_info': 'artist song (multi) (record if match): Elvis Ghetto concert'}

    dict_ger = {'button-edit': 'Radio Editor',
                'button_ini': 'Radio Liste',
                'button_bbr': 'Speichern',
                'entry_radio_dir': 'Aufnahme, Verzeichnis für die Radio Stationen',
                'label_timer': 'Uhr',
                'label_change_lang': 'Sprache',
                'label_bottom_info_start': ' Beginne oben links mit "Radio Liste", öffne "settings.ini" Datei. '
                                           'Unten links kann man die Datei ändern."',
                'label_bottom_info': ' Server nicht erreichbar? Oft nur Wartungsarbeiten.',
                'label_bottom_info_else': ' xxxxxxxxxxdxxxxxxxxx.',
                'label_search': 'Suche',
                'Label_search_info': 'Suchoption: Künstler Titel',
                'entry_search_info': 'Interpret Titel (mehrere), Treffer/Aufnahme: Elvis Ghetto Beton'}

    def __init__(self):
        super().__init__()
        self.list_e = []

    def process_switch_lang(self, arg):
        dictionary = {}
        if arg == 'eng':
            dictionary = self.dict_eng
        if arg == 'deutsch':
            dictionary = self.dict_ger

        uiw.btn_editor.configure(text=dictionary['button-edit'])
        uiw.btn_ini.configure(text=dictionary['button_ini'])
        uiw.btn_browse.configure(text=dictionary['button_bbr'])
        uiw.entry_bbr.delete(0, tk.END)
        uiw.entry_bbr.insert(0, dictionary['entry_radio_dir'])
        uiw.lbl_timer.configure(text=dictionary['label_timer'])
        uiw.lbl_lang.configure(text=dictionary['label_change_lang'])
        if uiw.start_screen:
            uiw.lbl_info.configure(text=dictionary['label_bottom_info_start'])
        if not uiw.start_screen:
            if not uiw.record_started:
                uiw.lbl_info.configure(text=dictionary['label_bottom_info'])

        uiw.lbl_search_cb.configure(text=dictionary['label_search'])
        uiw.lbl_search_entry.configure(text=dictionary['entry_search_info'])
        uiw.lbl_search_middle.configure(text=dictionary['Label_search_info'])

class UIUtils(UIWindow):

    def __init__(self, radio_dir=None, settings_path=None):
        super().__init__()

    @staticmethod
    def playlist_m3u(url):
        # returns the first server of the playlist
        try:
            read_url = term.GNet.http_pool.request('GET', url, preload_content=False)
        except Exception as ex:
            print(ex)
        else:
            file = read_url.read().decode('utf-8')

            m3u_lines = file.split("\n")
            # print(' \n    m3u_lines    ' + file)
            m3u_lines = list(filter(None, m3u_lines))  # remove empty rows
            m3u_streams = []
            for row_url in m3u_lines:
                if row_url[0:4].lower() == 'http'.lower():
                    m3u_streams.append(row_url)  # not to lower :)
                    # print(len(m3u_streams))

            if len(m3u_streams) > 1:
                print(' !!! Have more than one stream in playlist_m3u. !!! Take first stream available.')
                play_server = m3u_streams[0]
                return play_server
            if len(m3u_streams) == 1:
                # print(' One server found in playlist_m3u')
                play_server = m3u_streams[0]
                return play_server
            if len(m3u_streams) == 0:
                # print(' No http ... server found in playlist_m3u !!! -EXIT-')
                return False


if __name__ == "__main__":
    uiw = UIWindow()
    uiw.mainloop()
