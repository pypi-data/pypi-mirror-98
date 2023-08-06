from coopgantt.gantt import Gantt
from datetime import timedelta
from typing import List
import pkg_resources


def build_html(gantt: Gantt, svg_input_dir: str, embed_css: bool= True, output_dirs: List[str] = None):
   html = create_html(gantt, svg_input_dir=svg_input_dir, embed_css=embed_css)

   for dir in output_dirs:
      save_html(html, dir)

   return html

def save_html(html: str, file_path: str):
   f = open(file_path, 'w')
   f.write(html)
   f.close()

def create_html(gantt: Gantt, svg_input_dir:str, embed_css: bool= True) -> str:
   svg = open(f'{svg_input_dir}/projects.svg', 'r')
   svg_header = open(f'{svg_input_dir}/gantt_summary.svg', 'r')
   svg_calendar = open(f'{svg_input_dir}/calendar_header.svg', 'r')
   svg_resources = open(f'{svg_input_dir}/resources.svg', 'r')

   svg_data = svg.read()
   svg_header_data = svg_header.read()
   svg_calendar_data = svg_calendar.read()
   svg_resource_data = svg_resources.read()


   js_stream = pkg_resources.resource_stream(__name__, 'assets/myScripts.js')
   js_data = js_stream.read().decode("utf-8")
   # js = open('./rendering/assets/myScripts.js', 'r')
   # js_data = js.read()


   css_stream = pkg_resources.resource_stream(__name__, 'assets/styles.css')
   css_data= ""
   if embed_css: css_data = css_stream.read().decode("utf-8")

   # css = open('./rendering/assets/styles.css', 'r')
   # css_data= ""
   # if embed_css: css_data = css.read()



   task_rows = []

   for project in gantt.projects:
       task_rows.append(f"<tr class=\"rowsubgroup\"><td>{project.name}</td><td></td><td></td><td></td></tr>")
       for task in project.activities:
          text = None
          text_chars = 50
          if len(task.header) >= text_chars:
             text = task.header[:text_chars - 3] + "..."
          else:
             text = task.header.ljust(text_chars, ' ')
          task_rows.append(f"<tr><td>{text}</td><td>{task.start_date}</td><td>{task.end_date}</td><td>{task.percent_done}</td></tr>")

   task_rows_str = "".join(task_rows)

   resource_rows = []
   numdays = (gantt.end_date - gantt.start_date).days
   dates = [gantt.start_date + timedelta(days=x) for x in range(0, numdays)]
   for resource in gantt.resources:
      resources_used = [resource.n_used(date) for date in dates]
      resource_rows.append(
         f"<tr><td>{resource.name}</td><td>{round(sum(resources_used) / len(resources_used), 2)}</td></tr>")
   resource_rows_str = "".join(resource_rows)



   html = f"""<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <title>Maestro Project Gantt</title>
            <style>{css_data}</style>
        </head>
        <body>
            
            <div class="header">
                    <H1>Maestro Project Gantt</H1>
                    <div class="windowed_view" id="windowed_view">
                        {svg_header_data}
                    </div>
            </div>
            <!--<div class="header_spacer"></div>-->
            <div class = "content">
               <div class="cont_col_1" id="gantt_text">
                   <div id="table_spacer_1">Gantt Details</div>
                   <table id="resource_items"></div>
                       <thead>
                           <th>Resource Name</th>
                           <th>Average Daily Util</th>
                       </thead>
                       <tbody>
                           {resource_rows_str}
                       </tbody>
                   </table>
                  <div id="table_spacer_2"></div>
                   <table id="gantt_items"></div>
                       <thead>
                           <th>Task Name</th>
                           <th>Start Date</th>
                           <th>End Date</th>
                           <th>% Done</th>
                       </thead>
                       <tbody>
                           {task_rows_str}
                       </tbody>
                   </table>
               </div>
               <div class="cont_col_2" id="main_gantt">               
                   <div class="calendarheader">
                       {svg_calendar_data}
                   </div>
                   <div class="project_view">
                       {svg_data}
                   </div>
               </div>

            </div>
            <script>{js_data}</script>
        </body>
        </html>"""
   return html

