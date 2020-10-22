from django.contrib.auth.models import User
from rest_framework import serializers
from main.models import SubCategory, Tutorial


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']


class SubCategorySerializer(serializers.ModelSerializer):
    course_count = serializers.SerializerMethodField('get_course_count')

    class Meta:
        model = SubCategory
        fields = '__all__'

    def get_course_count(self, obj):
        return obj.tutorial_set.all().count()


class TutorialSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    
    class Meta:
        model = Tutorial
        fields = '__all__'

    