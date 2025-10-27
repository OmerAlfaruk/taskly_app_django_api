from rest_framework import serializers

from .models import House

class HouseSerializer(serializers.ModelSerializer):
    
    member_count=serializers.IntegerField(read_only=True)
    members =serializers.HyperlinkedRelatedField(read_only=True,many=True,view_name='profile-detail')
    manager=serializers.HyperlinkedRelatedField(read_only=True,many=False,view_name='profile-detail')
    tasklists=serializers.HyperlinkedRelatedField(read_only=True,many=True,view_name='tasklist-detail',source='lists')
    
    class Meta:
        model = House
        fields =['id','url','name','image','created_at','description','member_count','members','manager','points','tasklists','completed_task','not_completed_task']
        read_only_fields=['id','created_at','points','completed_task','not_completed_task']