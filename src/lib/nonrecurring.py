import os
import yaml as yml
import datetime as dt
import colorama as cr
from graphviz import Digraph


class data_handling:
    def __init__(self):
        cr.init(autoreset=True)
        self.data_dir_path = "src/data/nonrecurring"
        self.lib_dir_path = "src/lib"
        self.print_txt_path = os.path.join(self.lib_dir_path, "print.txt")

    def c_t(self):
        """
        clear terminal
        """
        os.system("clear")

    def dir_tree(self):
        """
        print the file tree
        """
        os.system(
            f"tree -q -L 2 '{self.data_dir_path}' | grep -Ev '[0-9]+ director(?:y|ies), [0-9]+ files?'"
        )

    def load_yml(self):
        """
        load .yml files
        """
        if self.data_path.endswith(".yml"):
            with open(self.data_path, "r") as f:
                self.data = yml.safe_load(f)
        else:
            self.data = []

    def save_yml(self):
        """
        save .yml files
        """
        with open(self.data_path, "w") as f:
            yml.safe_dump(self.data, f)

    def load_txt(self):
        """
        load .txt files
        """
        with open(self.print_txt_path, "r") as file:
            self.txt = file.read()

    def t_o(self, choice, clear=True, tree=False):
        """
        terminal output

        extract text to print from .txt file
        """
        if clear:
            self.c_t()
        if tree:
            self.dir_tree()
        scts = self.txt.split("===")
        for sct in scts:
            sct_strip = sct.strip()
            if sct_strip.startswith("#"):
                lines = sct_strip.split("\n")
                title_line = lines[0].strip("#").strip()
                if title_line == choice:
                    self.to_print = "\n".join(lines[1:]).strip()
                    print(self.to_print)
                    self.u_input = input()

    def timedeltas(self):
        """
        handle absolute dates and update relative dates
        """
        self.today = dt.date.today()
        self.yesterday = self.today - dt.timedelta(days=1)
        self.tomorrow = self.today + dt.timedelta(days=1)
        # self.due_rel = self.due_abs - self.today

    def chrono_print(self):
        self.data = sorted(self.data, key=lambda x: x["deadline"], reverse=False)
        for n, it in enumerate(self.data):
            t = it["task"]
            s = it["status"]
            dl = it["deadline"]
            dl = dt.datetime.strptime(dl, "%Y-%m-%d").strftime("%d %B %Y")

            r = cr.Fore.RESET
            c = r
            if s == "to do":
                c = cr.Fore.MAGENTA
            if s == "done":
                c = cr.Fore.CYAN

            print(f"{n + 1} ~ {c}{t}{r} ~ {c}{dl}{r} ~ {c}{s}{r}")
        print("\n")

    def v_1_chrono(self):
        pi = int(self.u_input) - 1
        self.data_path = os.path.join(self.data_dir_path, self.yml_f[pi])
        self.c_t()
        self.load_yml()
        self.chrono_print()

    def v_a_chrono(self):
        self.c_t()
        self.data_expand = []
        for p in os.listdir(self.data_dir_path):
            self.data_path = os.path.join(self.data_dir_path, p)
            self.load_yml()
            self.data_expand.append(self.data)

        self.data = [item for sublist in self.data_expand for item in sublist]
        self.chrono_print()

    def add_task(self, new_proj=False):
        """
        new entry in an existing .yml file
        """
        if not new_proj:
            pi = int(self.u_input) - 1
            self.data_path = os.path.join(self.data_dir_path, self.yml_f[pi])
        self.load_yml()
        while True:
            t = input("task\n")
            self.due_abs = input("deadline today [] or on date [yymmdd]\n")
            if self.due_abs == "":
                self.due_abs = dt.date.today().strftime("%Y-%m-%d")
            else:
                self.due_abs = dt.datetime.strptime(self.due_abs, "%y%m%d").strftime(
                    "%Y-%m-%d"
                )
            s = "to do"
            self.data.append(
                {
                    "task": t,
                    "status": s,
                    "deadline": self.due_abs,
                    # "due": self.due_rel,
                }
            )
            self.u_input = input("add [m]ore or [d]one ")
            if self.u_input == "m":
                continue
            if self.u_input == "d":
                self.save_yml()
                break

    def add_project(self):
        """
        new .yml file
        """
        self.u_input = input("project\n")
        pn = self.u_input + ".yml"
        self.data_path = os.path.join(self.data_dir_path, pn)
        self.data = []
        self.save_yml()

    def rename_project(self):
        old = self.u_input + ".yml"
        old = os.path.join(self.data_dir_path, old)
        new = input("rename to\n")
        new = new + ".yml"
        new = os.path.join(self.data_dir_path, new)
        os.rename(old, new)

    def print_projects(self, filter=False):
        self.c_t()
        self.yml_f = [f for f in os.listdir(self.data_dir_path) if f.endswith(".yml")]
        if filter:
            """
            filter out empty .yml files
            """
            non_empty = []
            for p in self.yml_f:
                with open(os.path.join(self.data_dir_path, p), "r") as f:
                    contents = yml.safe_load(f)
                if bool(contents):
                    non_empty.append(p)
            self.yml_f = non_empty
        for i, f in enumerate(self.yml_f, start=1):
            print(f"{i} {f}")

    def edit_task(self):
        self.v_1_chrono()
        self.t_o("4", clear=False)
        ti = int(int(self.u_input)) - 1
        t = self.data[ti]
        k = input("change [t]ask, [d]eadline or [s]tatus\n")
        if k == "t":
            k = "task"
        if k == "d":
            k = "deadline"
        if k == "s":
            k = "status"
        new_val = t[k]
        if k == "task":
            new_val = input("new task name\n")
        if k == "deadline":
            new_val = input("new deadline today [] or on date [yymmdd]\n")
            if new_val == "":
                new_val = dt.date.today().strftime("%Y-%m-%d")
            else:
                new_val = dt.datetime.strptime(new_val, "%y%m%d").strftime("%Y-%m-%d")
        if k == "status":
            new_val = input("new status\n")
        t[k] = new_val
        self.data[ti] = t
        self.save_yml()

    def delete_task(self):
        self.v_1_chrono()
        self.t_o("4", clear=False)
        ti = int(int(self.u_input)) - 1
        del self.data[ti]
        self.save_yml()

    def delete_project(self):
        pi = int(self.u_input) - 1
        self.data_path = os.path.join(self.data_dir_path, self.yml_f[pi])
        os.remove(self.data_path)

    def menu(self):
        """
        navigation
        """
        self.c_t()
        self.dir_tree()
        self.load_txt()

        while True:

            self.t_o("1", clear=False)

            if self.u_input == "v":
                self.t_o("2")
                chrono = False
                graphic = False
                if self.u_input == "c":
                    chrono = True
                if self.u_input == "g":
                    graphic = True
                self.t_o("3")
                if chrono & (self.u_input == "w"):
                    self.print_projects()
                    self.t_o("4", clear=False)
                    self.v_1_chrono()
                if chrono & (self.u_input == "a"):
                    self.v_a_chrono()
                if graphic & (self.u_input == "w"):
                    pass
                if graphic & (self.u_input == "a"):
                    pass
                break

            if self.u_input == "e":
                self.t_o("5")
                if self.u_input == "a":
                    self.t_o("6")
                    if self.u_input == "n":
                        self.add_project()
                        self.add_task(new_proj=True)
                    if self.u_input == "e":
                        self.print_projects()
                        self.t_o("4", clear=False)
                        self.add_task()
                    break
                if self.u_input == "c":
                    self.t_o("7")
                    if self.u_input == "p":
                        self.print_projects()
                        self.t_o("4", clear=False)
                        self.rename_project()
                    if self.u_input == "t":
                        self.print_projects(filter=True)
                        self.t_o("4", clear=False)
                        self.edit_task()
                if self.u_input == "d":
                    self.t_o("7")
                    if self.u_input == "p":
                        self.print_projects()
                        self.t_o("4", clear=False)
                        self.delete_project()
                    if self.u_input == "t":
                        self.print_projects(filter=True)
                        self.t_o("4", clear=False)
                        self.delete_task()
                break

            break


class graphviz_auto:
    def __init__(
        self,
        filename: str = "digraph_00.gv",
        fileformat: str = "pdf",  # 'png', 'svg'
    ):
        self.digraph = Digraph(
            "G",
            format=fileformat,
            filename=filename,
        )
