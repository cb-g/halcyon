from lib.nonrecurring import data_handling, graphviz_auto


class CLI:
    def __init__(self):
        self.nonrecurring_data = data_handling()
        self.nonrecurring_graphviz = graphviz_auto()

    def run(self):
        self.nonrecurring_data.menu()
