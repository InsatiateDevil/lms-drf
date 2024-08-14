from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from education.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = ('name', 'description', 'preview', 'course', 'video')


class CourseSerializer(serializers.ModelSerializer):
    lessons_number = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_lessons_number(self, instance):
        return instance.lessons.count()

    class Meta:
        model = Course
        fields = ('name', 'description', 'preview', 'lessons_number', 'lessons')
