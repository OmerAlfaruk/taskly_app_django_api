from background_task import background
from background_task.tasks import Task as BT
from house.models import House
from task.models import COMPLETE

@background(schedule=10)
def calculate_house_status():
    for house in House.objects.all():
        total_task = 0
        completed_task_count = 0

       
        for task_list in house.lists.all():
            total_task += task_list.tasks.count()
            completed_task_count += task_list.tasks.filter(status=COMPLETE).count()

        house.completed_task = completed_task_count
        house.not_completed_task = total_task - completed_task_count
        house.save()
