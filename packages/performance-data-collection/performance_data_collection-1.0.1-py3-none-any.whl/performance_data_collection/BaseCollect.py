import datetime
import os
import sys
import time
from pyecharts.charts import Line, Page
import psutil
import pandas as pd
import pyecharts.options as opts
from pyecharts.charts import Line


class BaseCollect():

    def __init__(self, process_name, collect_time):
        self.platform_name = sys.platform
        self.process_name = process_name
        self.collect_time = collect_time
        self.res_process, self.pid = self.get_process()

    def get_process(self):
        """
        Returns the process object and the corresponding PID by the process name
        :param process_name: Process name
        :return: res_process process object, res_pid process pid
        """
        generator_pro = psutil.process_iter()
        res_pid = [process.pid for process in generator_pro if process.name() == self.process_name.strip()]
        try:
            res_process = psutil.Process(res_pid[0])
            return res_process, res_pid
        except:
            raise psutil.AccessDenied("Process name does not exist. Make sure the application is started")

    def get_cpu(self):
        cpu_list = []
        average_cpu = 0
        for i in range(10):
            cpu = self.res_process.cpu_percent(interval=0.1)
            cpu_list.append(cpu)
            average_cpu = float(sum(cpu_list)) / len(cpu_list) / psutil.cpu_count()
        average_cpu = "%.2F" % average_cpu
        print("CPU:{}%".format(average_cpu))
        return average_cpu

    def get_memory(self, memtype="rss"):
        all_value = self.res_process.memory_info()
        memory = getattr(all_value, memtype) / 1024 / 1024
        memory = "%.2F" % memory
        print("memory：{}MB".format(memory))
        print('*' * 20)
        return memory

    def run(self):
        cpu_data = []
        memory_data = []
        data_dict = {}
        time_tup_list = []
        file_name = time.strftime("%Y_%m_%d_%H_%M_%S",
                                  time.localtime()) + "_" + self.process_name + "_" + self.platform_name
        while int(self.collect_time) > 0:
            cpu = self.get_cpu()
            memory = self.get_memory()
            cpu_data.append(float(cpu))
            memory_data.append(float(memory))
            time_tup_list.append(time.strftime("%H:%M:%S", time.localtime()))
            self.collect_time -= 1
        all_average_cpu = sum(cpu_data) / len(cpu_data)
        all_average_memory = sum(memory_data) / len(memory_data)
        columns = ["TIMESTAMP", "CPU/%", "MEMORY/MB"]
        data_dict[columns[0]] = time_tup_list
        data_dict[columns[1]] = cpu_data
        data_dict[columns[2]] = memory_data
        df = pd.DataFrame(data_dict)
        df.loc[0, "PID"] = self.pid
        df.loc[0, "PackageName"] = self.process_name
        df.loc[0, "AVERAGE_CPU/%"] = all_average_cpu
        df.loc[0, "AVERAGE_MEMORY/MB"] = all_average_memory
        res_dir_path = os.getcwd() + "/result/{}".format(file_name)
        excel_path = res_dir_path + "/data.xls"
        if self.platform_name == 'darwin':
            excel_path = res_dir_path + "/data.xls"
        elif self.platform_name[0:3] == 'win':
            excel_path = res_dir_path + "/data.xlsx"
        if not os.path.exists(res_dir_path):
            os.makedirs(res_dir_path)
        df.to_excel(excel_writer=excel_path, sheet_name="{}_perform".format(self.platform_name), index=False)
        self.chart_line(excel_path)

    def chart_line(self, excel_path):
        """
        Generate a broken line chart and save it to HTML
        """
        page = Page()
        performance_data = pd.read_excel(excel_path)
        x_data = performance_data['TIMESTAMP'].tolist()
        cpu_data = performance_data['CPU/%'].tolist()
        memory_data = performance_data['MEMORY/MB'].tolist()
        cpu_info = {
            'data': cpu_data,
            'title': 'CPU折线图',
            'min': '',
            'max': '',
            'series_name': 'CPU'
        }
        memory_info = {
            'data': memory_data,
            'title': 'Memory折线图',
            'min': min(memory_data) - 3,
            'max': max(memory_data) + 3,
            'series_name': 'memory'
        }
        y_datas = [cpu_info, memory_info]
        for data in y_datas:
            line = (
                Line(init_opts=opts.InitOpts(width="1900px"))
                    .set_global_opts(
                    axispointer_opts=opts.AxisPointerOpts(
                        is_show=True,
                        type_="shadow",
                    ),
                    toolbox_opts=opts.ToolboxOpts(
                        is_show=True,
                    ),
                    title_opts=opts.TitleOpts(title=data['title']),
                    tooltip_opts=opts.TooltipOpts(is_show=True),
                    xaxis_opts=opts.AxisOpts(
                        type_="category",
                        boundary_gap=True,

                    ),
                    yaxis_opts=opts.AxisOpts(
                        type_="value",
                        axistick_opts=opts.AxisTickOpts(is_show=True),
                        splitline_opts=opts.SplitLineOpts(is_show=True),
                        min_=data['min'],
                        max_=data['max'],
                        boundary_gap=True,
                    ),
                )
                    .add_xaxis(xaxis_data=x_data)
                    .add_yaxis(
                    series_name=data['series_name'],
                    y_axis=data['data'],
                    is_symbol_show=True,
                    label_opts=opts.LabelOpts(is_show=False),
                    markline_opts=opts.MarkLineOpts(
                        data=[opts.MarkLineItem(type_="average")]
                    ),

                )

            )
            page.add(line)
        page.render("{}/result_chart.html".format(os.path.dirname(excel_path)))
