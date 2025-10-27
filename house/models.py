from django.db import models
import uuid
import os
from django.utils.deconstruct import deconstructible

@deconstructible
class GenerateHouseImagePath(object):
    def __init__(self):
        pass
    def __call__(self, instance, filename):
        ext=filename.split('.')[-1]
        path=f'media/houses/{instance.id}/images'
        name=f'main.{ext}'
        return os.path.join(path,name)
house_image_path=GenerateHouseImagePath()


class House(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4 ,editable=False)
    name=models.CharField(max_length=120)
    image=models.ImageField(upload_to=house_image_path,null=True,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    description=models.TextField()
    manager=models.OneToOneField('users.Profile',on_delete=models.CASCADE,blank=True,related_name='managed_house')
    points=models.IntegerField(default=0)
    completed_task=models.IntegerField(default=0)
    not_completed_task=models.IntegerField(default=0)
    
    class Meta:
        verbose_name_plural = "Houses"
    def __str__(self):
        return f"{self.id} {self.name} - Managed by {self.manager.user.username}"
    
    
    