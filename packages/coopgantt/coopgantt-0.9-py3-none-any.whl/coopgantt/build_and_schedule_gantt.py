import datetime
from coopgantt.gantt import Gantt, Resource
import csv
from coopgantt.rendering.coloring import random_color
from coopgantt.rendering.build_html import save_html, create_html
from dateutil.parser import parse
from typing import Dict, List
from coopgantt.rendering.svg_renderer import save_svg, create_svg_drawing, create_calendar
from coopgantt.enums import ScheduleMethod
from datetime import date

def date_from_string(input:str):
    try:
        return parse(input).date()
    except:
        return None


def read_resource_file(filename: str):
    resources = []
    with open(filename) as file:
        data = csv.DictReader(file)

        for row in data:
            name = row['Resource']
            capacity = int(row['Capacity'])
            resources.append(Resource(name, capacity=capacity, color=random_color()))

    return resources

def read_data_file(filename: str):
    with open(filename) as csvfile:
        data = [x for x in csv.DictReader(csvfile)]

    return data

def build_and_schedule(gantt_name: str,
                       gantt_task_data: List[Dict],
                       resources: List[Resource],
                       resource_max_by_project: Dict = None,
                       project_priority: Dict = None,
                       schedule_start_date: date = None,
                       schedule_method: ScheduleMethod = None,
                       defined_schedule_sequence: Dict = None,
                       output_dirs: List[str] = None):

    gantt = Gantt.gantt_from_listdict(name=gantt_name, tasks_listdict=gantt_task_data, resources_dict={r.name: r for r in resources})

    if schedule_start_date is None:
        schedule_start_date = datetime.datetime.today().date()  # - datetime.timedelta(days=15)
    gantt.calculate_schedule(schedule_start_date,
                             max_resources_per_project=resource_max_by_project,
                             project_priority=project_priority,
                             schedule_method=schedule_method,
                             defined_schedule_sequence=defined_schedule_sequence)


    #Output
    if output_dirs is None:
        output_dirs = []
    for dir in output_dirs:
        gantt.as_dataframe().to_csv(dir, index=None)

    return gantt

def build_svgs(gantt,
               output_dirs: List[str] = None):

    SCALE = .75
    calendar_svg_container, calendar_header_container, tasks_header_container = create_calendar(gantt, scale=SCALE)
    projects_svg_container, resources_svg_container, tasks_header_container = create_svg_drawing(gantt, scale=SCALE)

    if output_dirs is None:
        output_dirs = []

    for dir in output_dirs:
        save_svg(calendar_header_container.elements, f'{dir}/calendar_header.svg', calendar_header_container.width,
                    calendar_header_container.height)
        save_svg(projects_svg_container.elements, f'{dir}/projects.svg', projects_svg_container.width,
                    projects_svg_container.height)
        save_svg(projects_svg_container.elements, f'{dir}/gantt_summary.svg', viewbox_width=projects_svg_container.width,
                    viewbox_height=projects_svg_container.height)
        save_svg(resources_svg_container.elements, f'{dir}/resources.svg', resources_svg_container.width,
                    resources_svg_container.height)
        save_svg(tasks_header_container.elements, f'{dir}/tasks_header.svg', tasks_header_container.width,
                    tasks_header_container.height)

if __name__ == "__main__":
    import logging
    loggingLvl = logging.DEBUG
    rootLogger = logging.getLogger('')
    rootLogger.handlers = []
    rootLogger.setLevel(loggingLvl)

    # Formatter
    consoleFormatter = logging.Formatter('%(name)s -- %(asctime)s : [%(levelname)s] %(message)s (%(filename)s lineno: %(lineno)d)')

    # #Console Handler
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(consoleFormatter)
    rootLogger.addHandler(console)

    resource_max_by_project = {"20-102037-03: R&D Project Darwin 2020": {"Dev I": 2},
                               "20-101825: Seegrid Test/Deployment": {"Dev I": 1},
                               "21-100425: MFI 1 - Myerstown TdaProxy Project": {"Dev I": 1}}
    project_priority = {"20-102037-03: R&D Project Darwin 2020": 2,
                        "21-100425: MFI 1 - Myerstown TdaProxy Project": 1,
                        "21-100428: MFI 2 - Boston (Marlborough) TDA Proxy Project": 1,
                        "21-100429: MFI 3 - Bordentown TDA Proxy project": 1,
                        "20-101747: KollMorgen System Manager Agent Service": 2,
                        "20-101825: Seegrid Test/Deployment": 2,
                        "R&D Maestro Continuous Development - WP1 (March-June)": 3,
                        "Task Assignment Visibility Improvements": 3,
                        "20-101747-05-01: KollMorgen System Manager CWAY Replacement": 2}

    ganttTasksCsvFilePath = 'C:/Users/tburns/Bastian Solutions/Software - _09 Maestro/Maestro - Customers/Raymond/Demo Site - Syracuse/gantt_items.csv'
    # ganttTasksCsvFilePath = 'C:/Users/tburns/Documents/GitHub/coopgantt/tests/testdata/gantt_items.csv'
    # resourceFileCsvFilePath = 'C:/Users/tburns/Documents/GitHub/ProjectGannt/data/resources.csv'
    resourceFileCsvFilePath = 'C:/Users/tburns/Bastian Solutions/Software - _09 Maestro/Maestro - Customers/Raymond/Demo Site - Syracuse/resources.csv'

    tasks = read_data_file(ganttTasksCsvFilePath)
    resources = read_resource_file(resourceFileCsvFilePath)

    defined_schedule_sequence = {x['id']: ii for ii, x in enumerate(tasks)}

    chart = build_and_schedule(gantt_name=ganttTasksCsvFilePath,
                               gantt_task_data=tasks,
                               resources=resources,
                               resource_max_by_project=resource_max_by_project,
                               project_priority=project_priority,
                               schedule_method=ScheduleMethod.DEFINED_SEQUENCE,
                               defined_schedule_sequence=defined_schedule_sequence,
                               output_dirs=[
                                   './gantt_items_scheduled.csv'
                               ])

    svg_renderings_dir = './rendering/svgs'
    build_svgs(chart, output_dirs=[svg_renderings_dir])

    html = create_html(chart, svg_input_dir=svg_renderings_dir, embed_css=True)
    save_html(html, 'main.html')


    print(chart)
