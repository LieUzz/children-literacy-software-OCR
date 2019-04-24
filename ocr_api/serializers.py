from rest_framework import serializers
from . import models

class WordHistorySerializer(serializers.ModelSerializer):
    word = serializers.CharField(source='wordinfo.word')
    gif = serializers.CharField(source='wordinfo.gif')
    pinyin = serializers.CharField(source='wordinfo.pinyin')
    bihua = serializers.CharField(source='wordinfo.bihua')
    bushou = serializers.CharField(source='wordinfo.bushou')
    yisi1 = serializers.CharField(source='wordinfo.yisi1')
    yisi2 = serializers.CharField(source='wordinfo.yisi2')
    yisi3 = serializers.CharField(source='wordinfo.yisi3')


    class Meta:
        model = models.UserWordHistory
        fields = ['word', 'gif', 'pinyin','bihua','bushou','yisi1','yisi2','yisi3']