import copy
import os
import tkinter as tk
import tkinter.ttk as ttk
from time import sleep
import webbrowser
from pygubu.widgets.pathchooserinput import PathChooserInput
import shutil
import hashlib
import string
from collections import Counter
import matplotlib.pyplot as plt
from os import walk
from PIL import Image, ImageTk

from Access_Sheets_main import access_sheets_with_report
from Access_Sheets_main import access_sheets_without_report
from Access_Sheets_main import report_data
from Audio_Conversion_main import perform_audio_analysis

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
PROJECT_UI = os.path.join(PROJECT_PATH, "FeedbackApp.ui")  # Outdated UI file, just for backup


class FeedbackApp:
    def __init__(self, root):
        # build ui
        root.title("Feedback System")
        self.main_notebook = ttk.Notebook(root)
        self.complete = False

        all_rankSums_without_reliability = []
        all_rankSums_with_reliability = []
        questions_list = []
        self.emotions_list = []

        # Creating a custom style/theme for the whole app
        mygreen = "#d2ffe2"
        myred = "#dd0212"

        style = ttk.Style()
        style.theme_create("colorful", parent="alt", settings={
            "TFrame": {"configure": {"background": "#000000"}},
            "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0], "background": "#000000"}},
            "TNotebook.Tab": {
                "configure": {"padding": [5, 1], "background": mygreen},
                "map": {"background": [("selected", myred)],
                        "expand": [("selected", [1, 1, 1, 0])]}},
            "TButton": {"configure": {"anchor": "center", "background": "#01ffc3", "foreground": "black"}},
            "TEntry": {"configure": {"background": "black", "foreground": "#00f900", "fieldbackground": "black",
                                     'insertcolor': "#39ff14"}},
            "TProgressbar": {"configure": {"background": 'green', "troughcolor": 'black', "bordercolor": 'white'}},
            "TCheckbutton": {"configure": {"background": "#000000", "foreground": "#ffd700"}},
            "TLabel": {"configure": {"background": "#000000", "foreground": '#00f900'}},
            "Custom.Treeview": {"configure": {"background": "#000000", "foreground": "#00f900", "fieldbackground": "#000000"}}})

        style.theme_use("colorful")

        def col2num(col) -> int:
            num = 0
            for c in col:
                if c in string.ascii_letters:
                    num = num * 26 + (ord(c.upper()) - ord('A')) + 1
            return num

        # Callback function to open instructional video link (instructional_link) in user's web browser
        def callback(url):
            webbrowser.open_new(url)

        self.login = ttk.Frame(self.main_notebook)

        self.instructional_link = ttk.Label(self.login, cursor="hand2")
        self.instructional_link.configure(background='#000000', font='{15} 12 {bold italic underline}',
                                          foreground="#c389fe",
                                          text='Click here for instructions')
        self.instructional_link.grid(column='0', row='8')
        self.instructional_link.bind("<Button-1>", lambda e: callback("https://drive.google.com/file/d/1eddgkjx7-jtYUij"
                                                                      "md6k0fcD2F3PzksKV/view?usp=sharing"))

        self.lbl_title = ttk.Label(self.login)
        self.lbl_title.configure(background='#000000', font='{15} 24 {bold}', foreground='#00f900',
                                 text='Feedback System Login')
        self.lbl_title.grid(column='0', pady='10', row='0')

        self.lbl_user = ttk.Label(self.login)
        self.lbl_user.configure(background='#000000', font='{1} 20 {}', foreground='#00f900', text='Username:')
        self.lbl_user.grid(column='0', pady='10', row='1')

        self.text_user = ttk.Entry(self.login)
        self.text_user.configure(font='{1} 20 {}')
        self.text_user.grid(column='0', pady='10', row='2')

        self.lbl_pwd = ttk.Label(self.login)
        self.lbl_pwd.configure(background='#000000', font='{1} 20 {}', foreground='#00f900', text='Password')
        self.lbl_pwd.grid(column='0', pady='10', row='3')

        self.text_pwd = ttk.Entry(self.login)
        self.text_pwd.configure(font='{2} 20 {}', show='•')
        self.text_pwd.grid(column='0', pady='10', row='4')

        self.lbl_confirm = ttk.Label(self.login)
        self.lbl_confirm.configure(background='#000000', font='{1} 20 {}', foreground='#00f900',
                                   text='Confirm Password:')
        self.lbl_confirm.grid(column='0', pady='10', row='5')

        self.text_confirm = ttk.Entry(self.login)
        self.text_confirm.configure(font='{1} 20 {}', show='•')
        self.text_confirm.grid(column='0', pady='10', row='6')

        # Delete function that deletes the directory
        def delete_dir(delete_path):
            try:
                shutil.rmtree(delete_path)
            except Exception as e:
                return

        # Verification check via double entry of pwd; uses SHA-256 to hash pwd and users during comparison
        def confirmation():
            actual_pwd_hash = "3730bf5fef55ffb38a958c6f9406d0ef214f53351e12a63d8163a8a0d5968209"
            actual_user_hash = "44751fcfe414e2cfe6df34ab50b0f29c2917708db13600bb739e6bfc76907542"
            user = hashlib.sha256(str(self.text_user.get()).encode("utf-8")).hexdigest()
            pwd = hashlib.sha256(str(self.text_pwd.get()).encode("utf-8")).hexdigest()
            confirm_pwd = hashlib.sha256(str(self.text_confirm.get()).encode("utf-8")).hexdigest()

            if pwd == actual_pwd_hash and confirm_pwd == actual_pwd_hash and user == actual_user_hash:
                self.main_notebook.tab(0, state="hidden")
                self.main_notebook.tab(1, state="normal")
                self.error1.configure(text='')  # Removes error message
            elif user != actual_user_hash:
                self.error1.configure(text='ERROR, incorrect username')  # Shows error message
            elif pwd != actual_pwd_hash:
                self.error1.configure(text='ERROR, incorrect password')  # Shows error message
            elif pwd == actual_pwd_hash and confirm_pwd != pwd:
                self.error1.configure(text='ERROR, verification check failed')  # Shows error message

        self.btn_login = ttk.Button(self.login, command=confirmation)
        self.btn_login.configure(text='Login', width='15')
        self.btn_login.grid(column='0', pady='15', row='7')

        self.error1 = ttk.Label(self.login)
        self.error1.configure(background='#000000', foreground='red', text='')
        self.error1.grid(column='0', row='9')

        self.login.configure(height='600', takefocus=True, width='500')
        self.login.grid(column='0', row='0', sticky='nsew')

        self.main_notebook.add(self.login, sticky='n', text='Login')

        self.choice_page = ttk.Frame(self.main_notebook)

        self.lbl_choice_title = ttk.Label(self.choice_page)
        self.lbl_choice_title.configure(font='{2} 24 {bold}', text='Pick a source for your data')
        self.lbl_choice_title.place(anchor='nw', relx='0.2', rely='0.21', x='0', y='0')

        global isaudio
        isaudio = False

        def sheets_chosen():
            global isaudio
            isaudio = False
            self.main_notebook.tab(1, state="hidden")
            self.main_notebook.tab(2, state="normal")

        self.btn_spreadsheet = ttk.Button(self.choice_page, command=sheets_chosen)
        self.sheetslogo_png = tk.PhotoImage(file='Images/sheetslogo.png')
        self.btn_spreadsheet.configure(image=self.sheetslogo_png, text='Google Spreadsheet')
        self.btn_spreadsheet.place(anchor='nw', height='250', relx='0.0', rely='0.35', width='250', x='0', y='0')

        def audio_chosen():
            global isaudio
            isaudio = True
            self.main_notebook.tab(1, state="hidden")
            self.main_notebook.tab(3, state="normal")

        self.btn_audio = ttk.Button(self.choice_page, command=audio_chosen)
        self.speakerlogo_png = tk.PhotoImage(file='Images/speakerlogo.png')
        self.btn_audio.configure(image=self.speakerlogo_png, text='.mp3 Audio File')
        self.btn_audio.place(anchor='nw', height='250', relx='0.5', rely='0.35', width='250', x='0', y='0')

        def back1():
            self.main_notebook.tab(0, state="normal")
            self.main_notebook.tab(1, state="hidden")

        self.btn_back1 = ttk.Button(self.choice_page, command=back1)
        self.btn_back1.configure(text='← Back')
        self.btn_back1.place(anchor='nw', height='40', relx='0.0', rely='0.08', x='0', y='0')

        def logout3():
            back1()

        self.btn_logout3 = ttk.Button(self.choice_page, command=logout3)
        self.btn_logout3.configure(text='Logout')
        self.btn_logout3.place(anchor='nw', height='40', relx='0.81', rely='0.08', x='0', y='0')

        self.choice_page.configure(height='500', width='500')
        self.choice_page.grid(column='0', row='0')

        self.main_notebook.add(self.choice_page, sticky='n', text='Data Source')

        self.sheets_analyzer = ttk.Frame(self.main_notebook)

        self.lbl_sheets_title = ttk.Label(self.sheets_analyzer)
        self.lbl_sheets_title.configure(font='{2} 24 {bold}', text='Sheets Analyzer')
        self.lbl_sheets_title.place(relx='0.35', rely='0.03', x='0', y='0')

        self.lbl_sheet_name = ttk.Label(self.sheets_analyzer)
        self.lbl_sheet_name.configure(text='Enter the Google Sheets title:')
        self.lbl_sheet_name.place(anchor='nw', relx='0.35', rely='0.13', x='0', y='0')

        self.text_title = tk.Text(self.sheets_analyzer)
        self.text_title.configure(height='10', width='50', background='#000000', foreground='#00f900',
                                  insertbackground="#39ff14")
        _text_ = '''Enter the Google Sheet's name and ensure view access is provided to:

anvay-971@avian-insight-318815.iam.gserviceaccount.com
'''
        self.text_title.insert('0.0', _text_)
        self.text_title.place(anchor='nw', height='100', relx='0.34', rely='0.18', width='200', x='0', y='0')

        self.lbl_column = ttk.Label(self.sheets_analyzer)
        self.lbl_column.configure(text='Enter Column Range [eg "F-H","F-F"]:')
        self.lbl_column.place(anchor='nw', relx='0.34', rely='0.43', x='0', y='0')

        self.text_column = ttk.Entry(self.sheets_analyzer)
        self.text_column.place(anchor='nw', relx='0.47', rely='0.48', width='50', x='0', y='0')

        self.message_title = tk.Message(self.sheets_analyzer)
        self.message_title.configure(text='Choose where to download the output folder by the same name as your '
                                          'Google Sheets title:', width='200', background='#000000',
                                     foreground='#00f900')
        self.message_title.place(anchor='nw', relx='0.34', rely='0.56', x='0', y='0')

        self.download_path_sheets = PathChooserInput(self.sheets_analyzer)
        self.download_path_sheets.configure(type='directory')
        self.download_path_sheets.place(anchor='nw', relx='0.33', rely='0.68', x='0', y='0')

        self.error2 = ttk.Label(self.sheets_analyzer)
        self.error2.configure(background='black', foreground='red')
        self.error2.place(anchor='nw', relx='0.32', rely='0.95', x='0', y='0')

        self.increment = 0

        title = str(self.text_title.get("1.0", 'end-1c'))

        def progress(success, isaudio):
            text_edited = "Log of executed commands and errors:"
            title = str(self.text_title.get("1.0", 'end-1c'))
            if success:
                for i in range(1, 101):
                    sleep(0.1)
                    self.progressbar.step()
                    self.lbl_progress.configure(text=str(i) + '%')
                    self.mainwindow.update()

                    if i == 10 and not isaudio:
                        text_edited += "\nAccessed spreadsheet through Google Sheets API…"
                        self.text_execution_log.configure(state='normal')
                        self.text_execution_log.delete('0.0', tk.END)
                        self.text_execution_log.insert("0.0", text_edited)
                        self.text_execution_log.configure(state='disabled')

                    elif i == 10 and isaudio:
                        text_edited += "\nConverted audio to text using speech-to-text…"
                        self.text_execution_log.configure(state='normal')
                        self.text_execution_log.delete('0.0', tk.END)
                        self.text_execution_log.insert("0.0", text_edited)
                        self.text_execution_log.configure(state='disabled')

                    if i == 20:
                        text_edited += "\nIdentified data values…"
                        self.text_execution_log.configure(state='normal')
                        self.text_execution_log.delete('0.0', tk.END)
                        self.text_execution_log.insert("0.0", "\n" + text_edited)
                        self.text_execution_log.configure(state='disabled')

                    elif i == 30:
                        text_edited += "\nProcessing data…"
                        self.text_execution_log.configure(state='normal')
                        self.text_execution_log.delete('0.0', tk.END)
                        self.text_execution_log.insert("0.0", "\n" + text_edited)
                        self.text_execution_log.configure(state='disabled')

                    elif i == 40:
                        text_edited += "\nPerforming Sentiment Analysis…"
                        self.text_execution_log.configure(state='normal')
                        self.text_execution_log.delete('0.0', tk.END)
                        self.text_execution_log.insert("0.0", "\n" + text_edited)
                        self.text_execution_log.configure(state='disabled')

                    elif i == 50:
                        text_edited += "\nIdentified emotions and polarities for each datapoint…"
                        self.text_execution_log.configure(state='normal')
                        self.text_execution_log.delete('0.0', tk.END)
                        self.text_execution_log.insert("0.0", "\n" + text_edited)
                        self.text_execution_log.configure(state='disabled')

                    elif i == 60:
                        text_edited += "\nCalculating Emotion RankSums…"
                        self.text_execution_log.configure(state='normal')
                        self.text_execution_log.delete('0.0', tk.END)
                        self.text_execution_log.insert("0.0", "\n" + text_edited)
                        self.text_execution_log.configure(state='disabled')

                    elif i == 70:
                        text_edited += "\nProducing each graph using the spreadsheet rows…"
                        self.text_execution_log.configure(state='normal')
                        self.text_execution_log.delete('0.0', tk.END)
                        self.text_execution_log.insert("0.0", "\n" + text_edited)
                        self.text_execution_log.configure(state='disabled')

                    elif i == 80:
                        text_edited += "\nProducing an aggregate graph using all rows…"
                        self.text_execution_log.configure(state='normal')
                        self.text_execution_log.delete('0.0', tk.END)
                        self.text_execution_log.insert("0.0", text_edited)
                        self.text_execution_log.configure(state='disabled')

                    elif i == 90:
                        text_edited += "\nStoring all graphs in directory" \
                                       " 'Graphs for " + title + "' in the download path provided…"
                        self.text_execution_log.configure(state='normal')
                        self.text_execution_log.delete('0.0', tk.END)
                        self.text_execution_log.insert("0.0", text_edited)
                        self.text_execution_log.configure(state='disabled')

                    elif i == 100:
                        text_edited += "\nAnalysis completed! Click 'Complete' to confirm the downloads."
                        self.text_execution_log.configure(state='normal')
                        self.text_execution_log.delete('0.0', tk.END)
                        self.text_execution_log.insert("0.0", text_edited)
                        self.text_execution_log.configure(state='disabled')
                        self.btn_complete.configure(state='normal')
                        self.btn_filters.configure(state='normal')
                        self.complete = True
                        return
            else:
                self.error2.configure(text="ERROR, no such sheet or column found")
                text_edited = '\nERROR occurred in sentiment analysis. Contact admin via email, or click "Force Stop" ' \
                              'to make changes to file title, column, audio path, or output path details'
                self.text_execution_log.configure(state='normal')
                self.text_execution_log.insert("0.0", text_edited)
                self.text_execution_log.configure(state='disabled')

        global global_success
        global_success = False

        def execution_sheets():
            global global_success
            col_check = str(self.text_column.get()) != ""
            col_range = str(self.text_column.get()).split("-")
            start_col = col_range[0]
            start_col_num = col2num(start_col)
            end_question_col = col_range[1]
            end_col_num = col2num(end_question_col)
            title = str(self.text_title.get("1.0", 'end-1c'))
            download_path = str(self.download_path_sheets.cget(key='path'))
            delete_dir(download_path + "/Graphs for " + title)

            if download_path != "" and col_check:
                self.error2.configure(text='')  # Removes error message
                all_rankSums_without_reliability.clear()
                all_rankSums_with_reliability.clear()
                questions_list.clear()
                global_success = True

                for i in range(start_col_num, end_col_num + 1):
                    result_without_reliability = access_sheets_without_report(title, i, download_path)
                    success = result_without_reliability[0]
                    global_success = success
                    if success:
                        rankSum_without_reliability = result_without_reliability[1]
                    else:
                        rankSum_without_reliability = {}
                    question_name = result_without_reliability[2]
                    all_rankSums_without_reliability.append(copy.deepcopy(rankSum_without_reliability))
                    questions_list.append(question_name)

                self.main_notebook.tab(2, state="hidden")
                self.main_notebook.tab(4, state="normal")
                progress(global_success, False)
            elif download_path == '' and not col_check:
                self.error2.configure(text='ERROR, download path should be non-empty and column range is invalid')
            elif download_path != '' and not col_check:
                self.error2.configure(text='ERROR, column range is invalid')
            else:
                self.error2.configure(text='ERROR, download path should be non-empty')

        self.btnAnalyse1 = ttk.Button(self.sheets_analyzer, command=execution_sheets)
        self.btnAnalyse1.configure(text='Analyse without Report')
        self.btnAnalyse1.place(anchor='nw', relx='0.38', rely='0.78', x='0', y='0')

        def generate_report():
            download_path = str(self.download_path_sheets.cget(key='path'))
            col_check = str(self.text_column.get()) != ""
            title_check = str(self.text_title.get("1.0", 'end-1c')) != ""
            if download_path != "" and col_check:
                self.main_notebook.tab(2, state="hidden")
                self.main_notebook.tab(5, state="normal")
                self.error2.configure(text='')  # Removes error message
            elif download_path == '' and not col_check:
                self.error2.configure(text='ERROR, download path and column range is invalid')
            elif download_path != '' and not col_check:
                self.error2.configure(text='ERROR, column range is invalid')
            else:
                self.error2.configure(text='ERROR, download path is invalid')

            if not title_check or len(str(self.text_title.get("1.0", 'end-1c'))) <= 1:
                self.error2.configure(text='ERROR, sheet name is invalid')

        self.btn_generate_report = ttk.Button(self.sheets_analyzer, command=generate_report)
        self.btn_generate_report.configure(text='Customize Reliability Report')
        self.btn_generate_report.place(anchor='nw', relx='0.35', rely='0.86', x='0', y='0')

        def back2():
            self.main_notebook.tab(1, state="normal")
            self.main_notebook.tab(2, state="hidden")

        self.btn_back2 = ttk.Button(self.sheets_analyzer, command=back2)
        self.btn_back2.configure(text='← Back')
        self.btn_back2.place(anchor='nw', height='40', relx='0.05', rely='0.04', x='0', y='0')

        def logout4():
            self.main_notebook.tab(0, state="normal")
            self.main_notebook.tab(2, state="hidden")

        self.btn_logout4 = ttk.Button(self.sheets_analyzer, command=logout4)
        self.btn_logout4.configure(text='Logout')
        self.btn_logout4.place(anchor='nw', height='40', relx='0.79', rely='0.04', x='0', y='0')

        self.sheets_analyzer.configure(height='500', width='500')
        self.sheets_analyzer.grid(column='0', row='0')

        self.main_notebook.add(self.sheets_analyzer, text='Sheets Analysis')

        self.audio_analyzer = ttk.Frame(self.main_notebook)

        self.lbl_audio_title = ttk.Label(self.audio_analyzer)
        self.lbl_audio_title.configure(font='{2} 24 {bold}', text='Audio Analyzer')
        self.lbl_audio_title.place(anchor='nw', relx='0.35', rely='0.05', x='0', y='0')

        self.lbl_audio_path = ttk.Label(self.audio_analyzer)
        self.lbl_audio_path.configure(text='Pick an audio path (.wav):')
        self.lbl_audio_path.place(anchor='nw', relx='0.36', rely='0.17', x='0', y='0')

        self.error3 = ttk.Label(self.audio_analyzer)
        self.error3.configure(background='black', foreground='red')
        self.error3.place(anchor='nw', relx='0.28', rely='0.77', x='0', y='0')

        self.audio_path = PathChooserInput(self.audio_analyzer)
        self.audio_path.configure(type='file')
        self.audio_path.place(anchor='nw', relx='0.32', rely='0.24', x='0', y='0')

        self.message_output = tk.Message(self.audio_analyzer)
        self.message_output.configure(text="Choose where to download the output folder called 'Graphs':",
                                      background='#000000', foreground='#00f900')
        self.message_output.place(anchor='nw', relx='0.38', rely='0.36', x='0', y='0')

        self.download_path_audio = PathChooserInput(self.audio_analyzer)
        self.download_path_audio.configure(type='directory')
        self.download_path_audio.place(anchor='nw', relx='0.32', rely='0.56', x='0', y='0')

        def execution_audio():
            audio_path_text = str(self.audio_path.cget(key='path'))
            download_path = str(self.download_path_audio.cget(key='path'))
            title = str(self.text_title.get("1.0", 'end-1c'))

            if download_path != "" and audio_path_text != "":
                self.main_notebook.tab(3, state="hidden")
                self.main_notebook.tab(4, state="normal")
                self.error3.configure(text='')  # Removes error message
                # Perform NLP here
                is_audio_analysed = perform_audio_analysis(audio_path_text, download_path, title)
                progress(is_audio_analysed, True)

                if is_audio_analysed:
                    self.error3.configure(text='')  # Removes error message
                else:
                    self.error3.configure(text='ERROR with audio file')

            else:
                if download_path == "" and audio_path_text == "":
                    self.error3.configure(text="ERROR, download AND audio paths don't exist")
                elif download_path == "":
                    self.error3.configure(text="ERROR, download path doesn't exist")
                elif audio_path_text == "":
                    self.error3.configure(text="ERROR, audio file doesn't exist")

        self.btnAnalyse2 = ttk.Button(self.audio_analyzer, command=execution_audio)
        self.btnAnalyse2.configure(text='Analyse')
        self.btnAnalyse2.place(anchor='nw', relx='0.45', rely='0.67', x='0', y='0')

        def back3():
            self.main_notebook.tab(1, state="normal")
            self.main_notebook.tab(3, state="hidden")

        self.btn_back3 = ttk.Button(self.audio_analyzer, command=back3)
        self.btn_back3.configure(text='← Back')
        self.btn_back3.place(anchor='nw', height='40', relx='0.05', rely='0.04', x='0', y='0')

        def logout5():
            self.main_notebook.tab(0, state="normal")
            self.main_notebook.tab(3, state="hidden")

        self.btn_logout5 = ttk.Button(self.audio_analyzer, command=logout5)
        self.btn_logout5.configure(text='Logout')
        self.btn_logout5.place(anchor='nw', height='40', relx='0.79', rely='0.04', x='0', y='0')

        self.audio_analyzer.configure(height='200', width='200')
        self.audio_analyzer.place(anchor='nw', x='0', y='0')

        self.main_notebook.add(self.audio_analyzer, text='Audio Analysis')

        self.execution_log = ttk.Frame(self.main_notebook, style='TFrame')

        self.lbl_exec_log = ttk.Label(self.execution_log)
        self.lbl_exec_log.configure(background='#000000', font='{2} 24 {bold}', foreground='#00f900',
                                    text='Execution Log')
        self.lbl_exec_log.grid(column='1', pady='10', row='0')

        self.lbl_progress = ttk.Label(self.execution_log)
        self.lbl_progress.configure(background='#000000', font='{2} 16 {bold}', foreground='#00f900')
        self.lbl_progress.grid(column='2', row='2')

        def logout3():
            self.main_notebook.tab(0, state="normal")
            self.error1.configure(text='SUCCESS!')
            self.main_notebook.tab(4, state="hidden")

        self.btn_complete = ttk.Button(self.execution_log, command=logout3)
        self.btn_complete.configure(state='disabled', text='Finish and Exit')
        self.btn_complete.grid(column='1', pady='10', row='3')

        def open_filter_page():
            global isaudio
            if isaudio:
                self.main_notebook.tab(8, state="normal")
                self.main_notebook.tab(4, state="hidden")
                submit_graph()
            else:
                self.main_notebook.tab(6, state="normal")
                self.main_notebook.tab(4, state="hidden")
            self.error1.configure(text='SUCCESS!')

        self.btn_filters = ttk.Button(self.execution_log, command=open_filter_page)
        self.btn_filters.configure(text='Finish and Explore')
        self.btn_filters.grid(column='2', pady='10', row='3')
        self.btn_filters.configure(state='disabled')

        self.progressbar = ttk.Progressbar(self.execution_log, orient="horizontal")
        self.progressbar.configure(length='350', orient='horizontal')
        self.progressbar.grid(column='1', row='2')

        def forcestop():
            global isaudio
            if not self.complete:
                title = str(self.text_title.get("1.0", 'end-1c'))
                if not isaudio:
                    d_path = str(self.download_path_sheets.cget(key='path')) + \
                                    "/Graphs for " + title
                else:
                    d_path = str(self.download_path_audio.cget(key='path')) + \
                                    "/Audio_Graph"

                delete_dir(d_path)
                self.text_execution_log.configure(state='normal')
                self.text_execution_log.delete('0.0', tk.END)
                self.text_execution_log.configure(state='disabled')
                self.main_notebook.tab(4, state="hidden")
                self.main_notebook.tab(1, state="normal")
            else:
                self.btn_force_stop.configure(state='disabled')

        self.btn_force_stop = ttk.Button(self.execution_log, command=forcestop)
        self.btn_force_stop.configure(text='Force Stop')
        self.btn_force_stop.grid(column='0', row='3')

        def logout2():
            self.main_notebook.tab(0, state="normal")
            self.main_notebook.tab(4, state="hidden")

        self.btn_logout2 = ttk.Button(self.execution_log, command=logout2)
        self.btn_logout2.configure(text='Logout')
        self.btn_logout2.grid(column='2', row='0')

        self.text_execution_log = tk.Text(self.execution_log)
        self.text_execution_log.configure(background='#000000', foreground='#00f900', height='20',
                                          insertunfocussed='hollow')
        self.text_execution_log.configure(state='disabled', width='50')
        text_init = '''Log of executed commands and errors:'''
        self.text_execution_log.configure(state='normal')
        self.text_execution_log.insert('0.0', text_init)
        self.text_execution_log.configure(state='disabled')
        self.text_execution_log.grid(column='1', row='1')

        self.execution_log.configure(height='500', takefocus=True, width='500')
        self.execution_log.grid(column='0', row='0', sticky='n')
        self.main_notebook.add(self.execution_log, sticky='n', text='Execution Log')

        self.reliability_report = ttk.Frame(self.main_notebook)

        def back4():
            self.main_notebook.tab(2, state="normal")
            self.main_notebook.tab(5, state="hidden")

        self.btn_back4 = ttk.Button(self.reliability_report, command=back4)
        self.btn_back4.configure(text='← Back')
        self.btn_back4.place(anchor='nw', height='40', relx='0.05', rely='0.04', x='0', y='0')

        def logout6():
            self.main_notebook.tab(0, state="normal")
            self.main_notebook.tab(5, state="hidden")

        self.btn_logout6 = ttk.Button(self.reliability_report, command=logout6)
        self.btn_logout6.configure(text='Logout')
        self.btn_logout6.place(anchor='nw', height='40', relx='0.79', rely='0.04', x='0', y='0')

        self.lbl_title_report = ttk.Label(self.reliability_report)
        self.lbl_title_report.configure(font='{2} 24 {bold}', text='Reliability Report')
        self.lbl_title_report.place(anchor='nw', relx='0.34', rely='0.05', x='0', y='0')

        self.lbl_start_col = ttk.Label(self.reliability_report)
        self.lbl_start_col.configure(text='From what column (char) do ratings start?')
        self.lbl_start_col.place(anchor='nw', relx='0.29', rely='0.17', x='0', y='0')

        self.text_start_col = ttk.Entry(self.reliability_report)
        self.text_start_col.place(anchor='nw', relx='0.45', rely='0.24', width='50', x='0', y='0')

        self.lbl_end_col = ttk.Label(self.reliability_report)
        self.lbl_end_col.configure(text='At what column (char) do ratings finish?')
        self.lbl_end_col.place(anchor='nw', relx='0.3', rely='0.33', x='0', y='0')

        self.text_end_col = ttk.Entry(self.reliability_report)
        self.text_end_col.place(anchor='nw', relx='0.45', rely='0.4', width='50', x='0', y='0')

        self.lbl_min_rating = ttk.Label(self.reliability_report)
        self.lbl_min_rating.configure(text='What is the smallest possible rating?')
        self.lbl_min_rating.place(anchor='nw', relx='0.32', rely='0.49', x='0', y='0')

        self.text_min_value = ttk.Entry(self.reliability_report)
        self.text_min_value.place(anchor='nw', relx='0.45', rely='0.56', width='50', x='0', y='0')

        self.lbl_max_rating = ttk.Label(self.reliability_report)
        self.lbl_max_rating.configure(text='What is the largest possible rating?')
        self.lbl_max_rating.place(anchor='nw', relx='0.33', rely='0.65', x='0', y='0')

        self.text_max_value = ttk.Entry(self.reliability_report)
        self.text_max_value.place(anchor='nw', relx='0.45', rely='0.72', width='50', x='0', y='0')

        self.is_ranked = tk.IntVar()
        self.checkbutton_is_ranked = ttk.Checkbutton(self.reliability_report, variable=self.is_ranked)
        self.checkbutton_is_ranked.configure(text='Do you want the questions to be ranked?*')
        self.checkbutton_is_ranked.place(anchor='nw', relx='0.27', rely='0.79', x='0', y='0')

        def main_graph(counter, is_with_report):
            rankSum = dict(sorted(counter.items(), key=lambda item: item[1]))
            fig, ax1 = plt.subplots()
            ax1.bar(rankSum.keys(), rankSum.values())
            fig.autofmt_xdate()
            download_path = str(self.download_path_sheets.cget(key='path'))
            file_name = str(self.text_title.get("1.0", 'end-1c'))

            path = download_path + "/Graphs for " + file_name + "/"
            if not os.path.exists(path):
                os.makedirs(path)

            plt.title('Aggregate relative frequencies (RankSums)')
            plt.xlabel('Emotion')
            plt.ylabel('RankSum Value (in ascending order)')
            if is_with_report:
                fig.savefig(path + "/SummativeAggregateFigure_With_Report.png")
            else:
                fig.savefig(path + "/SummativeAggregateFigure_Without_Report.png")

        def submit_report():
            start_col = str(self.text_start_col.get())
            end_col = str(self.text_end_col.get())
            min_value = float(self.text_min_value.get())
            max_value = float(self.text_max_value.get())
            is_ranked = int(self.is_ranked.get())
            col_range = str(self.text_column.get()).split("-")
            start_question_col = col_range[0]
            start_col_num = col2num(start_question_col)
            end_question_col = col_range[1]
            end_col_num = col2num(end_question_col)
            file_name = str(self.text_title.get("1.0", 'end-1c'))
            download_path = str(self.download_path_sheets.cget(key='path'))
            success1 = True
            success2 = True
            all_rankSums_without_reliability.clear()
            all_rankSums_with_reliability.clear()

            for i in range(start_col_num, end_col_num + 1):
                if success1 and success2:
                    reliability = report_data(file_name, start_col, end_col, min_value, max_value, is_ranked, i,
                                              download_path)
                    if is_ranked:
                        result_with_reliability = access_sheets_with_report(file_name, i, download_path, is_ranked,
                                                                            reliability)
                        success1 = result_with_reliability[0]
                        rankSum_with_reliability = result_with_reliability[1]
                        question_name = result_with_reliability[2]
                        all_rankSums_with_reliability.append(copy.deepcopy(rankSum_with_reliability))
                        questions_list.append(question_name)

                    result_without_reliability = access_sheets_without_report(file_name, i, download_path)
                    success2 = result_without_reliability[0]
                    rankSum_without_reliability = result_without_reliability[1]
                    all_rankSums_without_reliability.append(copy.deepcopy(rankSum_without_reliability))

            if success1 and success2:
                counter_without_reliability = {}
                counter_with_reliability = {}

                for dictionary in all_rankSums_without_reliability:
                    a_counter = Counter(counter_without_reliability)
                    b_counter = Counter(dictionary)
                    add_dict = a_counter + b_counter
                    counter_without_reliability = dict(add_dict)
                main_graph(counter_without_reliability, False)

                for dictionary in all_rankSums_with_reliability:
                    a_counter = Counter(counter_with_reliability)
                    b_counter = Counter(dictionary)
                    add_dict = a_counter + b_counter
                    counter_with_reliability = dict(add_dict)
                main_graph(counter_with_reliability, True)
                temp_emotions_list = list(counter_with_reliability.keys())
                self.emotions_list = copy.deepcopy(temp_emotions_list)

                self.main_notebook.tab(4, state="normal")
                self.main_notebook.tab(5, state="hidden")
                progress(True, False)
            else:
                progress(False, False)

        self.btn_submit_report = ttk.Button(self.reliability_report, command=submit_report)
        self.btn_submit_report.configure(text='Submit')
        self.btn_submit_report.place(anchor='nw', relx='0.45', rely='0.86', x='0', y='0')

        self.lbl_rank_instructions_link = ttk.Label(self.reliability_report, cursor="hand2")
        self.lbl_rank_instructions_link.configure(font='{2} 14 {bold italic underline}',
                                                  text='* What is the question rank system?', foreground="#c389fe")
        self.lbl_rank_instructions_link.place(anchor='nw', relx='0.29', rely='0.93', x='0', y='0')
        # TODO: Replace the link below to an instructional video about how the question ranks work
        self.lbl_rank_instructions_link.bind("<Button-1>",
                                             lambda e: callback("https://drive.google.com/file/d/1eddgkjx7-jtYUij"
                                                                "md6k0fcD2F3PzksKV/view?usp=sharing"))

        self.reliability_report.configure(height='200', width='200')
        self.reliability_report.pack(side='top')

        self.main_notebook.add(self.reliability_report, text='Reliability Report')

        self.filtered_questions = ttk.Frame(self.main_notebook)

        self.lbl_emotion_filters = ttk.Label(self.filtered_questions)
        self.lbl_emotion_filters.configure(font='{2} 24 {bold}', text='Emotion Filters')
        self.lbl_emotion_filters.place(anchor='nw', relx='0.37', rely='0.05', x='0', y='0')

        def back5():
            self.main_notebook.tab(4, state="normal")
            self.main_notebook.tab(6, state="hidden")

        self.btn_back5 = ttk.Button(self.filtered_questions, command=back5)
        self.btn_back5.configure(text='← Back')
        self.btn_back5.place(anchor='nw', height='40', relx='0.05', rely='0.04', x='0', y='0')

        def logout7():
            self.main_notebook.tab(0, state="normal")
            self.main_notebook.tab(6, state="hidden")

        self.btn_logout7 = ttk.Button(self.filtered_questions, command=logout7)
        self.btn_logout7.configure(text='Logout')
        self.btn_logout7.place(anchor='nw', height='40', relx='0.79', rely='0.04', x='0', y='0')

        self.table = ttk.Treeview(self.filtered_questions, style="Custom.Treeview")
        self.table.place(anchor='nw', height='300', relx='0.05', rely='0.31', width='500', x='0', y='0')

        def treeview_sort_column(tv, col, reverse):
            l = [(tv.set(k, col), k) for k in tv.get_children('')]
            l.sort(reverse=reverse)

            # rearrange items in sorted positions
            for index, (val, k) in enumerate(l):
                tv.move(k, '', index)

            # reverse sort next time
            tv.heading(col, command=lambda: \
                treeview_sort_column(tv, col, not reverse))

        global count
        count = 0
        def search(e):
            # TODO: Sorting stuff using ttk TreeView
            global count
            self.table.delete(*self.table.get_children())
            if self.cbox_type.get() == "Questions":
                self.table['columns'] = ("Emotion", "Ranksum with Reliability", "Ranksum without Reliability")
                self.table.column("#0", width=0, stretch=tk.NO)
                self.table.column("Emotion", minwidth=0, width=100, anchor=tk.CENTER)
                self.table.column("Ranksum with Reliability", minwidth=0, width=200, anchor=tk.CENTER)
                self.table.column("Ranksum without Reliability", minwidth=0, width=200, anchor=tk.CENTER)

                self.table.heading("#0", text="", anchor=tk.W)
                self.table.heading("Emotion", text="Emotion", anchor=tk.CENTER, command=lambda: \
                    treeview_sort_column(self.table, "Emotion", False))
                self.table.heading("Ranksum with Reliability", text="Ranksum with Reliability", anchor=tk.CENTER,
                                   command=lambda: \
                                       treeview_sort_column(self.table, "Ranksum with Reliability", False))
                self.table.heading("Ranksum without Reliability", text="Ranksum without Reliability", anchor=tk.CENTER,
                                   command=lambda: \
                                       treeview_sort_column(self.table, "Ranksum without Reliability", False))

                for i in range(len(questions_list)):
                    if questions_list[i] == self.cbox_choice.get():
                        for emotion1, ranksum_with_reliability in all_rankSums_with_reliability[i].items():
                            for emotion2, ranksum_without_reliability in all_rankSums_without_reliability[i].items():
                                if emotion1 == emotion2:
                                    self.table.insert(parent='', index='end', iid=count, text='', values=(
                                    emotion1, ranksum_with_reliability, ranksum_without_reliability))
                                    count += 1
                                    break

            elif self.cbox_type.get() == "Emotions":
                self.table['columns'] = ("Question", "Ranksum with Reliability", "Ranksum without Reliability")
                self.table.column("#0", width=0, stretch=tk.NO)
                self.table.column("Question", minwidth=0, width=100, anchor=tk.CENTER)
                self.table.column("Ranksum with Reliability", minwidth=0, width=200, anchor=tk.CENTER)
                self.table.column("Ranksum without Reliability", minwidth=0, width=200, anchor=tk.CENTER)

                self.table.heading("#0", text="", anchor=tk.W)
                self.table.heading("Question", text="Question", anchor=tk.CENTER, command=lambda: \
                    treeview_sort_column(self.table, "Question", False))
                self.table.heading("Ranksum with Reliability", text="Ranksum with Reliability", anchor=tk.CENTER,
                                   command=lambda: \
                                       treeview_sort_column(self.table, "Ranksum with Reliability", False))
                self.table.heading("Ranksum without Reliability", text="Ranksum without Reliability", anchor=tk.CENTER,
                                   command=lambda: \
                                       treeview_sort_column(self.table, "Ranksum without Reliability", False))

                for i in range(len(all_rankSums_with_reliability)):
                    for emotion1, ranksum_with_reliability in all_rankSums_with_reliability[i].items():
                        if emotion1 == self.cbox_choice.get():
                            for emotion2, ranksum_without_reliability in all_rankSums_without_reliability[i].items():
                                if emotion2 == self.cbox_choice.get():
                                    self.table.insert(parent='', index='end', iid=count, text='', values=(
                                        questions_list[i], ranksum_with_reliability, ranksum_without_reliability))
                                    count += 1
                                    break

        def update_options(e):
            if self.cbox_type.get() == "Questions":
                self.cbox_choice.config(value=questions_list)
            if self.cbox_type.get() == "Emotions":
                self.cbox_choice.config(value=self.emotions_list)

        type_options = ["Questions", "Emotions"]

        self.cbox_type = ttk.Combobox(self.filtered_questions, value=type_options)
        self.cbox_type.current(0)
        self.cbox_type.place(anchor='nw', relx='0.05', rely='0.23', width='100', x='0', y='0')
        self.cbox_type.bind("<<ComboboxSelected>>", update_options)

        self.lbl_type = ttk.Label(self.filtered_questions)
        self.lbl_type.configure(text='Sort by:')
        self.lbl_type.place(anchor='nw', relx='0.09', rely='0.17', x='0', y='0')

        self.lbl_choice = ttk.Label(self.filtered_questions)
        self.lbl_choice.configure(text='Which emotion/question?')
        self.lbl_choice.place(anchor='nw', relx='0.38', rely='0.17', x='0', y='0')

        self.cbox_choice = ttk.Combobox(self.filtered_questions, value=[" "])
        self.cbox_choice.current(0)
        self.cbox_choice.place(anchor='nw', relx='0.28', rely='0.23', width='300', x='0', y='0')
        self.cbox_choice.bind("<<ComboboxSelected>>", search)

        def to_main_menu():
            self.main_notebook.tab(7, state="normal")
            self.main_notebook.tab(6, state="hidden")

            is_ranked = int(self.is_ranked.get())
            if is_ranked:
                self.cb_reliability.config(value=["Only Non-Reliability", "Only Reliability"])
            else:
                self.cb_reliability.config(value=["Only Non-Reliability"])

            labeled_qs = ["Overall"]
            c = 1
            for i in questions_list:
                labeled_qs.append("Q" + str(c) + ": " + i)
                c += 1
            self.cb_questions.config(value=labeled_qs)

        self.btn_main_menu = ttk.Button(self.filtered_questions, command=to_main_menu)
        self.btn_main_menu.configure(text='Main Menu')
        self.btn_main_menu.place(anchor='nw', relx='0.83', rely='0.23', x='0', y='0')

        self.filtered_questions.configure(height='200', width='200')
        self.filtered_questions.place(anchor='nw', x='0', y='0')

        self.main_notebook.add(self.filtered_questions, text='Emotion Filters')


        self.main_menu = ttk.Frame(self.main_notebook)

        self.lbl_main_menu = ttk.Label(self.main_menu)
        self.lbl_main_menu.configure(font='{2} 24 {bold}', text='Main Menu')
        self.lbl_main_menu.place(anchor='nw', relx='0.37', rely='0.05', x='0', y='0')

        def back6():
            self.main_notebook.tab(6, state="normal")
            self.main_notebook.tab(7, state="hidden")

        self.btn_back6 = ttk.Button(self.main_menu, command=back6)
        self.btn_back6.configure(text='← Back')
        self.btn_back6.place(anchor='nw', height='40', relx='0.05', rely='0.04', x='0', y='0')

        def logout8():
            self.main_notebook.tab(0, state="normal")
            self.main_notebook.tab(7, state="hidden")

        self.btn_logout8 = ttk.Button(self.main_menu, command=logout8)
        self.btn_logout8.configure(text='Logout')
        self.btn_logout8.place(anchor='nw', height='40', relx='0.79', rely='0.04', x='0', y='0')

        self.cb_reliability = ttk.Combobox(self.main_menu, value=[" "])
        self.cb_reliability.place(anchor='nw', relx='0.33', rely='0.33', x='0', y='0')

        self.cb_questions = ttk.Combobox(self.main_menu, value=[" "])
        self.cb_questions.place(anchor='nw', relx='0.27', rely='0.59', width='300', x='0', y='0')

        self.lbl_rel = ttk.Label(self.main_menu)
        self.lbl_rel.configure(font='{2} 18 {bold}', text='Include Reliability?')
        self.lbl_rel.place(anchor='nw', relx='0.35', rely='0.22', x='0', y='0')

        self.lbl_questions = ttk.Label(self.main_menu)
        self.lbl_questions.configure(font='{2} 18 {bold}', text='Which question to inspect?')
        self.lbl_questions.place(anchor='nw', relx='0.31', rely='0.48', x='0', y='0')

        global relstatus
        global question
        global filelist
        global gindex
        global relpath

        def show_graph():
            global gindex
            global filelist
            photo = Image.open(filelist[gindex])
            resized = photo.resize((400, 250), Image.ANTIALIAS)
            converted = ImageTk.PhotoImage(resized)
            self.current_graph = ttk.Label(self.graph_viewer, image=converted)
            self.current_graph.place(height='250', relx='0.18', rely='0.28', width='400', x='0', y='0')
            self.current_graph.image = converted

        def submit_graph():
            download_path = str(self.download_path_sheets.cget(key='path'))
            file_name = str(self.text_title.get("1.0", 'end-1c'))
            global relstatus
            global question
            global filelist
            global gindex
            global relpath
            global isaudio
            relpath = ""
            gindex = 0

            relstatus = str(self.cb_reliability.get())
            question = str(self.cb_questions.get())
            qnum = "Overall"
            qsplit = question.split(": ", 1)

            if not isaudio:
                if question != "Overall":
                    qnum = qsplit[0]
                    question = qsplit[1]
                    self.btn_aggregate.configure(state="normal")
                    if relstatus == "Only Reliability":
                        self.btn_scatter.configure(state="normal")
                        relpath = "Graphs accounting for Reliability/IndividualData_With_Report"
                    elif relstatus == "Only Non-Reliability":
                        self.btn_scatter.configure(state="disabled")
                        relpath = "Graphs not accounting for Reliability/IndividualData_Without_Report"

                    filelist = next(walk(download_path + "/Graphs for " + file_name + "/" + question + "/" + relpath), (None, None, []))[2]
                    templist = []
                    for x in filelist:
                        templist.append(download_path + "/Graphs for " + file_name + "/" + question + "/" + relpath + "/" + x)
                    filelist = templist

                    self.btn_individual.configure(state="normal")
                    self.btn_prev_graph.configure(state="normal")
                    self.btn_next_graph.configure(state="normal")
                else:
                    questionpath = ""
                    if relstatus == "Only Reliability":
                        questionpath = "SummativeAggregateFigure_With_Report.png"
                    elif relstatus == "Only Non-Reliability":
                        questionpath = "SummativeAggregateFigure_Without_Report.png"

                    self.btn_aggregate.configure(state="disabled")
                    self.btn_scatter.configure(state="disabled")
                    self.btn_individual.configure(state="disabled")
                    self.btn_prev_graph.configure(state="disabled")
                    self.btn_next_graph.configure(state="disabled")

                    filelist = [download_path + "/Graphs for " + file_name + "/" + questionpath]
            else:
                audio_download_path = str(self.download_path_audio.cget(key='path'))
                qnum = "Audio"
                gindex = 0
                filelist = [audio_download_path + "/Audio_Graph/FigureAggregate.png"]
                self.btn_aggregate.configure(state="disabled")
                self.btn_scatter.configure(state="disabled")
                self.btn_individual.configure(state="disabled")
                self.btn_prev_graph.configure(state="disabled")
                self.btn_next_graph.configure(state="disabled")

            self.lbl_graph_viewer.configure(text='Graph Viewer: ' + qnum)

            show_graph()

            self.main_notebook.tab(8, state="normal")
            self.main_notebook.tab(7, state="hidden")

        self.btn_submit_graph = ttk.Button(self.main_menu, command=submit_graph)
        self.btn_submit_graph.configure(text='View Graphs')
        self.btn_submit_graph.place(anchor='nw', height='40', relx='0.42', rely='0.74', x='0', y='0')

        self.main_menu.configure(height='200', width='200')
        self.main_menu.place(anchor='nw', x='0', y='0')

        self.main_notebook.add(self.main_menu, text='Main Menu')


        self.graph_viewer = ttk.Frame(self.main_notebook)

        self.lbl_graph_viewer = ttk.Label(self.graph_viewer)
        self.lbl_graph_viewer.configure(font='{2} 24 {bold}', text='Graph Viewer: ')
        self.lbl_graph_viewer.place(anchor='nw', relx='0.36', rely='0.05', x='0', y='0')

        def back7():
            global isaudio
            if isaudio:
                self.main_notebook.tab(4, state="normal")
            else:
                self.main_notebook.tab(7, state="normal")
            self.main_notebook.tab(8, state="hidden")

        self.btn_back7 = ttk.Button(self.graph_viewer, command=back7)
        self.btn_back7.configure(text='← Back')
        self.btn_back7.place(anchor='nw', height='40', relx='0.05', rely='0.04', x='0', y='0')

        def logout9():
            self.main_notebook.tab(0, state="normal")
            self.main_notebook.tab(8, state="hidden")

        self.btn_logout9 = ttk.Button(self.graph_viewer, command=logout9)
        self.btn_logout9.configure(text='Logout')
        self.btn_logout9.place(anchor='nw', height='40', relx='0.79', rely='0.04', x='0', y='0')

        def prev_graph():
            global gindex
            self.btn_next_graph.configure(state="normal")
            if gindex <= 1:
                self.btn_prev_graph.configure(state="disabled")
                gindex -= 1
            else:
                self.btn_prev_graph.configure(state="normal")
                gindex -= 1
            show_graph()

        def next_graph():
            global gindex
            self.btn_prev_graph.configure(state="normal")
            if gindex >= len(filelist)-1:
                self.btn_next_graph.configure(state="disabled")
                gindex += 1
            else:
                self.btn_next_graph.configure(state="normal")
                gindex += 1
            show_graph()

        self.btn_prev_graph = ttk.Button(self.graph_viewer, command=prev_graph)
        self.btn_prev_graph.configure(text='⏮ Previous')
        self.btn_prev_graph.place(anchor='nw', height='40', relx='0.05', rely='0.86', x='0', y='0')

        self.btn_next_graph = ttk.Button(self.graph_viewer, command=next_graph)
        self.btn_next_graph.configure(text='Next ⏭')
        self.btn_next_graph.place(anchor='nw', height='40', relx='0.79', rely='0.86', x='0', y='0')

        def show_aggregate():
            global gindex
            global filelist
            global relpath
            global question
            gindex = 0

            download_path = str(self.download_path_sheets.cget(key='path'))
            file_name = str(self.text_title.get("1.0", 'end-1c'))
            self.btn_prev_graph.configure(state="disabled")
            self.btn_next_graph.configure(state="disabled")

            if relstatus == "Only Reliability":
                filelist = [download_path + "/Graphs for " + file_name + "/" + question + "/" + relpath.split("/", 1)[0] + "/AggregateFigure_With_Report.png"]
            elif relstatus == "Only Non-Reliability":
                filelist = [download_path + "/Graphs for " + file_name + "/" + question + "/" + relpath.split("/", 1)[0] + "/AggregateFigure_Without_Report.png"]

            show_graph()

        def show_scatter():
            global gindex
            global filelist
            gindex = 0

            download_path = str(self.download_path_sheets.cget(key='path'))
            file_name = str(self.text_title.get("1.0", 'end-1c'))
            self.btn_prev_graph.configure(state="disabled")
            self.btn_next_graph.configure(state="disabled")

            filelist = [download_path + "/Graphs for " + file_name + "/" + question + "/Graphs accounting for Reliability/"
                                                                                      "Scatter_Plot_of_Numerical_vs_Textual_Positivity.png"]

            show_graph()

        self.btn_aggregate = ttk.Button(self.graph_viewer, command=show_aggregate)
        self.btn_aggregate.configure(text='Aggregate Graph')
        self.btn_aggregate.place(anchor='nw', relx='0.15', rely='0.18', x='0', y='0')

        self.btn_scatter = ttk.Button(self.graph_viewer, command=show_scatter)
        self.btn_scatter.configure(text='Scatter Graph')
        self.btn_scatter.place(anchor='nw', relx='0.41', rely='0.18', x='0', y='0')

        def show_individual():
            global gindex
            global filelist
            gindex = 0

            download_path = str(self.download_path_sheets.cget(key='path'))
            file_name = str(self.text_title.get("1.0", 'end-1c'))
            self.btn_prev_graph.configure(state="normal")
            self.btn_next_graph.configure(state="normal")

            filelist = next(walk(download_path + "/Graphs for " + file_name + "/" + question + "/" + relpath), (None, None, []))[2]
            templist = []
            for x in filelist:
                templist.append(download_path + "/Graphs for " + file_name + "/" + question + "/" + relpath + "/" + x)
            filelist = templist

            show_graph()

        self.btn_individual = ttk.Button(self.graph_viewer, command=show_individual)
        self.btn_individual.configure(text='Individual Graphs')
        self.btn_individual.place(anchor='nw', relx='0.64', rely='0.18', x='0', y='0')

        self.graph_viewer.configure(height='200', width='200')
        self.graph_viewer.place(anchor='nw', x='0', y='0')

        self.main_notebook.add(self.graph_viewer, text='Graph Viewer')


        self.main_notebook.configure(height='450', takefocus=True, width='600')
        self.main_notebook.grid(column='0', row='0')

        # Main widget
        self.mainwindow = self.main_notebook

        # Set tab1 as disabled and tab2 as hidden
        self.main_notebook.tab(1, state="hidden")
        self.main_notebook.tab(2, state="hidden")
        self.main_notebook.tab(3, state="hidden")
        self.main_notebook.tab(4, state="hidden")
        self.main_notebook.tab(5, state="hidden")
        self.main_notebook.tab(6, state="hidden")
        self.main_notebook.tab(7, state="hidden")
        self.main_notebook.tab(8, state="hidden")

    def run(self):
        self.mainwindow.mainloop()


if __name__ == '__main__':
    root = tk.Tk()
    app = FeedbackApp(root)
    root.mainloop()
