"""
Core of simple-scheduler
"""
from datetime import date, timedelta, datetime
import logging
from typing import List, Dict, Tuple
from abc import ABC, abstractmethod
import pandas as pd
import math
from dateutil.parser import parse
from coopgantt.rendering.coloring import random_color
from coopgantt.enums import ActivityStatus, ScheduleMethod
from coopgantt.exceptions import IncompleteOperationError

ONE_DAY = timedelta(days=1)
WEEKEND_DAYS = [5, 6]

class Resource:
    """
    Resource for the gantt chart. I.E., a person.
    """
    def __init__(self, name, chart=None, capacity: int = 1, color = None):
        """
        Configure required resource attributes
        """
        self.name = name
        self.activities = []
        self.capacity = capacity

        self.chart = None
        self.set_chart(chart)

        # Drawing info
        self.color = color if color else random_color()

    @classmethod
    def from_dict(cls, dict: Dict):

        dict = cls._clean_resource_dict(dict)

        name = dict['resource']
        capacity = dict['capacity']
        return Resource(name, capacity=capacity, color=random_color())

    @staticmethod
    def _clean_resource_dict(dict: Dict) -> Dict:
        resource = dict.get('resource', None)
        if resource is None:
            raise ValueError(f"The field 'resource' must be provided in dataset")

        capacity = dict.get('capacity', None)
        if capacity is None:
            raise ValueError(f"The field 'capacity' must be provided in dataset")
        else:
            try:
                capacity = int(capacity)
            except:
                raise ValueError(f"Error converting the input value {capacity} to type int")

        return {
            'resource': resource,
            'capacity': capacity
        }




    def set_chart(self, chart):
        """
        Assigns task to given chart. Ensures chart has us included in their list.
        """
        old_chart = self.chart
        self.chart = chart
        if old_chart != chart and self.chart is not None:
            self.chart.add_resource(self)

    def add_activity(self, activity):
        """
        Adds the given task to this resource so it knows what it's working on.
        """
        if activity not in self.activities:
            self.activities.append(activity)
            activity.add_resource(self)

    def n_used(self, date, project_names: List[str] = None):

        if project_names is None:
            project_names = [project.name for project in self.chart.projects]

        return len([task for task in self.activities if task.is_scheduled
                                                    and task.start_date <= date <= task.end_date
                                                    and task.project.name in project_names])

    def is_free(self, date):
        """
        Determines if the resource is available to work on the given day
        """
        if self.n_used(date) < self.capacity:
            return True

        return False


    def __str__(self):
        """
        Basic resource info
        """
        return '{} with {} tasks'.format(self.name, len(self.activities))

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return type(other) == Resource and other.__hash__() == self.__hash__()

class Gantt:
    """
    Builds gantt charts.

    This is designed to be a basic utility to help estimate schedules and provide a projected
    timeline for a project. As such, not all features like exact start and end dates are supported;
    instead, tasks ask for duration and follow these rules:
        - A resource (person) can never be doing two things at once
        - All dependencies must be complete before a task can begin
        - All tasks are measurable in days
        - Tasks are ordered on the chart top-to-bottom in the order they were added to projects

    Currently, vacations/unavailability for resources is not supported and only a single project
    may be added to a chart.
    """
    def __init__(self, name, non_weekend_skipped_days: List[date] = None, work_weekends: bool = False):
        self.name = name
        self.projects = []
        self.resources = []

        self._non_weekend_skipped_days = non_weekend_skipped_days if non_weekend_skipped_days else []
        self.work_weekends = work_weekends
        self.color = '#FF3030'


    @classmethod
    def gantt_from_listdict(cls, name: str, tasks_listdict: List[Dict], resources_dict: Dict[str, Resource]=None):
        chart = Gantt(name)

        if resources_dict is None:
            resources_dict = {}

        activities = {}
        projects = {}
        dependency_map = {}

        tasks = cls._clean_input_data(tasks_listdict)

        # Create all the tasks
        for row in tasks:
            # Add new resources as encountered
            task_resources = []
            for r in row['resources']:
                if r.name not in resources_dict:
                    resources_dict[r.name] = r
                task_resources.append(resources_dict[r.name])

            # Add new project as encountered
            project = row['project']
            if project not in projects.keys():
                proj_obj = Project(project)
                projects[project] = proj_obj
                chart.add_project(proj_obj)

            # Add new dependencies as encountered
            dependency_map[row['id']] = row['dependencies']

            # Create the task and/or milestone for the gannt
            if row['activity_type'] == 'Task':
                activities[row['id']] = Task(
                    id=row['id'],
                    name=row['activity'],
                    duration=row['duration_days'],
                    resources=task_resources,
                    project=projects[project],
                    dont_start_before_date=row['dont_start_before_date'],
                    actual_start_date=row['actual_start_date'],
                    target_completion_date=row['target_completion_date'],
                    closed_date=row['closed_date'],
                    perc_done=row['perc_done'],
                    priority=row['priority'],
                    status=row['state'],
                    sub_activities=row['sub_activities'],
                    scheduled_start_date=row['scheduled_start_date']
                )
            elif row['ActivityType'] == 'Milestone':
                activities[row['id']] = Milestone(
                    id=row['id'],
                    name=row['Activity'],
                    dont_start_before_date=row['dont_start_before_date'],
                    actual_start_date=row['ActualStart'],
                    target_completion_date=row['TargetDate'],
                    closed_date=row['ClosedDate'],
                    resources=task_resources,
                    project=projects[project],
                    done=True if row['perc_done'] >= 100 else False,
                    status=row['state'],
                    sub_activities=row['sub_activities'],
                    scheduled_start_date=row['scheduled_start_date']
                )

        # set all the dependencies on created items from the created dependency map
        for id, dependency_ids in dependency_map.items():
            activities[id].dependencies = [activities[dependency_id] for dependency_id in dependency_ids
                                           if dependency_id in activities.keys()]

        # add the resources to the gannt from the resource dict
        for r in resources_dict:
            chart.add_resource(resources_dict[r])

        return chart

    @staticmethod
    def _clean_input_data(data: List[Dict]) -> List[Dict]:
        clean_tasks_data = []

        # Create listdict of tasks
        for row in data:

            # Determine state and skip if the item is in removed status
            provided_state = row['state']
            state = None
            if provided_state == "Blocked":
                state = ActivityStatus.Blocked
            elif provided_state == "Active":
                state = ActivityStatus.InProgress
            elif provided_state == "Removed":
                continue

            # resources
            task_resources = []
            for r in row['resources'].split('&&'):
                task_resources.append(Resource(r, color=random_color()))

            # Add new project as encountered
            project = row['project']

            # Add new dependencies as encountered
            row_dependency_list = row['dependencies'].split('&&') if row['dependencies'] != '' else []

            # sub activities
            # TODO: Add validation around the structure of sub activities
            sub_activities = eval(row['sub_activities'])

            # Duration
            feature_duration = math.ceil(float(row['duration_days'])) if row['duration_days'] is not '' else 1
            us_duration = sum([math.ceil(float(sub_activity.get('duration_days', 0)) if sub_activity.get('duration_days', 0) is not '' else 0)
                               for sub_activity in sub_activities])

            duration = max(feature_duration, us_duration)

            # Dates
            dont_start_before_date = parse(row['dont_start_before_date']).date() if row['dont_start_before_date'] != "" else None
            actual_start_date = parse(row['actual_start_date']).date() if row['actual_start_date'] != "" else None
            target_completion_date = parse(row['target_completion_date']).date() if row['target_completion_date'] != "" else None
            closed_date = parse(row['closed_date']).date() if row['closed_date'] != "" else None
            scheduled_start_date = parse(row['scheduled_start_date']).date() if row['scheduled_start_date'] != "" else None

            # Percent Complete
            perc_done = row['perc_done'] if row['perc_done'] != "" else 0
            priority = int(float(row['priority'])) if row['priority'] != "" else 999

            # Task Type
            if row['activity_type'] == 'Task':
                activity_type = 'Task'
            elif row['activity_type'] == 'Milestone':
                activity_type = 'Milestone'
            else:
                raise NotImplementedError(f"The provided ActivityType {row['activity_type']} was not recognized")

            # add
            clean_tasks_data.append({
                'id': row['id'],
                'activity_type': activity_type,
                'activity': row['activity'],
                'state': state,
                'resources': task_resources,
                'duration_days': duration,
                'project': project,
                'dont_start_before_date': dont_start_before_date,
                'actual_start_date': actual_start_date,
                'target_completion_date': target_completion_date,
                'scheduled_start_date': scheduled_start_date,
                'closed_date': closed_date,
                'perc_done': perc_done,
                'priority': priority,
                'sub_activities': sub_activities,
                'dependencies': row_dependency_list
            })

        return clean_tasks_data


    def add_project(self, project):
        """
        Adds the given project to the chart
        """
        if project not in self.projects:
            self.projects.append(project)
            project.set_chart(self)

    def add_resource(self, resource):
        """
        Adds the given resource to the gantt chart
        """
        if resource not in self.resources:
            self.resources.append(resource)
            resource.set_chart(self)

    def date_skipped(self, date: date):
        if date in self._non_weekend_skipped_days or date.weekday() in self.weekend_days:
            return True
        else:
            return False

    @property
    def non_weekend_skipped_days(self):
        return self._non_weekend_skipped_days

    @property
    def weekend_days(self):
        """
        Returns weekdays that are NEVER worked (weekends).

        Can be disabled via chart.work_weekends = True
        """
        if self.work_weekends:
            return []
        else:
            return WEEKEND_DAYS

    @property
    def end_date(self):
        """
        Returns the final date any tasks will be performed.
        """
        end_date = None
        for t in self.tasks:
            if end_date is None or t.end_date > end_date:
                end_date = t.end_date
        return end_date

    @property
    def start_date(self):
        """
        Returns the final date any tasks will be performed.
        """
        start_date = None
        for t in self.tasks:
            if start_date is None or t.start_date < start_date:
                start_date = t.start_date
        return start_date

    @property
    def tasks(self):
        """
        Returns an iterator for all tasks under all projects
        """
        for proj in self.projects:
            for t in proj.activities:
                yield t

    def calculate_schedule(self,
                           start_date,
                           max_resources_per_project: Dict[str, Dict[str, int]] = None,
                           project_priority: Dict[str, int] = None,
                           schedule_method: ScheduleMethod = None,
                           defined_schedule_sequence: Dict[str, int] = None):
        """
        Calculates the start and end dates of each task. Do activities with actual dates prior to w.o actual dates.
        This prevents the algo from assigning a resource that is committed to a task with an actual date simply because
        it was provided first

        :param: schedule_method ScheduleMethod: defines how the scheduling algorithm will behave. Different types result
        in different schedules based on the user's prioritization concerns

        :param defined_schedule_sequence Dict[wi_id: str, sequence: int]: necessary if the schedule_method is
        ScheduleMethod.DEFINED_SEQUENCE. Defines the sequence in which to perform the scheduling routine. Note that if
        an item is a predecessor of an item with an earlier sequence, the predecessor relationship will still be honored.
        Tasks without values in the defined_schedule_sequence will be scheduled last and in project_priority order.
        Final sort order is FIFO
        """

        # start by honoring any task with an actual_start_date
        self.set_schedule_for_activities_with_actual_start(start_date)

        # Default to ScheduleMethod.PRIORITY
        if schedule_method is None:
            schedule_method = ScheduleMethod.PRIORITY

        # Switch on ScheduleMethod
        if schedule_method == ScheduleMethod.PRIORITY:
            self.schedule_by_priority(start_date, max_resources_per_project, project_priority)
        elif schedule_method == ScheduleMethod.EARLIEST_DUE_DATE:
            self.schedule_by_earliest_due_date(start_date, max_resources_per_project, project_priority)
        elif schedule_method == ScheduleMethod.DEFINED_SEQUENCE:
            self.schedule_by_defined_sequence(start_date, defined_schedule_sequence, max_resources_per_project, project_priority)
        else:
            raise NotImplementedError(f"The provided schedule method [{schedule_method}] is not understood for scheduling")

        # Raise error if any task ends up not scheduled
        shouldnt_be_left = self.activities_not_scheduled
        if any(shouldnt_be_left):
            raise IncompleteOperationError(f"The following {len(shouldnt_be_left)} activities were not scheduled: [{shouldnt_be_left}]")
    @property
    def flattened_tasks_across_projects(self):
        #create a list of activities sorted on their relative priority
        activities = [proj.activities for proj in self.projects]
        flat_list = []
        for sublist in activities:
            for item in sublist:
                flat_list.append(item)

        return flat_list

    @property
    def activities_with_actual_starts(self):
        flat_list = self.flattened_tasks_across_projects
        return [x for x in flat_list if x.actual_start_date is not None]

    @property
    def activities_not_scheduled(self):
        flat_list = self.flattened_tasks_across_projects
        return [x for x in flat_list if x.start_date is None]

    def set_schedule_for_activities_with_actual_start(self, start_date):
        actual_start_activities = self.activities_with_actual_starts

        for item in actual_start_activities:
            item.schedule(start_date, {})

    def schedule_by_earliest_due_date(self,
                                     start_date,
                                     max_resources_per_project: Dict[str, Dict[str, int]] = None,
                                     project_priority: Dict[str, int] = None):
        if project_priority is None:
            project_priority = {}

        # Get all activities that have a set target date
        activities_with_target_date = [x for x in self.activities_not_scheduled if x.target_completion_date is not None]

        # Sort by target date
        activities_with_target_date.sort(key=lambda x: x.target_completion_date)

        # Schedule items in target_date order. Will also appropriately schedule pre-decessors
        for item in activities_with_target_date:
            item.schedule(start_date, max_resources_per_project.get(item.project.name, None))

        # Get remaining tasks left unscheduled
        remaining_unscheduled = self.activities_not_scheduled

        # Sort by priority (Multiply by project priority)
        remaining_unscheduled.sort(key=lambda x: x.priority * project_priority.get(x.project.name, 10))

        # Schedule remaining
        for item in remaining_unscheduled:
            item.schedule(start_date, max_resources_per_project.get(item.project.name, None))


    def schedule_by_priority(self,
                             start_date,
                             max_resources_per_project: Dict[str, Dict[str, int]] = None,
                             project_priority: Dict[str, int] = None):
        if project_priority is None:
            project_priority = {}

        # Get all items not scheduled (only scheduled should be items with actual_start_date
        needs_scheduled = self.activities_not_scheduled

        #Multiply the task priority by the project priority for an "Overall" priority
        needs_scheduled.sort(key=lambda x: x.extrapolated_priority * project_priority.get(x.project.name, 10))

        # Schedule remaining
        for item in needs_scheduled:
            item.schedule(start_date, max_resources_per_project.get(item.project.name, None))

    def schedule_by_defined_sequence(self,
                             start_date,
                             defined_schedule_sequence: Dict[str, int],
                             max_resources_per_project: Dict[str, Dict[str, int]] = None,
                             project_priority: Dict[str, int] = None,
                            ):
        if defined_schedule_sequence is None:
            raise ValueError(f"the parameter defined_schedule_sequence cannot be None when scheduling using ScheduleMethod.DEFINED_SEQUENCE")

        if project_priority is None:
            project_priority = {}

        # Get all items not scheduled (only scheduled should be items with actual_start_date
        needs_scheduled = self.activities_not_scheduled

        # Sort needs scheduled first by presence of a value in defined_schedule_sequence, then by that value (None's last)
        # Note: Sorting by a Tuple. False<True. key=lambda x: (x is None, x)  --> https://stackoverflow.com/questions/18411560/python-sort-list-with-none-at-the-end
        needs_scheduled.sort(key=lambda x: (defined_schedule_sequence.get(x, None) is None, defined_schedule_sequence.get(x, None)))

        # Schedule items in defined_schedule order. Will also appropriately schedule pre-decessors
        for item in needs_scheduled:
            # Once hit None's, done scheduling according to definition
            if defined_schedule_sequence.get(item, None) is None:
                break
            item.schedule(start_date, max_resources_per_project.get(item.project.name, None))

        # Get remaining tasks left unscheduled
        remaining_unscheduled = self.activities_not_scheduled

        # Sort by priority (Multiply by project priority)
        remaining_unscheduled.sort(key=lambda x: x.priority * project_priority.get(x.project.name, 10))

        # Schedule remaining
        for item in needs_scheduled:
            item.schedule(start_date, max_resources_per_project.get(item.project.name, None))


    def to_csv(self, filepath: str):
        with open(filepath, 'a+') as file:
            for task in self.tasks:
                file.write(f"{task.as_csv_string()}\n")


    def as_dataframe(self) -> pd.DataFrame:
        df = pd.DataFrame()
        df['id'] = [task.id for task in self.tasks]
        df['project'] = [task.project.name for task in self.tasks]
        df['activity_group'] = [task.name.split(':')[0] if ':' in task.name else 'NA' for task in self.tasks]
        df['activity'] = [task.name for task in self.tasks]
        df['activity_type'] = [type(task).__name__ for task in self.tasks]
        df['actual_start_date'] = [task.actual_start_date for task in self.tasks]
        df['dont_start_before_date'] = [task.dont_start_before_date for task in self.tasks]
        df['target_completion_date'] = [task.target_completion_date for task in self.tasks]
        df['closed_date'] = [task.closed_date for task in self.tasks]
        df['duration_days'] = [task.duration for task in self.tasks]
        df['expected_duration_remaining'] = [(100 - task.percent_done) * task.duration / 100.0 for task in self.tasks]
        df['resources'] = ['&&'.join([resource.name for resource in task.resources]) for task in self.tasks]
        df['perc_done'] = [task.percent_done for task in self.tasks]
        df['dependencies'] = ['&&'.join([dependency.id for dependency in task.dependencies]) for task in self.tasks]
        df['priority'] = [task.priority for task in self.tasks]
        df['scheduled_start_date'] = [task._start_date for task in self.tasks]
        df['scheduled_end_date'] = [task.end_date for task in self.tasks]
        df['state'] = [task.calculated_status.name for task in self.tasks]
        df['sub_activity_summary'] = [task.sub_activity_summary() for task in self.tasks]
        df['sub_activities'] = [task._sub_activities for task in self.tasks]

        df.sort_values(by=['scheduled_start_date'], ascending=True, inplace=True)

        return df

    def __str__(self):
        """
        Display info on all projects under us
        """
        s = 'Chart {} starts {}, {} resources\nProjects:'.format(self.name, self.start_date, len(self.resources))
        for p in self.projects:
            s += '\n' + str(p)
        return s


class Project:
    """
    Collects tasks
    """
    def __init__(self, name, chart=None):
        self.name = name

        self.activities = []


        self.chart = None
        self.set_chart(chart)

    def set_chart(self, chart):
        """
        Assigns task to given chart. Ensures chart has us included in their list.
        """
        old_chart = self.chart
        self.chart = chart
        if old_chart != chart and self.chart is not None:
            self.chart.add_project(self)

    def add_activity(self, activity):
        """
        Adds the given activity to the project
        """
        self.activities.append(activity)
        activity.set_project(self)

    @property
    def start_date(self):
        """
        First date a task under this project will be performed
        """
        start_date = None
        for t in self.activities:
            if start_date is None or start_date > t.start_date:
                start_date = t.start_date

        return start_date

    @property
    def end_date(self):
        """
        Last date a task under this project will be performed
        """
        end_date = None
        for t in self.activities:
            if end_date is None or end_date < t.end_date:
                end_date = t.end_date

        return end_date


    def resources_on_date(self, check_date):
        return {resource.name: resource.n_used(check_date, self.name) for resource in self.chart.resources}



    def __str__(self):
        """
        Displays info on all tasks
        """
        s = 'Project {} with {} activities:'.format(self.name, len(self.activities))
        for t in self.activities:
            s += '\n' + str(t)
        return s

    def __eq__(self, other):
        if isinstance(other, Project) and other.name == self.name:
            return True
        else:
            return False




class ScheduledActivity(ABC):
    """
    Activity in Project
    """
    def __init__(self,
                 id:int,
                 name:str,
                 dont_start_before_date:date=None,
                 actual_start_date:date=None,
                 target_completion_date: date = None,
                 closed_date: date = None,
                 resources:List[Resource]=None,
                 dependencies=None,
                 project:Project=None,
                 perc_done:int=0,
                 duration:int=None,
                 priority:int=999,
                 status: ActivityStatus = None,
                 sub_activities: List[Dict[str, str]] = None, # Dict to include id, type, state, activatedDate, closedDate
                 scheduled_start_date: date = None
    ):

        """
        Sets the basic attributes of a task
        """
        if resources is None:
            resources = []

        if dependencies is None:
            dependencies = []

        self.resources = []
        for r in resources:
            self.add_resource(r)

        self.id = id
        self.name = name
        self.dont_start_before_date = dont_start_before_date
        self.actual_start_date = actual_start_date
        self.target_completion_date = target_completion_date
        self.closed_date = closed_date

        self.project = None
        self.set_project(project)
        self._dependencies = None
        self._successors = []
        self.duration = duration
        self.priority = priority

        self._start_date = scheduled_start_date if scheduled_start_date else None
        self.percent_done = float(perc_done)

        self._status = status
        self._sub_activities = sub_activities if sub_activities else []


    @property
    def dependencies(self):
        return self._dependencies

    @dependencies.setter
    def dependencies(self, dependants: List):
        self._dependencies = dependants
        for obj in dependants:
            obj.add_successors([obj])

    @property
    def successors(self):
        return self._successors

    def add_successors(self, successors: List):
        self._successors += successors

    def set_project(self, project):
        """
        Assigns task to given project. Ensures project has us included in their list.
        """
        old_proj = self.project
        self.project = project
        if old_proj != project and self.project is not None:
            self.project.add_activity(self)

    def add_resource(self, resource):
        """
        Assigns task to given project. Ensures project has us included in their list.
        """
        if resource not in self.resources:
            self.resources.append(resource)
            resource.add_activity(self)

    def clear_schedule(self):
        """
        Clears any cached scheduling information
        """
        self._start_date = None


    def first_eligible_date(self, start_date, max_resources_by_type_for_project: Dict[str, int]):
        # Resource deconfliction
        attempted_start_date = start_date
        date_is_valid = False
        while not date_is_valid:
            # dont consider the start date if its skipped
            if self.project.chart.date_skipped(attempted_start_date):
                attempted_start_date += ONE_DAY
                continue

            date_is_valid = True
            check_date = attempted_start_date
            checked_days = 0

            # Check dates in duration starting at attempted_start_date to see if resources are free
            while date_is_valid and checked_days < self.duration:    # check_date < attempted_start_date + timedelta(days=self.duration):
                # Dont evaluate on skipped days
                if self.project.chart.date_skipped(check_date):
                    check_date += ONE_DAY
                    continue

                # Check if resources are free on this day
                project_resources_on_date = self.project.resources_on_date(check_date)
                for resc in self.resources:
                    resources_used = project_resources_on_date[resc.name]

                    resources_at_over_capacity = resources_used >= max_resources_by_type_for_project.get(resc.name, resources_used+1) if max_resources_by_type_for_project else False


                    if not resc.is_free(check_date) or resources_at_over_capacity:
                        date_is_valid = False
                        break
                    else:
                        check_date += ONE_DAY
                        checked_days += 1

            if not date_is_valid:
                attempted_start_date += ONE_DAY

        return attempted_start_date


    def build_header(self, include_id: bool = True):
        if include_id:
            return f"{self.id} - {self.name}"
        else:
            return self.name

    def schedule(self, start_date, max_resources_by_type_for_project: Dict[str, int]):
        """
        Schedule ourselves based on other tasks and resource availability

        General algorithm:
            0. If activity has an "actual start" -> use that value
            1. Try first date immediately after dependency
                1a. If no dependency, use chart start date
            2. Keep advancing date until first free date
        """
        self.clear_schedule()

        if self.actual_start_date is not None:
            self._start_date = self.actual_start_date
            return

        if self.dont_start_before_date is not None:
            schedule_start_date = max(self.dont_start_before_date, start_date)
        else:
            schedule_start_date = start_date

        # TODO: The below loop is not optimized. Works fine "small" to "medium" gantts, but would start to crash in huge
        #   ones. Recursiveness helps this get closer to O(n), but the first_eligible_date() calculation is redone every
        #   activity. There is opportunity to cache some information into a comparison matrix for quick lookups

        # Dependencies
        for activity in self.dependencies:
            if not activity.is_scheduled:
                activity.schedule(start_date, max_resources_by_type_for_project)

            '''Update so self wont schedule until after the end of the dependency'''
            if activity.end_date >= start_date:
                schedule_start_date = max(activity.end_date + ONE_DAY, schedule_start_date)

        # Calculated Start Based on Completion
        if self.percent_done >0 and self.percent_done < 100:
            self._start_date = self.beg_date_on_completion
            return
        elif math.isclose(self.percent_done, 0):
            schedule_start_date = max(schedule_start_date, datetime.today().date())

        self._start_date = self.first_eligible_date(schedule_start_date, max_resources_by_type_for_project)
        logging.debug(f'scheduled activity {self}')

    @property
    def is_scheduled(self):
        """
        Returns if this task has had a start date set
        """
        return self._start_date is not None

    @property
    def start_date(self):
        return self._start_date

    @property
    def end_date(self):
        """
        End date of task based on start and duration.

        Marks the final day work is actually performed.

        If chart is set to not work weekends, schedule will be extended to
        include extra days to compensate for Saturday and Sunday.
        """

        return self.closed_date if self.closed_date else self.end_date_estimated



        #
        # work_done = 0
        # end_date = self.start_date
        #
        # while work_done + 1 < self.duration and \
        #         (end_date < self.closed_date if self.closed_date else True):
        #     end_date += ONE_DAY
        #
        #     if not self.project.chart.date_skipped(end_date):
        #     # if end_date.weekday() not in self.project.chart.weekend_days:
        #         work_done += 1
        # return end_date

    @property
    def end_date_estimated(self):
        """"""

        """
        End date of task based on start and duration.

        If chart is set to not work weekends, schedule will be extended to
        include extra days to compensate for Saturday and Sunday.
        """
        if str(self.id) == '2267':
            deb = True

        work_done = 0
        end_date = self.start_date

        work_to_do = (1 - self.percent_done/100.0) * self.duration

        # Need to cover the following cases:
        #   a. Scheduling in the past, there is still work that hasnt been scheduled
        #   b. if there is still work to be done after reaching "today", need to keep scheduling until work is completed
        #   c. if work is done early (no more work_to_do today) need to stop scheduling for the future

        while (work_done + 1 < self.duration
                or work_to_do > 0) \
                and not (math.isclose(work_to_do, 0) and end_date + ONE_DAY > datetime.today().date()):
            end_date += ONE_DAY

            date_skipped = self.project.chart.date_skipped(end_date)
            if not date_skipped:
                work_done += 1

            if not date_skipped and end_date >= datetime.today().date():
                work_to_do = max(work_to_do - 1, 0)

        return end_date


    @property
    def beg_date_on_completion(self):
        """
        Beg date of task based on completion perc, today and duration.

        Marks the start day work is actually performed.

        """

        work_done = int(self.percent_done/100 * self.duration)
        start_date = datetime.today().date()
        while work_done > 0:
            start_date -= ONE_DAY

            if not self.project.chart.date_skipped(start_date):
                work_done -= 1
        return start_date

    @property
    def header(self):
        return self.build_header()

    @property
    def extrapolated_priority(self):
        return min(self.priority, min(x.priority for x in self.successors) if len(self.successors) > 0 else self.priority)

    @property
    def extrapolated_target_date(self):

        targets = [self.target_completion_date]
        targets += [x.target_completion_date for x in self.successors]
        return min([x for x in targets if x is not None])

    # @property
    # def

    @property
    def slack(self):
        if self.target_completion_date:
            return (self.target_completion_date - datetime.today().date()).days
        else:
            return min(x.slack for x in self.successors)


    @property
    def calculated_status(self):
        if self._status is not None:
            return self._status
        elif self.actual_start_date is not None and 0 < self.percent_done < 100:
            return ActivityStatus.InProgress
        elif not all([dependency.calculated_status == ActivityStatus.Completed for dependency in self.dependencies]):
            return ActivityStatus.ToDo
        elif math.isclose(self.percent_done, 100):
            return ActivityStatus.Completed
        elif all([dependency.calculated_status == ActivityStatus.Completed for dependency in self.dependencies]) and self.percent_done == 0:
            return ActivityStatus.Available
        else:
            return ActivityStatus.Unknown

    def as_csv_string(self):
        return f"{self.id}, " \
               f"{self.project.name}, " \
               f"{self.name}, " \
               f"{type(self).__name__}, " \
               f"{self.actual_start_date}, " \
               f"{self.dont_start_before_date}, " \
               f"{self.duration}, " \
               f"{'&&'.join([x.name for x in self.resources])}, " \
               f"{self.percent_done}, " \
               f"{'&&'.join(x.name for x in self.dependencies)}, " \
               f"{self.priority}, " \
               f"{self._start_date}"

    def sub_activity_summary(self):
        ret = {}

        act_types = [activity['type'] for activity in self._sub_activities]

        for act_type in act_types:
            states = [activity['state'] for activity in self._sub_activities if activity['type'] == act_type]
            state_agg = {}
            for state in states:
                act_by_state = [activity for activity in self._sub_activities if activity['type'] == act_type and activity['state'] == state]
                state_agg[state] = len(act_by_state)
            ret[act_type] = state_agg

        return ret

    def __repr__(self):
        return self.__str__()

class Task(ScheduledActivity):
    def __init__(self,
                 id: int,
                 name:str,
                 duration: int,
                 dont_start_before_date:date=None,
                 actual_start_date:date=None,
                 target_completion_date: date = None,
                 closed_date: date = None,
                 resources:List[Resource]=None,
                 dependencies=None,
                 project:Project=None,
                 perc_done:int=None,
                 priority:int = None,
                 status: ActivityStatus = None,
                 sub_activities: List[Dict[str, str]] = None, # Dict to include id, type, state, activatedDate, closedDate
                 scheduled_start_date: date = None
                 ):

        if duration < 1:
            raise Exception(f"Duration must be positive but {duration} was provided for [{id}]")

        super().__init__(id,
                         name,
                         dont_start_before_date=dont_start_before_date,
                         actual_start_date=actual_start_date,
                         target_completion_date = target_completion_date,
                         closed_date=closed_date,
                         resources=resources,
                         dependencies=dependencies,
                         project=project,
                         perc_done=perc_done,
                         duration=duration,
                         priority=priority,
                         status=status,
                         sub_activities=sub_activities,
                         scheduled_start_date = scheduled_start_date)

    def __str__(self):
        return '\tTask {} ({} resources, {} dependencies): {} days, {} through {} ({}%)'.format(
            self.name,
            len(self.resources),
            len(self.dependencies),
            self.duration,
            self.start_date,
            self.end_date,
            self.percent_done
        )


class Milestone(ScheduledActivity):
    def __init__(self,
                 id: int,
                 name: str,
                 dont_start_before_date: date,
                 actual_start_date:date=None,
                 target_completion_date: date = None,
                 closed_date: date = None,
                 dependencies=None,
                 resources:List[Resource] = None,
                 project:Project=None,
                 done: bool = False,
                 priority:int = None,
                 status: ActivityStatus = None,
                 sub_activities: List[Dict[str, str]] = None, # Dict to include id, type, state, activatedDate, closedDate
                 scheduled_start_date: date = None
    ):

        super().__init__(id,
                         name,
                         dont_start_before_date=dont_start_before_date,
                         actual_start_date=actual_start_date,
                         target_completion_date = target_completion_date,
                         closed_date=closed_date,
                         resources=resources,
                         dependencies=dependencies,
                         project=project,
                         duration=1,
                         priority=priority,
                         status=status,
                         sub_activities=sub_activities,
                         scheduled_start_date=scheduled_start_date )

        self.duration = 1
        self.done = done

    @property
    def done(self):
        return True if self.percent_done >=100 else False

    @done.setter
    def done(self, done: bool):
        self.percent_done = 100 if done else 0

    def set_project(self, project):
        """
        Assigns task to given project. Ensures project has us included in their list.
        """
        old_proj = self.project
        self.project = project
        if old_proj != project and self.project is not None:
            self.project.add_activity(self)

class SchedulingError(Exception):
    """
    Exceptions related to improperly configured or impossible scheduling
    """
    pass


