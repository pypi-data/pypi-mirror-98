import svgwrite
import svgwrite.shapes, svgwrite.container, svgwrite.text, svgwrite.mixins
from datetime import date, timedelta, datetime
import re
from coopgantt.gantt import Gantt, Task, Project, Milestone, Resource

class SvgContainer:
    def __init__(self, elements: svgwrite.container.Group, height, width):
        self.elements = elements
        self.height = height
        self.width = width


ONE_DAY = timedelta(days=1)
FONT_ATTR = {
    'fill': 'black',
    'subfill': 'purple',
    'stroke': 'black',
    'stroke_width': 0,
    'font_family': 'Arial',
    'font_size': 15,
    'projectheader': 'steelblue'
    }

DATE_FORMAT = "%m/%d/%Y"

# conversion from mm/cm to pixel is done by ourselves as firefox seems
# to have a bug for big numbers...
# 3.543307 is for conversion from mm to pt units !

MM = 3.543307
CM = 35.43307
import ctypes

def GetTextDimensions(text, points, font):
    class SIZE(ctypes.Structure):
        _fields_ = [("cx", ctypes.c_long), ("cy", ctypes.c_long)]

    hdc = ctypes.windll.user32.GetDC(0)
    hfont = ctypes.windll.gdi32.CreateFontA(int(points), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, font)
    hfont_old = ctypes.windll.gdi32.SelectObject(hdc, hfont)

    size = SIZE(0, 0)
    ctypes.windll.gdi32.GetTextExtentPoint32A(hdc, text, len(text), ctypes.byref(size))

    ctypes.windll.gdi32.SelectObject(hdc, hfont_old)
    ctypes.windll.gdi32.DeleteObject(hfont)

    return (size.cx, size.cy)

def save_svg(svg, filename, width="100%", height="100%", viewbox_height:int=0, viewbox_width:int=0):
    dwg = _my_svgwrite_drawing_wrapper(filename, debug=True)
    dwg.add(svg)

    # for resc in svg:
    #     dwg.add(resc)

    dwg.save(width, height, viewbox_width=viewbox_width, viewbox_height=viewbox_height)



def create_calendar(chart: Gantt, end=None, scale:float=1) -> (SvgContainer, SvgContainer, SvgContainer):
    cm = CM * scale
    mm = MM * scale
    """
    Draws SVG of gantt chart

    Based on https://bitbucket.org/xael/python-gantt/
    """

    start_date = chart.start_date - ONE_DAY

    if end is None:
        end_date = chart.end_date + 3 * ONE_DAY
    else:
        end_date = end

    if start_date > end_date:
        raise ValueError('Unable to draw chart, start date {0} > end_date {1}'.format(start_date, end_date))

    # How many days do we need to draw?
    maxx = (end_date - start_date).days

    # Draw calendar at top
    calendar_body_container = svgwrite.container.Group()
    calendar_header_container = svgwrite.container.Group()

    # Get SVG for each resource, but dont actually add yet to make ordering with calendar easy
    resources_svg, resources_height = svg_of_resources(chart, chart_size=maxx, prev_y=2, scale=scale)

    # Get SVG for each project, but don't actually add yet to make ordering with calendar easy
    projects_svg, headers, projects_height = svg_of_projects(chart, chart_size=maxx, prev_y=2 + resources_height,
                                                    start_date=start_date, end_date=end_date, scale=scale)

    chart_height = projects_height + resources_height

    # White background and calendar
    calendar_body_container.add(svgwrite.shapes.Rect(
        insert=(0 * cm, 0 * cm),
        size=((maxx + 1) * cm, (chart_height + 3) * cm),
        fill='white',
        stroke_width=0,
        opacity=1
    ))

    calendar_body, calendar_header = _svg_calendar(chart, maxx, chart_height, start_date, datetime.today(), scale=scale)
    calendar_body_container.add(calendar_body.elements)

    calendar_header_container.add(calendar_header.elements)

    return SvgContainer(calendar_body_container, width = (maxx + 1) * cm, height = (chart_height) * cm), \
           SvgContainer(calendar_header_container, width = (maxx + 1) * cm, height= 2 * cm), \
           SvgContainer(headers, width=500, height = (chart_height) * cm)

def create_svg_drawing(chart: Gantt, filename=None, end=None, scale: float=1) -> (SvgContainer, SvgContainer, SvgContainer):
    cm = CM * scale
    mm = MM * scale
    """
    Draws SVG of gantt chart

    Based on https://bitbucket.org/xael/python-gantt/
    """

    start_date = chart.start_date - ONE_DAY

    if end is None:
        end_date = chart.end_date + 3 * ONE_DAY
    else:
        end_date = end

    if start_date > end_date:
        raise ValueError('Unable to draw chart, start date {0} > end_date {1}'.format(start_date, end_date))

    # How many days do we need to draw?
    maxx = (end_date - start_date).days

    # Draw calendar at top
    projects = svgwrite.container.Group()
    resources = svgwrite.container.Group()
    # dwg = _my_svgwrite_drawing_wrapper(filename, debug=True)

    # Get SVG for each resource, but dont actually add yet to make ordering with calendar easy
    resources_svg, resources_height = svg_of_resources(chart, chart_size=maxx,scale=scale)

    # Get SVG for each project, but don't actually add yet to make ordering with calendar easy
    projects_svg, headers, projects_height = svg_of_projects(chart, chart_size=maxx, prev_y=resources_height, start_date=start_date, end_date=end_date, scale=scale)

    chart_height = projects_height + resources_height

    # White background and calendar
    projects.add(svgwrite.shapes.Rect(
        insert=(0 * cm, 0 * cm),
        size=((maxx + 1) * cm, (chart_height) * cm),
        fill='white',
        stroke_width=0,
        opacity=1
    ))
    calendar_body, calendar_header = _svg_calendar(chart, maxx, chart_height, start_date, datetime.today(), scale=scale)
    projects.add(calendar_body.elements)

    # Highlight today
    todayx = (datetime.today().date() - start_date).days
    projects.add(svgwrite.shapes.Rect(
        insert=(todayx * cm, 0),
        size=(cm, (chart_height) * cm),
        fill='purple',
        stroke_width=0,
        opacity=.5
    ))

    # Draw each resource
    for resc in resources_svg:
        projects.add(resc)

    # Draw each project
    for proj in projects_svg:
        projects.add(proj)

    # Draw dependencies between tasks
    dep = svg_chart_dependencies(chart, scale=scale)
    if dep is not None:
        projects.add(dep)

    return SvgContainer(projects, width = (maxx + 1) * cm, height = (chart_height) * cm), \
           SvgContainer(resources, width = (maxx + 1) * cm, height = (resources_height) * cm), \
           SvgContainer(headers, width=500, height = (chart_height) * cm)


def svg_chart_dependencies(chart: Gantt, scale: float =1):
    """
    Draws svg dependencies between tasks according to coordinates cached
    when drawing tasks
    """
    svg = svgwrite.container.Group()
    for t in chart.tasks:
        trepr = svg_task_dependencies(t, scale=scale)
        if trepr is not None:
            svg.add(trepr)
    return svg

def svg_task_dependencies(task: Task, scale: float =1):
    """
    Draws svg dependencies between task and project according to coordinates
    cached when drawing tasks
    """

    mm = MM * scale
    cm = CM * scale


    if not task.dependencies:
        return None
    else:
        svg = svgwrite.container.Group()
        x_off = 0
        for t in task.dependencies:


            if not (t.drawn_x_end_coord is None or t.drawn_y_coord is None or task.drawn_x_begin_coord is None):
                # horizontal line
                svg.add(svgwrite.shapes.Line(
                        start=((t.drawn_x_end_coord - 2)*mm, (t.drawn_y_coord + 9)*mm),
                        end=((task.drawn_x_begin_coord + x_off)*mm, (t.drawn_y_coord + 9)*mm),
                        stroke='black',
                        stroke_dasharray='5,3',
                        ))

                marker = svgwrite.container.Marker(insert=(5,5), size=(10,10))
                marker.add(svgwrite.shapes.Circle((5, 5), r=3, fill='#000000', opacity=0.5, stroke_width=0))
                svg.add(marker)
                # vertical line
                eline = svgwrite.shapes.Line(
                    start=((task.drawn_x_begin_coord + x_off)*mm, (t.drawn_y_coord + 10)*mm),
                    end=((task.drawn_x_begin_coord  + x_off)*mm, (task.drawn_y_coord + 5)*mm),
                    stroke='black',
                    stroke_dasharray='5,3',
                    )
                eline['marker-end'] = marker.get_funciri()
                svg.add(eline)

            x_off += 2

    return svg


def _svg_calendar(chart:Gantt, maxx, maxy, start_date, today=None, scale: float = 1) -> (SvgContainer, SvgContainer):
    """
    Draw calendar in svg, begining at start_date for maxx days, containing
    maxy lines. If today is given, draw a blue line at date

    Keyword arguments:
    maxx -- number of days, weeks, months or quarters (depending on scale) to draw
    maxy -- number of lines to draw
    start_date -- datetime.date of the first day to draw
    today -- datetime.date of day as today reference
    """

    cm = CM * scale
    mm = MM * scale

    header = svgwrite.container.Group()
    body = svgwrite.container.Group()
    # dwg = svgwrite.container.Group()

    cal = {0: 'Mo', 1: 'Tu', 2: 'We', 3: 'Th', 4: 'Fr', 5: 'Sa', 6: 'Su'}

    maxx += 1

    vlines = body.add(svgwrite.container.Group(id='vlines', stroke='lightgray'))
    for x in range(maxx):
        vlines.add(svgwrite.shapes.Line(start=(x * cm, 2 * cm), end=(x * cm, (maxy) * cm)))
        jour = start_date + timedelta(days=x)

        if today is not None and today == jour:
            vlines.add(svgwrite.shapes.Rect(
                insert=((x + 0.4) * cm, 0),
                size=(0.2 * cm, maxy * cm),
                fill='#76e9ff',
                stroke='lightgray',
                stroke_width=0,
                opacity=0.8
            ))

        # draw vacations
        if (start_date + timedelta(days=x)).weekday() in chart.weekend_days:
            vlines.add(svgwrite.shapes.Rect(
                insert=(x * cm, 0),
                size=(1 * cm, maxy * cm),
                fill='gray',
                stroke='lightgray',
                stroke_width=1,
                opacity=0.7,
            ))

        # Current day
        text = svgwrite.text.Text('{1} {0:02}'.format(jour.day, cal[jour.weekday()][0]),
                                      insert=((x * 10 + 1) * mm, 19 * mm),
                                      fill='black', stroke='black', stroke_width=0,
                                      font_family=FONT_ATTR['font_family'], font_size=(15 - 3) * scale)
        # vlines.add(text)
        header.add(text)

        # Year
        if x == 0 or (jour.day == 1 and jour.month == 1):
            text = svgwrite.text.Text('{0}'.format(jour.year),
                                          insert=((x * 10 + 1) * mm, 5 * mm),
                                          fill='#400000', stroke='#400000', stroke_width=0,
                                          font_family=FONT_ATTR['font_family'], font_size=(15 + 5) * scale,
                                          font_weight="bold")
            # vlines.add(text)
            header.add(text)

        # Month name
        if x == 0 or (jour.day == 1):
            text = svgwrite.text.Text('{0}'.format(jour.strftime("%B")),
                                          insert=((x * 10 + 1) * mm, 10 * mm),
                                          fill='#800000', stroke='#800000', stroke_width=0,
                                          font_family=FONT_ATTR['font_family'], font_size=(15 + 3) * scale,
                                          font_weight="bold")
            # vlines.add(text)
            header.add(text)

        # Week number
        if jour.weekday() == 0:
            text = svgwrite.text.Text('{0:02}'.format(jour.isocalendar()[1]),
                                          insert=((x * 10 + 1) * mm, 15 * mm),
                                          fill='black', stroke='black', stroke_width=0,
                                          font_family=FONT_ATTR['font_family'],
                                          font_size=(15 + 1) * scale,
                                          font_weight="bold")
            # vlines.add(text)
            header.add(text)

    vlines.add(svgwrite.shapes.Line(start=(maxx * cm, 2 * cm), end=(maxx * cm, (maxy) * cm)))

    hlines = body.add(svgwrite.container.Group(id='hlines', stroke='lightgray'))

    body.add(svgwrite.shapes.Line(start=(0 * cm, 2 * cm), end=(maxx * cm, 2 * cm), stroke='black'))
    body.add(svgwrite.shapes.Line(start=(0 * cm, (maxy) * cm), end=(maxx * cm, (maxy) * cm), stroke='black'))

    for y in range(2, maxy + 1):
        hlines.add(svgwrite.shapes.Line(start=(0 * cm, y * cm), end=(maxx * cm, y * cm)))

    return SvgContainer(body, width=maxx*cm, height=2 * cm), SvgContainer(header, width=maxx*cm, height= maxy * cm)

def _time_diff(e, s):
    return (e - s).days
def _time_diff_d(e, s):
    return _time_diff(e, s) + 1


def svg_of_task_descriptions(task: Task,
                            prev_y=0,
                            offset=0,
                            scale: float=1):

    mm = MM * scale
    cm = CM * scale
    svg = svgwrite.container.Group()
    y = prev_y * 10

    text = None
    text_chars = 50
    if len(task.header) >= text_chars:
        text = task.header[:text_chars - 3] + "..."
    else:
        text = task.header.ljust(text_chars, ' ')

    text_width = GetTextDimensions(text, (10) * scale, FONT_ATTR['font_family'])
    start_date_width = GetTextDimensions(str(task.start_date), (10) * scale, FONT_ATTR['font_family'])
    end_date_width = GetTextDimensions(str(task.end_date), (10) * scale, FONT_ATTR['font_family'])


    padding = 100
    total_width = text_width[0] + start_date_width[0] + end_date_width[0] + padding * 2

    # Background Rectangle
    background = svgwrite.shapes.Rect(
            insert=((offset)*mm, (y+1)*mm),
            size=(total_width, 8*mm),
            fill="white",
            stroke_width=2,
            opacity=0.25,
            class_='task_header',
            )
    svg.add(background)



    svg.add(svgwrite.text.Text(f"{text}",
                               insert=((offset + 1)*mm, (y + 5)*mm),
                               fill=FONT_ATTR['fill'],
                               stroke=FONT_ATTR['stroke'],
                               stroke_width=FONT_ATTR['stroke_width'],
                               font_family=FONT_ATTR['font_family'],
                               font_size=(10) * scale))
    svg.add(svgwrite.text.Text(f"{task.start_date}",
                               insert=((offset + 1)*mm + text_width[0] + padding, (y + 5)*mm),
                               fill=FONT_ATTR['fill'],
                               stroke=FONT_ATTR['stroke'],
                               stroke_width=FONT_ATTR['stroke_width'],
                               font_family=FONT_ATTR['font_family'],
                               font_size=(10) * scale))
    svg.add(svgwrite.text.Text(f"{task.end_date}",
                               insert=((offset + 1)*mm + text_width[0] + start_date_width[0] + padding, (y + 5)*mm),
                               fill=FONT_ATTR['fill'],
                               stroke=FONT_ATTR['stroke'],
                               stroke_width=FONT_ATTR['stroke_width'],
                               font_family=FONT_ATTR['font_family'],
                               font_size=(10) * scale))

    return svg, total_width


def svg_of_task(task: Task, prev_y=0, start=None, end=None, color=None, level=None, offset=0, scale: float=1):
    """
    Return SVG for drawing this task.

    Keyword arguments:
    prev_y -- int, line to start to draw
    start -- datetime.date of first day to draw
    end -- datetime.date of last day to draw
    color -- string of color for drawing the project
    level -- int, indentation level of the project, not used here
    scale -- drawing scale (d: days, w: weeks, m: months, q: quaterly)
    title_align_on_left -- boolean, align task title on left
    offset -- X offset from image border to start of drawing zone
    """
    mm = MM * scale
    cm = CM * scale


    if not task.is_scheduled:
        raise Exception('Unable to draw task until it has been scheduled')

    add_planned_begin_mark = True
    add_target_end_mark = True
    add_expected_end_mark = True
    add_begin_mark = True
    add_end_mark = True

    y = prev_y * 10

    if color is None:
        color = task.resources[0].color

    # cas 1 -s--S==E--e-
    if task.start_date >= start and task.end_date <= end:
        x = _time_diff(task.start_date, start) * 10
        d = _time_diff_d(task.end_date, task.start_date) * 10
        task.drawn_x_begin_coord = x
        task.drawn_x_end_coord = x+d
    # cas 5 -s--e--S==E-
    elif task.start_date > end:
        return (None, 0)
    # cas 6 -S==E-s--e-
    elif task.end_date < start:
        return (None, 0)
    # cas 2 -S==s==E--e-
    elif task.start_date < start and task.end_date <= end:
        x = 0
        d = _time_diff_d(task.end_date, start) * 10
        task.drawn_x_begin_coord = x
        task.drawn_x_end_coord = x+d
        add_begin_mark = True
    # cas 3 -s--S==e==E-
    elif task.start_date >= start and task.end_date > end:
        x = _time_diff(task.start_date, start) * 10
        d = _time_diff_d(end, task.start_date) * 10
        task.drawn_x_begin_coord = x
        task.drawn_x_end_coord = x+d
        add_end_mark = True
    # cas 4 -S==s==e==E-
    elif task.start_date < start and task.end_date > end:
        x = 0
        d = _time_diff_d(end, start) * 10
        task.drawn_x_begin_coord = x
        task.drawn_x_end_coord = x+d
        add_end_mark = True
        add_begin_mark = True
    else:
        return (None, 0)

    task.drawn_y_coord = y

    # Task Group
    svg = svgwrite.container.Group(id=re.sub(r"[ ,'\/()]", '_', task.name))
    svg.attribs['class'] = 'task'

    # Background Rectangle
    background = svgwrite.shapes.Rect(
            insert=((x+1+offset)*mm, (y+1)*mm),
            size=((d-2)*mm, 8*mm),
            fill=color,
            stroke=color,
            stroke_width=2,
            opacity=0.25,
            class_='task',
            rx=10,
            ry=10
            )
    background.attribs['class'] = 'task'
    svg.add(background)

    # Planned Begin Mark
    if add_planned_begin_mark and task.dont_start_before_date:  #and task.start_date > task.dont_start_before_date:
        beg_offset = _time_diff(task.dont_start_before_date, start) * 10
        svg.add(svgwrite.shapes.Rect(
                insert=((beg_offset+1)*mm, (y+1)*mm),
                size=(3*mm, 8*mm),
                fill="#0000ff",
                stroke=color,
                stroke_width=1,
                opacity=0.35,
                ))

    # Modifed End Mark
    # if add_modified_end_mark:
    #     svg.add(svgwrite.shapes.Rect(
    #             insert=((x+d-7+1)*mm, (y+1)*mm),
    #             size=(5*mm, 4*mm),
    #             fill="#0000FF",
    #             stroke=color,
    #             stroke_width=1,
    #             opacity=0.35,
    #             ))

    # Begin Mark
    if add_begin_mark:
        svg.add(svgwrite.shapes.Rect(
                insert=((x+1)*mm, (y+1)*mm),
                size=(5*mm, 8*mm),
                fill="#000000",
                stroke=color,
                stroke_width=1,
                opacity=0.2,
                ))

    # End Mark
    if add_end_mark:
        svg.add(svgwrite.shapes.Rect(
                insert=((x+d-7+1)*mm, (y+1)*mm),
                size=(5*mm, 8*mm),
                fill="#000000",
                stroke=color,
                stroke_width=1,
                opacity=0.2,
                ))

    # Percent Done Rectangle
    background = svgwrite.shapes.Rect(
            insert=((x+1+offset)*mm, (y+1)*mm),
            size=(((d-2)*task.percent_done/100)*mm, 8*mm),
            fill=color,
            stroke=color,
            stroke_width=2,
            opacity=0.85,
            class_='task',
            rx=10,
            ry=10
            )
    background.attribs['class'] = 'task'
    svg.add(background)

    # Missed Target Mark
    if add_target_end_mark and task.target_completion_date and task.target_completion_date < task.end_date:
        beg_offset = _time_diff(task.target_completion_date, start) * 10
        svg.add(svgwrite.shapes.Rect(
                insert=((beg_offset+1)*mm, (y+1)*mm),
                size=(5*mm, 8*mm),
                fill="#ff0000",
                stroke="#ff0000",
                stroke_width=1,
                opacity=0.35,
                ))
        svg.add(svgwrite.shapes.Rect(
            insert=((x + 1 + offset) * mm, (y + 1) * mm),
            size=((d - 2) * mm, 8 * mm),
            stroke="#ff0000",
            stroke_width=2,
            fill_opacity=0.0,
            class_='task',
            rx=10,
            ry=10
        ))

    # Expected End Mark
    if add_expected_end_mark and task.end_date_estimated > task.end_date:
        exp_end_offset = _time_diff(task.end_date_estimated, start) * 10
        svg.add(svgwrite.shapes.Rect(
                insert=((exp_end_offset+1)*mm, (y+1)*mm),
                size=(5*mm, 8*mm),
                fill="#FFA500",
                stroke="#FFA500",
                stroke_width=1,
                opacity=0.2,
                ))

    # Title alignment
    tx = x+2

    svg.add(svgwrite.text.Text(f"{task.header}", insert=((tx)*mm, (y + 5)*mm), fill=FONT_ATTR['fill'], stroke=FONT_ATTR['stroke'], stroke_width=FONT_ATTR['stroke_width'], font_family=FONT_ATTR['font_family'], font_size=(15) * scale))

    t = ""
    if task.resources is not None:
        t = " / ".join(["{0}".format(r.name) for r in task.resources])
        svg.add(svgwrite.text.Text("{0}".format(t), insert=(tx*mm, (y + 8.5)*mm), fill=FONT_ATTR['subfill'], stroke=FONT_ATTR['stroke'], stroke_width=FONT_ATTR['stroke_width'], font_family=FONT_ATTR['font_family'], font_size=(15-5) * scale))

    txt_len = GetTextDimensions(t, (15-5) * scale, FONT_ATTR['font_family'])

    svg.add(
        svgwrite.text.Text(f"{datetime.strftime(task.start_date, DATE_FORMAT)} - {datetime.strftime(task.end_date, DATE_FORMAT)}", insert=((tx + txt_len[0]) * mm, (y + 8.5) * mm), fill=FONT_ATTR['subfill'], stroke=FONT_ATTR['stroke'],
                           stroke_width=FONT_ATTR['stroke_width'], font_family=FONT_ATTR['font_family'],
                           font_size=(15 - 5) * scale))


    return (svg, 1)





def svg_of_milestone(milestone: Milestone, prev_y=0, start=None, end=None, color=None, level=None, offset=0, scale: float=1):
    """
    Return SVG for drawing this task.

    Keyword arguments:
    prev_y -- int, line to start to draw
    start -- datetime.date of first day to draw
    end -- datetime.date of last day to draw
    color -- string of color for drawing the project
    level -- int, indentation level of the project, not used here
    scale -- drawing scale (d: days, w: weeks, m: months, q: quaterly)
    title_align_on_left -- boolean, align task title on left
    offset -- X offset from image border to start of drawing zone
    """
    mm = MM * scale
    cm = CM * scale


    if not milestone.is_scheduled:
        raise Exception('Unable to draw task until it has been scheduled')

    y = prev_y * 10

    x = _time_diff(milestone.start_date, start) * 10


    # cas 1 -s--S==E--e-
    if milestone.start_date >= start and milestone.end_date <= end:
        x = _time_diff(milestone.start_date, start) * 10
        d = _time_diff_d(milestone.end_date, milestone.start_date) * 10
        milestone.drawn_x_begin_coord = x
        milestone.drawn_x_end_coord = x+d
    # cas 5 -s--e--S==E-
    elif milestone.start_date > end:
        return (None, 0)
    # cas 6 -S==E-s--e-
    elif milestone.end_date < start:
        return (None, 0)
    # cas 2 -S==s==E--e-
    elif milestone.start_date < start and milestone.end_date <= end:
        x = 0
        d = _time_diff_d(milestone.end_date, start) * 10
        milestone.drawn_x_begin_coord = x
        milestone.drawn_x_end_coord = x+d
        add_begin_mark = True
    # cas 3 -s--S==e==E-
    elif milestone.start_date >= start and milestone.end_date > end:
        x = _time_diff(milestone.start_date, start) * 10
        d = _time_diff_d(end, milestone.start_date) * 10
        milestone.drawn_x_begin_coord = x
        milestone.drawn_x_end_coord = x+d
        add_end_mark = True
    # cas 4 -S==s==e==E-
    elif milestone.start_date < start and milestone.end_date > end:
        x = 0
        d = _time_diff_d(end, start) * 10
        milestone.drawn_x_begin_coord = x
        milestone.drawn_x_end_coord = x+d
        add_end_mark = True
        add_begin_mark = True
    else:
        return (None, 0)


    milestone.drawn_y_coord = y





    # Milestone Group
    svg = svgwrite.container.Group(id=re.sub(r"[ ,'\/()]", '_', milestone.name))
    svg.attribs['class'] = 'milestone'



    if color is None:
        color = 'lightblue' if milestone.done else 'yellow'
    opacity = 1 if milestone.done else .65

    # Background Circle
    background = svgwrite.shapes.Circle(
        center=((x + 5 + offset) * mm, (y + 5) * mm),
        r=10 * scale,
        fill=color,
        stroke='black',
        stroke_width=2,
        opacity=opacity,
    )
    background.attribs['class'] = 'milestone'
    svg.add(background)

    # Title alignment
    tx = x+10

    svg.add(svgwrite.text.Text(f"{milestone.name}", insert=((tx)*mm, (y + 5)*mm), fill=FONT_ATTR['fill'], stroke=FONT_ATTR['stroke'], stroke_width=FONT_ATTR['stroke_width'], font_family=FONT_ATTR['font_family'], font_size=(15) * scale))

    t = ""
    if milestone.resources is not None:
        t = " / ".join(["{0}".format(r.name) for r in milestone.resources])
        svg.add(svgwrite.text.Text("{0}".format(t), insert=(tx*mm, (y + 8.5)*mm), fill=FONT_ATTR['subfill'], stroke=FONT_ATTR['stroke'], stroke_width=FONT_ATTR['stroke_width'], font_family=FONT_ATTR['font_family'], font_size=(15-5) * scale))

    txt_len = GetTextDimensions(t, (15-5) * scale, FONT_ATTR['font_family'])

    svg.add(
        svgwrite.text.Text(f"{datetime.strftime(milestone.start_date, DATE_FORMAT)} - {datetime.strftime(milestone.end_date, DATE_FORMAT)}", insert=((tx + txt_len[0]) * mm, (y + 8.5) * mm), fill=FONT_ATTR['subfill'], stroke=FONT_ATTR['stroke'],
                           stroke_width=FONT_ATTR['stroke_width'], font_family=FONT_ATTR['font_family'],
                           font_size=(15 - 5) * scale))


    return (svg, 1)

def svg_of_resources(chart: Gantt, chart_size: int, prev_y:int =0, scale:float = 1):
    """
    Return (SVG code, number of lines drawn) for the resources. Draws the resource usage by day.

    Keyword arguments:
    prev_y -- int, line to start to draw
    color -- string of color for drawing the project
    level -- int, indentation level of the project
    scale -- drawing scale (d: days, w: weeks, m: months, q: quaterly)
    offset -- X offset from image border to start of drawing zone
    """
    mm = MM * scale
    cm = CM * scale

    y = prev_y * 10

    resources_svg = []

    # Draw Title
    svg = svgwrite.container.Group(id=re.sub(r"[ ,'\/()]", '_', "Resources"))
    background = svgwrite.shapes.Rect(
            insert=(0*mm, (y+1)*mm),
            size=((chart_size + 1)*cm, 8*mm),
            fill='black',
            stroke='black',
            stroke_width=2,
            opacity=0.75,
            class_='resource',
            )
    svg.add(background)
    svg.add(svgwrite.text.Text(f"Resources", insert=((0) * mm, (y + 6) * mm), fill='white',
                               stroke=FONT_ATTR['stroke'], stroke_width=FONT_ATTR['stroke_width'],
                               font_family=FONT_ATTR['font_family'], font_size=(20) * scale, font_weight='bold'))

    resources_svg.append(svg)

    # Draw Resources

    resources_height = 1
    ldwg = None

    start_date = chart.start_date

    for resource in chart.resources:
        ldwg = svgwrite.container.Group()
        rsvg, rheight = svg_of_resource(resource, start_date=start_date, chart_size=chart_size, prev_y=prev_y + resources_height, scale=scale)
        if rsvg is not None:
            ldwg.add(rsvg)
            resources_svg.append(ldwg)
            resources_height += rheight

    return (resources_svg, resources_height)


def svg_of_resource(resource: Resource, start_date: date, chart_size: int, prev_y=0, color=None, level=0, offset=0, scale:float=1):
    """
    Return (SVG code, number of lines drawn) for the resource. Draws the resource usage by day.

    Keyword arguments:
    prev_y -- int, line to start to draw
    start -- datetime.date of first day to draw
    end -- datetime.date of last day to draw
    color -- string of color for drawing the project
    level -- int, indentation level of the project
    scale -- drawing scale (d: days, w: weeks, m: months, q: quaterly)
    offset -- X offset from image border to start of drawing zone
    """
    mm = MM * scale
    cm = CM * scale

    y = prev_y * 10

    if color is None:
        color = resource.color

    resource.drawn_y_coord = y

    svg = svgwrite.container.Group(id=re.sub(r"[ ,'\/()]", '_', resource.name))

    # Background Rectangle
    background = svgwrite.shapes.Rect(
            insert=(0*mm, (y+1)*mm),
            size=((chart_size + 1)*cm, 8*mm),
            fill=color,
            stroke=color,
            stroke_width=2,
            opacity=0.25,
            class_='resource',
            )
    svg.add(background)

    # Draw Resource Names
    svg.add(svgwrite.text.Text(f"{resource.name}", insert=((0) * mm, (y + 5) * mm), fill=FONT_ATTR['fill'],
                               stroke=FONT_ATTR['stroke'], stroke_width=FONT_ATTR['stroke_width'],
                               font_family=FONT_ATTR['font_family'], font_size=(15) * scale))

    # Draw Resource capacities
    for nDays in range(0, chart_size):
        n_used = resource.n_used(start_date + timedelta(days=nDays))

        # Draw Percent of capacity used rectangle
        svg.add(svgwrite.shapes.Rect(
            insert=((nDays + 1) * cm, (y) * mm),
            size=((1)*cm, (min(n_used/resource.capacity, 1))*cm),
            fill=color,
            stroke=color,
            stroke_width=2,
            opacity=0.75,
            class_='resource',
            )
        )

        # Write resources used SVG
        svg.add(svgwrite.text.Text(f"{n_used}", insert=((nDays + 1) * cm + 8, (y + 7) * mm), fill=FONT_ATTR['fill'],
                                   stroke=FONT_ATTR['stroke'], stroke_width=FONT_ATTR['stroke_width'],
                                   font_family=FONT_ATTR['font_family'], font_size=(15) * scale))

    return (svg, 1)


def svg_of_projects(chart: Gantt, chart_size: int, prev_y:int =0, start_date=None, end_date=None, scale:float = 1):
    """
    Return (SVG code, number of lines drawn) for the resource. Draws the resource usage by day.

    Keyword arguments:
    prev_y -- int, line to start to draw
    start -- datetime.date of first day to draw
    end -- datetime.date of last day to draw
    color -- string of color for drawing the project
    level -- int, indentation level of the project
    scale -- drawing scale (d: days, w: weeks, m: months, q: quaterly)
    offset -- X offset from image border to start of drawing zone
    """
    mm = MM * scale
    cm = CM * scale

    y = prev_y * 10

    projects_svg = []

    # Draw Title
    svg = svgwrite.container.Group(id=re.sub(r"[ ,'\/()]", '_', "Projects"))
    background = svgwrite.shapes.Rect(
            insert=(0*mm, (y+1)*mm),
            size=((chart_size + 1)*cm, 8*mm),
            fill='black',
            stroke='black',
            stroke_width=2,
            opacity=0.75,
            class_='resource',
            )
    svg.add(background)
    svg.add(svgwrite.text.Text(f"Projects", insert=((0) * mm, (y + 6) * mm), fill='white',
                               stroke=FONT_ATTR['stroke'], stroke_width=FONT_ATTR['stroke_width'],
                               font_family=FONT_ATTR['font_family'], font_size=(20) * scale, font_weight='bold'))

    projects_svg.append(svg)
    headers_svg = svgwrite.container.Group()


    # Get SVG for each project, but don't actually add yet to make ordering with calendar easy
    projects_height = 1
    ldwg = None
    for proj in chart.projects:
        ldwg = svgwrite.container.Group()
        psvg, header, pheight = svg_of_project(proj, prev_y=prev_y + projects_height, start=start_date, end=end_date, scale=scale)
        if psvg is not None:
            ldwg.add(psvg)
            headers_svg.add(header)
            projects_svg.append(ldwg)
            projects_height += pheight

    return (projects_svg, headers_svg, projects_height)

def svg_of_project(project: Project, prev_y=0, start=None, end=None, color=None, level=0, offset=0, scale:float=1):
    """
    Return (SVG code, number of lines drawn) for the project. Draws all
    tasks and add project name with a purple bar on the left side.

    Keyword arguments:
    prev_y -- int, line to start to draw
    start -- datetime.date of first day to draw
    end -- datetime.date of last day to draw
    color -- string of color for drawing the project
    level -- int, indentation level of the project
    scale -- drawing scale (d: days, w: weeks, m: months, q: quaterly)
    offset -- X offset from image border to start of drawing zone
    """

    mm = MM * scale
    cm = CM * scale


    if start is None:
        start = project.start_date
    if end is None:
        end = project.end_date

    cy = prev_y + 1*(project.name != "")

    prj = svgwrite.container.Group()
    header = svgwrite.container.Group()

    amount_done = 0
    amount_of_work = 0

    # sort activities so that they render nicely
    project.activities.sort(key=lambda x: x.start_date)

    # Draw tasks
    for t in project.activities:
        thead, width = svg_of_task_descriptions(t, prev_y=cy)

        header.add(thead)
        if type(t) == Task:
            trepr, theight = svg_of_task(t, cy, start=start, end=end, color=color, level=level+1, offset=offset, scale=scale)
            if trepr is not None:
                amount_done += (t.end_date - t.start_date).days * t.percent_done/100.0
                amount_of_work += (t.end_date - t.start_date).days + 1
        elif type(t) == Milestone:
            trepr, theight = svg_of_milestone(t, cy, start=start, end=end, color=color, level=level+1, offset=offset, scale=scale)
        else:
            raise NotImplementedError("The type of task found in project.activities is not supported by the SVG renderer")

        if trepr is not None:
            prj.add(trepr)
        cy += theight

    fprj = svgwrite.container.Group()
    prj_bar = False
    if project.name != "":
        if ((project.start_date >= start and project.end_date <= end)
            or ((project.end_date >=start and project.start_date <= end))) or level == 1:


            # Background Rectangle
            # insert=((x+1+offset)*mm, (y+1)*mm),
            # size=((d-2)*mm, 8*mm),
            background = svgwrite.shapes.Rect(
                insert=((_time_diff(project.start_date, start) + offset) * cm, ((prev_y)*10+1) * mm),
                size=((_time_diff(project.end_date, project.start_date)+1) * cm, 8 * mm),
                fill=FONT_ATTR['projectheader'],
                stroke='black',
                stroke_width=2,
                opacity=0.25,
                rx=10,
                ry=10
            )
            background.attribs['class'] = 'project'
            fprj.add(background)

            est_perc_done = amount_done/amount_of_work
            amount_done_rect = svgwrite.shapes.Rect(
                insert=((_time_diff(project.start_date, start) + offset) * cm, ((prev_y)*10+1) * mm),
                size=((_time_diff(project.end_date, project.start_date)+1) * cm * est_perc_done, 8 * mm),
                fill=FONT_ATTR['projectheader'],
                stroke=FONT_ATTR['projectheader'],
                stroke_width=2,
                opacity=0.85,
                rx=10,
                ry=10
            )
            amount_done_rect.attribs['class'] = 'project'
            fprj.add(amount_done_rect)




            # (6*level+3+offset)*mm
            proj_text = svgwrite.text.Text('{0}'.format(project.name),
                                           insert=((_time_diff(project.start_date, start) + offset + .15) * cm,
                                                   ((prev_y)*10+7)*mm),
                                           fill=FONT_ATTR['fill'],
                                           stroke=FONT_ATTR['stroke'],
                                           stroke_width=FONT_ATTR['stroke_width'],
                                           font_family=FONT_ATTR['font_family'],
                                           font_size=(15+3) * scale,
                                           font_weight="bold")
            fprj.add(proj_text)

            fprj.add(svgwrite.shapes.Rect(
                    insert=((6*level+0.8+offset)*mm, (prev_y+0.5)*cm),
                    size=(0.2*cm, ((cy-prev_y-1)+0.4)*cm),
                    fill='purple',
                    stroke='lightgray',
                    stroke_width=0,
                    opacity=0.5
                    ))
            prj_bar = True
        else:
            cy -= 1

    # Do not display empty tasks
    if (cy - prev_y) == 0 or ((cy - prev_y) == 1 and prj_bar):
        return (None, 0)

    fprj.add(prj)

    return (fprj, header, cy-prev_y)

class _my_svgwrite_drawing_wrapper(svgwrite.Drawing):
    """
    Hack for being able to use a file descriptor as filename
    """
    def save(self, width='100%', height='100%', viewbox_width:int=0, viewbox_height:int=0):
        """ Write the XML string to **filename**. """
        test = False
        import io

        # Fix height and width
        self['height'] = height
        self['width'] = width

        if not viewbox_height==viewbox_width==0:
            svgwrite.mixins.ViewBox.viewbox(self, 0, 0, viewbox_width, viewbox_height)
            svgwrite.mixins.ViewBox.stretch(self)

        test = type(self.filename) == io.TextIOWrapper

        if test:
            self.write(self.filename)
        else:
            fileobj = io.open(str(self.filename), mode='w', encoding='utf-8')
            self.write(fileobj)
            fileobj.close()




