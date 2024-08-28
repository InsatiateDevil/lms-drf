from rest_framework import viewsets, generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from education.models import Course, Lesson, Subscription
from education.paginators import CustomPaginator
from education.permissions import IsOwner, IsModer
from education.serializers import CourseSerializer, LessonSerializer, \
    SubscriptionSerializer
from users.services import create_stripe_product
from education.tasks import subscribers_notification


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CustomPaginator

    def perform_create(self, serializer):
        course = serializer.save()
        stripe_product_id = create_stripe_product(course.name)
        serializer.save(owner=self.request.user, stripe_product_id=stripe_product_id)

    def perform_update(self, serializer):
        course = serializer.save()
        subscribers_notification.delay(course_id=course.id)


    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModer,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModer | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (IsOwner | ~IsModer,)
        return super().get_permissions()


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, ~IsModer)

    def perform_create(self, serializer):
        lesson = serializer.save()
        stripe_product_id = create_stripe_product(lesson.name)
        serializer.save(owner=self.request.user, stripe_product_id=stripe_product_id)


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = CustomPaginator

    def get_queryset(self):
        queryset = Lesson.objects.all()
        if self.request.user.groups.filter(name='moderation').exists():
            return queryset
        return queryset.filter(owner=self.request.user)


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonDestroyAPIView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsOwner)


class SubscriptionAPIView(APIView):
    serializer_class = SubscriptionSerializer

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course")
        course_item = get_object_or_404(Course, pk=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = "Подписка удалена"
            data = {
                "message": message,
                "subscription": "Объект удален"
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            subscription = Subscription.objects.create(user=user, course=course_item)
            message = "Подписка добавлена"
            subscription = SubscriptionSerializer().to_representation(subscription)
            data = {
                "message": message,
                "subscription": subscription
            }
            return Response(data, status=status.HTTP_201_CREATED)