import tkinter as tk
import when_was_last_build as build


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.master.title('When was last build?')
        self.create_widgets()
        self.master.after(1000, self.update_info)

    def create_widgets(self):
        self.check_lbl = tk.Label(self)
        self.check_lbl["text"] = "Check"
        self.check_lbl.pack(side="top")

        self.last_build_lbl = tk.Label(self)
        self.last_build_lbl["text"] = "Build"
        self.last_build_lbl.pack(side="top")

        self.diff_lbl = tk.Label(self)
        self.diff_lbl["text"] = "Diff"
        self.diff_lbl.pack(side="top")

        #self.quit = tk.Button(self, text="QUIT", fg="red",
        #                      command=self.master.destroy)
        #self.quit.pack(side="bottom")

    def update_info(self):
        res = None
        try:
            res = build.checkForBuild()
        except:
            self.last_build_lbl["text"] = 'No log file found'
            self.master.after(1000, self.update_info)
            # self.update_info()
        if not res:
            self.check_lbl["text"] = "Checked at {0}".format(build.datetime.now().strftime('%H:%M:%S'))
            self.last_build_lbl["text"] = "There was no builds today"
            self.diff_lbl["text"] = "Diff"
        else:
            self.check_lbl["text"] = "Checked at {0}".format(res['checkTimeStr'])
            bt = '{:%H:%M:%S}'.format(res['buildTime'])
            self.last_build_lbl["text"] = "Last build was {0} at {1}".format(res['project'], bt)
            diff = build.datetime.strptime('{0}'.format(res['checkTime'] - res['buildTime']),'%H:%M:%S.%f')
            self.diff_lbl["text"] = "Diff from now: {:%H:%M:%S}\n".format( diff )
        self.master.after(1000, self.update_info)


root = tk.Tk()
app = Application(master=root)
root.attributes('-topmost', True)
app.mainloop()
