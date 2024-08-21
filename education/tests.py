from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from education.models import Lesson, Course, Subscription
from users.models import User


class LessonTestCaseIsOwner(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="owner@owner.com")
        self.course = Course.objects.create(name="Мастера-зайтеники", description="Доктор Стоун",
                                            owner=self.user)
        self.lesson = Lesson.objects.create(name="Урок 1", description="Основы",
                                            course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("education:lesson_detail", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data["name"], self.lesson.name
        )

    def test_lesson_create(self):
        url = reverse("education:lesson_create")
        data = {
            "name": "Урок 2",
            "description": "Подбор хороших материалов для обшивки космического корабля",
            "course": self.course.pk,
            "owner": self.user.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Lesson.objects.all().count(), 2
        )

    def test_lesson_update(self):
        url = reverse("education:lesson_update", args=(self.lesson.pk,))
        data = {
            "name": "Измененный заголовок",
        }
        response = self.client.patch(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            Lesson.objects.get(pk=self.lesson.pk).name, "Измененный заголовок"
        )

    def test_lesson_delete(self):
        url = reverse("education:lesson_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Lesson.objects.all().count(), 0
        )

    def test_lesson_list(self):
        url = reverse("education:lesson_list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "name": self.lesson.name,
                    "description": self.lesson.description,
                    "preview": None,
                    "video": None,
                    "course": self.lesson.course.pk,
                    "owner": self.lesson.owner.pk
                },
            ]
        }
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data, result
        )


class LessonTestCaseNotOwner(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="notowner@notowner.com")
        self.course = Course.objects.create(name="Мастера-затейники", description="Доктор Стоун", )
        self.lesson = Lesson.objects.create(name="Урок 1", description="Основы",
                                            course=self.course,)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("education:lesson_detail", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN
        )

    def test_lesson_create(self):
        url = reverse("education:lesson_create")
        data = {
            "name": "Урок 2",
            "description": "Подбор хороших материалов для обшивки космического корабля",
            "course": self.course.pk,
            "owner": self.user.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Lesson.objects.all().count(), 2
        )

    def test_lesson_update(self):
        url = reverse("education:lesson_update", args=(self.lesson.pk,))
        data = {
            "name": "Изменненный заголовок",
        }
        response = self.client.patch(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN
        )
        self.assertEqual(
            Lesson.objects.get(pk=self.lesson.pk).name, "Урок 1"
        )

    def test_lesson_delete(self):
        url = reverse("education:lesson_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_403_FORBIDDEN
        )
        self.assertEqual(
            Lesson.objects.all().count(), 1
        )

    def test_lesson_list(self):
        url = reverse("education:lesson_list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 0,
            "next": None,
            "previous": None,
            "results": []
        }

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data, result
        )


class LessonTestCaseIsAnonymous(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="notowner@notowner.com")
        self.course = Course.objects.create(name="Мастера-затейники", description="Доктор Стоун", )
        self.lesson = Lesson.objects.create(name="Урок 1", description="Основы",
                                            course=self.course,)

    def test_lesson_retrieve(self):
        url = reverse("education:lesson_detail", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED
        )

    def test_lesson_create(self):
        url = reverse("education:lesson_create")
        data = {
            "name": "Урок 2",
            "description": "Подбор хороших материалов для обшивки космического корабля",
            "course": self.course.pk,
            "owner": self.user.pk,
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED
        )
        self.assertEqual(
            Lesson.objects.all().count(), 1
        )

    def test_lesson_update(self):
        url = reverse("education:lesson_update", args=(self.lesson.pk,))
        data = {
            "name": "Изменненный заголовок",
        }
        response = self.client.patch(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED
        )
        self.assertEqual(
            Lesson.objects.get(pk=self.lesson.pk).name, "Урок 1"
        )

    def test_lesson_delete(self):
        url = reverse("education:lesson_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED
        )
        self.assertEqual(
            Lesson.objects.all().count(), 1
        )

    def test_lesson_list(self):
        url = reverse("education:lesson_list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 0,
            "next": None,
            "previous": None,
            "results": []
        }

        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED
        )


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@sky.pro")
        self.course = Course.objects.create(name="Мастера-зайтейники", description="Доктор Стоун",
                                            owner=self.user)
        self.lesson = Lesson.objects.create(name="Урок 1", description="Сбор материалов",
                                            course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_subscription_create(self):
        url = reverse("education:subscriptionapi")
        data = {
            "course": self.course.pk,
            "user": self.user.pk,
        }
        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            response.data.get("message"), "Подписка добавлена"
        )

    def test_subscription_delete(self):
        url = reverse("education:subscriptionapi")
        Subscription.objects.create(user=self.user, course=self.course)
        data = {
            "course": self.course.pk,
            "user": self.user.pk,
        }
        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            response.data.get("message"), "Подписка удалена"
        )


class SubscriptionTestCaseIsAnonymous(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="admin@sky.pro")
        self.course = Course.objects.create(name="Мастера-зайтейники", description="Доктор Стоун",
                                            owner=self.user)
        self.lesson = Lesson.objects.create(name="Урок 1", description="Сбор материалов",
                                            course=self.course, owner=self.user)

    def test_subscription_create(self):
        url = reverse("education:subscriptionapi")
        data = {
            "course": self.course.pk,
            "user": self.user.pk,
        }
        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED
        )

    def test_subscription_delete(self):
        url = reverse("education:subscriptionapi")
        Subscription.objects.create(user=self.user, course=self.course)
        data = {
            "course": self.course.pk,
            "user": self.user.pk,
        }
        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code, status.HTTP_401_UNAUTHORIZED
        )