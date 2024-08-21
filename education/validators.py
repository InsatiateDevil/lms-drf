from rest_framework.serializers import ValidationError

allowed_video_hosts = ['youtube.com']

def validate_video_url(value):
    for allowed_video_host in allowed_video_hosts:
        if allowed_video_host in value:
            return value
    raise ValidationError('Неразрешенный источник видео')