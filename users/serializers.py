from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.HyperlinkedRelatedField(read_only=True, view_name='user-detail')


    class Meta:
        model = Profile
        fields = ['url', 'id', 'user', 'image']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    username = serializers.CharField(read_only=True)
    old_password = serializers.CharField(write_only=True, required=False)
    profile = ProfileSerializer(read_only=True)

    def validate(self,data):
        requested_method=self.context['request'].method
        password=data.get('password',None)
        if requested_method=='POST' and not password:
            raise serializers.ValidationError({"info":"This field is required"})
        elif requested_method=='PUT' or requested_method=='PATCH':
            old_password=data.get('old_password',None)
            if password and not old_password:
                raise serializers.ValidationError({"info":"Old password is required to set a new password"})
            
        return data
    def create(self, validated_data):
        # Extract first_name and last_name from validated_data
        first_name = validated_data.get('first_name', '')
        last_name = validated_data.get('last_name', '')
        password = validated_data.pop('password', None)

        # Generate username
        username = f"{first_name}_{last_name}".lower()
        counter = 1
        original_username = username
        # Ensure unique username
        while User.objects.filter(username=username).exists():
            username = f"{original_username}{counter}"
            counter += 1

        # Add username to validated_data
        validated_data['username'] = username

        # Create user with validated_data
        user = User.objects.create_user(**validated_data)
        
        # Set password if provided
        if password:
            user.set_password(password)
            user.save()

        return user
        
        return user
    
    def update(self,instance,validated_data):
        try:
            user=instance
            if 'password' in validated_data:
                password=validated_data.pop('password')
                old_password=validated_data.pop('old_password')
                if user.check_password(old_password):
                    user.set_password(password)
                else:
                    raise Exception("Old password is incorrect")
                user.save()
        except Exception as err:
           raise serializers.ValidationError({"password":err})
        
        return super(UserSerializer,self).update(instance,validated_data)
    
    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'email', 'first_name', 'last_name', 'password', 'old_password', 'profile']
    