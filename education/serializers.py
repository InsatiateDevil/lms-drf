from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from education.models import Course, Lesson, Subscription
from education.validators import validate_video_url


class LessonSerializer(serializers.ModelSerializer):
    video = serializers.URLField(validators=(validate_video_url,), required=False)

    class Meta:
        model = Lesson
        fields = ('id', 'name', 'description', 'preview', 'course', 'video', 'owner')


class CourseSerializer(serializers.ModelSerializer):
    lessons_number = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    subscription = serializers.SerializerMethodField(read_only=True)

    def get_lessons_number(self, instance):
        return instance.lessons.count()

    def get_subscription(self, instance):
        return SubscriptionSerializer().to_representation(
            Subscription.objects.filter(
                user=self.context['request'].user,
                course=instance,
                is_active=True
            ).first()
        )

    class Meta:
        model = Course
        fields = ('name', 'description', 'preview', 'lessons_number', 'lessons', 'subscription')


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = ('user', 'course')