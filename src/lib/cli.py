from lib.nonrecurring import data_handling, graphviz_auto


class CLI:
    def __init__(self):
        self.nonrecurring_data = data_handling()
        self.nonrecurring_graphviz = graphviz_auto()

    def plot_for_nonrecurring(self, across = False, u_input = None):
        collect = self.nonrecurring_graphviz.dict_reader(across, u_input)
        tsks = []
        for l in collect:
            for dict in l:
                tsks.append(dict["task"])
            self.nonrecurring_graphviz.make_nodes(*tsks)
            self.nonrecurring_graphviz.make_chain(*tsks)
            tsks = []
        self.nonrecurring_graphviz.viz()

    def menu_for_nonrecurring(self):
        """
        navigation
        """
        self.nonrecurring_data.c_t()
        self.nonrecurring_data.dir_tree()
        self.nonrecurring_data.load_txt()

        while True:

            self.nonrecurring_data.t_o("1", clear=False)

            if self.nonrecurring_data.u_input == "v":
                self.nonrecurring_data.t_o("2")
                chrono = False
                graphic = False
                if self.nonrecurring_data.u_input == "c":
                    chrono = True
                if self.nonrecurring_data.u_input == "g":
                    graphic = True
                self.nonrecurring_data.t_o("3")
                if chrono & (self.nonrecurring_data.u_input == "w"):
                    self.nonrecurring_data.print_projects()
                    self.nonrecurring_data.t_o("4", clear=False)
                    self.nonrecurring_data.v_1_chrono()
                if chrono & (self.nonrecurring_data.u_input == "a"):
                    self.nonrecurring_data.v_a_chrono()
                if graphic & (self.nonrecurring_data.u_input == "w"):
                    self.nonrecurring_data.print_projects()
                    u_input = self.nonrecurring_data.t_o("4", clear=False, graphic=graphic)
                    self.plot_for_nonrecurring(across=False, u_input=u_input)
                if graphic & (self.nonrecurring_data.u_input == "a"):
                    self.plot_for_nonrecurring(across=True)
                break

            if self.nonrecurring_data.u_input == "e":
                self.nonrecurring_data.t_o("5")
                if self.nonrecurring_data.u_input == "a":
                    self.nonrecurring_data.t_o("6")
                    if self.nonrecurring_data.u_input == "n":
                        self.nonrecurring_data.add_project()
                        self.nonrecurring_data.add_task(new_proj=True)
                    if self.nonrecurring_data.u_input == "e":
                        self.nonrecurring_data.print_projects()
                        self.nonrecurring_data.t_o("4", clear=False)
                        self.nonrecurring_data.add_task()
                    break
                if self.nonrecurring_data.u_input == "c":
                    self.nonrecurring_data.t_o("7")
                    if self.nonrecurring_data.u_input == "p":
                        self.nonrecurring_data.print_projects()
                        self.nonrecurring_data.t_o("4", clear=False)
                        self.nonrecurring_data.rename_project()
                    if self.nonrecurring_data.u_input == "t":
                        self.nonrecurring_data.print_projects(filter=True)
                        self.nonrecurring_data.t_o("4", clear=False)
                        self.nonrecurring_data.edit_task()
                if self.nonrecurring_data.u_input == "d":
                    self.nonrecurring_data.t_o("7")
                    if self.nonrecurring_data.u_input == "p":
                        self.nonrecurring_data.print_projects()
                        self.nonrecurring_data.t_o("4", clear=False)
                        self.nonrecurring_data.delete_project()
                    if self.nonrecurring_data.u_input == "t":
                        self.nonrecurring_data.print_projects(filter=True)
                        self.nonrecurring_data.t_o("4", clear=False)
                        self.nonrecurring_data.delete_task()
                break

            break

    def run(self):
        self.menu_for_nonrecurring()
        # self.menu_for_recurring()
