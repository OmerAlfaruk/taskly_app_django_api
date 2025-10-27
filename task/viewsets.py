from rest_framework import viewsets,mixins,response,filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import AttachmentSerializer, TaskListSerializer, TaskSerializer
from .models import TaskList,Task,Attachment,COMPLETE,NOT_COMPLETE
from .permissions import IsAllowedToEditTaskListOrNone, IsAllowedToEditTaskOrNone,IsAllowedToEditAttachmentsOrReadOnly
from rest_framework.decorators import action
from django.utils import timezone
from rest_framework import status as s

class TaskListViewSet(mixins.CreateModelMixin,
mixins.ListModelMixin,
mixins.RetrieveModelMixin,
mixins.UpdateModelMixin,
mixins.DestroyModelMixin,
viewsets.GenericViewSet):
    permision_classes=[IsAllowedToEditTaskListOrNone]
    queryset=TaskList.objects.all()
    serializer_class=TaskListSerializer
    
    
    
class TaskViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAllowedToEditTaskOrNone]
    queryset=Task.objects.all()
    serializer_class=TaskSerializer
    filter_backends=[filters.SearchFilter,DjangoFilterBackend]
    search_fields=['name','status']
    filterset_fields=['status','task_list']
    search_fields=['name','status']
    def get_queryset(self):
        queryset= super(TaskViewSet,self).get_queryset()
        user_profile=self.request.user.profile
        updated_queryset=queryset.filter(created_by=user_profile);
        return updated_queryset
    
    @action(detail=True,methods=['patch'])
    def update_status(self,request,pk=None):
        try:
            task=self.get_object()
            profile=request.user.profile
            status=request.data['status']
            if (status== NOT_COMPLETE):
                if (task.status==COMPLETE):
                    task.status=NOT_COMPLETE
                    task.completed_by=None
                    task.completed_on=None
                else:
                    raise Exception("Tasks is already marked as not complete")
            elif(status==COMPLETE):
                if(task.status==NOT_COMPLETE):
                    task.status=COMPLETE
                    task.completed_on=timezone.now()
                    task.completed_by=profile
                else:
                    raise Exception("Tasks is already marked as complete")
            else:
                Exception("Tasks is already marked as complete")
                
            task.save()
            
            serializer=TaskSerializer(instance=task,context={'request':request})
            
            return response.Response(serializer.data,status=s.HTTP_200_OK)
        except Exception as e:
            return response.Response({'detail':str(e)},status=s.HTTP_400_BAD_REQUEST)
            
           
    
    
class AttachmentViewSet(mixins.CreateModelMixin,
mixins.RetrieveModelMixin,
mixins.DestroyModelMixin,viewsets.GenericViewSet):
    permission_classes=[IsAllowedToEditAttachmentsOrReadOnly]
    queryset=Attachment.objects.all()
    serializer_class=AttachmentSerializer
    
    
    
