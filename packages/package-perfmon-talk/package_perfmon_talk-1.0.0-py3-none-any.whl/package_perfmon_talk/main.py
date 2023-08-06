import os
import time

import psutil
import pandas as pd
from pyecharts.charts import Line, Page
import pyecharts.options as opts


def get_process(process_name: str):
    """
    通过进程名称，返回进程对象和对应pid
    :param process_name: 进程名称
    :return: res_process 进程对象, res_pid 进程pid
    """
    generator_pro = psutil.process_iter()
    res_pid = [process.pid for process in generator_pro if process.name() == process_name.strip()]
    try:
        res_process = psutil.Process(res_pid[0])
        return res_process, res_pid
    except:
        raise psutil.AccessDenied("进程名称不存在，请确保应用已启动")


def get_cpu(res_process):
    cpu_list = []
    average_cpu = 0
    for i in range(10):
        cpu = res_process.cpu_percent(interval=0.1)
        cpu_list.append(cpu)
        average_cpu = float(sum(cpu_list)) / len(cpu_list) / 6
    average_cpu = "%.2F" % average_cpu
    print("CPU:{}%".format(average_cpu))
    return average_cpu


def get_memory(res_process, memtype="rss"):
    print(res_process)
    all_value = res_process.memory_info()
    memory = getattr(all_value, memtype) / 1024 / 1024
    memory = "%.2F" % memory
    print("内存：{}MB".format(memory))
    print('*' * 20)
    return memory


def run(process_name, collect_time):
    cpu_data = []
    memory_data = []
    data_dict = {}
    time_tup_list = []
    time_str = time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())
    res_process, avc_pid = get_process(process_name)
    while int(collect_time) > 0:
        cpu = get_cpu(res_process)
        memory = get_memory(res_process)
        cpu_data.append(float(cpu))
        memory_data.append(float(memory))
        time_tup_list.append(time.strftime("%H:%M:%S", time.localtime()))
        collect_time -= 1
    all_average_cpu = sum(cpu_data) / len(cpu_data)
    all_average_memory = sum(memory_data) / len(memory_data)
    columns = ["TIMESTAMP", "CPU/%", "MEMORY/MB"]
    data_dict[columns[0]] = time_tup_list
    data_dict[columns[1]] = cpu_data
    data_dict[columns[2]] = memory_data
    df = pd.DataFrame(data_dict)
    df.loc[0, "PID"] = avc_pid
    df.loc[0, "PackageName"] = "AgoraVideoCall"
    df.loc[0, "AVERAGE_CPU/%"] = all_average_cpu
    df.loc[0, "AVERAGE_MEMORY/MB"] = all_average_memory
    res_dir_path = os.path.dirname(__file__) + "/result/{}".format(time_str)
    excel_path = res_dir_path + "/data.xls"
    if not os.path.exists(res_dir_path):
        os.makedirs(res_dir_path)
    df.to_excel(excel_writer=excel_path, sheet_name="windows_perform", index=False)
    chart_line(excel_path)


def chart_line(excel_path):
    """
    生成折线图表，保存到html中
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
                    # max_interval=3600 * 24 * 1000,
                    # axislabel_opts={'formatter':"{MM}/{dd} {HH}:{mm}"}
                ),  # axislabel_opts={"interval":"0"})  type_="category"
                yaxis_opts=opts.AxisOpts(
                    type_="value",
                    # axisline_opts=opts.AxisLineOpts(symbol=['none', 'arrow']),
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
                # symbol="emptyCircle",
                is_symbol_show=True,
                label_opts=opts.LabelOpts(is_show=False),
                markline_opts=opts.MarkLineOpts(
                    data=[opts.MarkLineItem(type_="average")]
                ),
                # is_smooth=True,
            )
            # .render("basic_line_chart.html")
        )
        page.add(line)
    page.render("{}/result_chart.html".format(os.path.dirname(excel_path)))
