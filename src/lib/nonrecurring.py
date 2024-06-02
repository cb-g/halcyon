import os
import yaml as yml
import datetime as dt
import colorama as cr
from graphviz import Digraph
from typing import List, Dict


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

    def t_o(self, choice, clear=True, tree=False, graphic=False):
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
        if graphic:
            return int(self.u_input) - 1
        else:
            return None

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


class graphviz_auto:
    def __init__(
        self,
        max_char: int = 20,
        filepath: str = "src/viz",
        data_dir_path: str = "src/data/nonrecurring",
        filename: str = "digraph_00.gv",
        # fileformat: str = "pdf",
        fileformat: str = "png",
        # fileformat: str = "svg",
    ):
        self.filepath = filepath
        self.max_line_len = max_char  # linebreak
        self.digraph = Digraph(
            "G",
            format=fileformat,
            filename=filename,
        )
        self.fileformat = fileformat
        self.filename = filename
        self.data_dir_path = data_dir_path

    def autolinebreak(self, string: str) -> str:
        x = self.max_line_len
        lst = string.split()
        line = ""
        str_final = ""
        for word in lst:
            if len(line + " " + word) <= x:
                str_final += word + " "
                line += word + " "
            else:
                str_final += "\n" + word + " "
                line = word + " "
        return str_final

    def design_node(self, choose_node_design: str = "node_design_0"):
        """
        shape: https://graphviz.gitlab.io/doc/info/shapes.html#polygon
        style: https://graphviz.gitlab.io/doc/info/shapes.html#styles-for-nodes
        color: https://graphviz.gitlab.io/doc/info/colors.html#x11
        fontname: https://graphviz.gitlab.io/faq/font/#default-fonts-and-postscript-fonts
        """

        node_design = {
            "shape": "rectangle",
            "style": "rounded",
            "color": "darkgray",
            "fontcolor": "black",
            # "fontname": "Times-Roman",
            "fontname": "Symbol",
        }

        if choose_node_design == "node_design_red":
            node_design = {
                "shape": "rectangle",
                "style": "rounded",
                "color": "firebrick",
                "fontcolor": "black",
                # "fontname": "Times-Roman",
                "fontname": "Symbol",
            }
        if choose_node_design == "node_design_green":
            node_design = {
                "shape": "rectangle",
                "style": "rounded",
                "color": "darkgreen",
                "fontcolor": "white",
                # "fontname": "Times-Roman",
                "fontname": "Symbol",
            }

        self.digraph.attr(
            "node",
            shape=node_design["shape"],
            style=node_design["style"],
            color=node_design["color"],
            fontcolor=node_design["fontcolor"],
            fontname=node_design["fontname"],
        )

    def design_edge(self):
        """
        color: https://graphviz.gitlab.io/doc/info/colors.html#x11
        arrowhead: https://graphviz.gitlab.io/doc/info/arrows.html#primitive-shapes
        """
        edge_design = {
            "color": "darkgray",
            "arrowhead": "vee",
        }

        self.digraph.attr(
            "edge", color=edge_design["color"], arrowhead=edge_design["arrowhead"]
        )

    def make_node(
        self, node_content: str = "empty", choose_node_design: str = "node_design_0"
    ):
        self.design_node(choose_node_design)
        self.digraph.node(self.autolinebreak(node_content))

    def make_nodes(self, *args, choose_node_design: str = "node_design_0"):
        for i in range(len(args)):
            self.make_node(node_content=args[i], choose_node_design=choose_node_design)

    def make_edge(
        self,
        start_node: str = "empty",
        end_node: str = "empty",
    ):
        self.design_edge()
        self.digraph.edge(self.autolinebreak(start_node), self.autolinebreak(end_node))

    def make_chain(self, *args):
        for i in range(len(args) - 1):
            self.make_edge(args[i], args[i + 1])

    def viz(self):
        self.digraph.render(directory=self.filepath, view=False)
        ff = "." + self.fileformat
        print(f"rendered to {os.path.join(self.filepath, self.filename + ff)}")

    def dict_reader(self, across=False, u_input=None) -> List[Dict[str, str]]:
        collect = []

        if not across:
            self.yml_f = [
                f for f in os.listdir(self.data_dir_path) if f.endswith(".yml")
            ]
            f_path = os.path.join(self.data_dir_path, self.yml_f[u_input])
            with open(f_path, "r") as proj_yml:
                proj = yml.safe_load(proj_yml)
            collect.append(proj)

        if across:
            self.yml_f = [
                f for f in os.listdir(self.data_dir_path) if f.endswith(".yml")
            ]

            for f in self.yml_f:
                f_path = os.path.join(self.data_dir_path, f)
                with open(f_path, "r") as proj_yml:
                    proj = yml.safe_load(proj_yml)
                collect.append(proj)

        return collect
