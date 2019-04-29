from rest_framework import serializers
from .models import Act

class ActSerializer(serializers.ModelSerializer):
    """ アカウント情報のシリアライザー """
    class Meta(object):
        model = Act
        fields = '__all__'
