from performance_data.BaseCollect import BaseCollect


class Win(BaseCollect):

    def __init__(self, process_name, collect_time):
        super().__init__(process_name, collect_time)

    def collect(self):
        self.run()


