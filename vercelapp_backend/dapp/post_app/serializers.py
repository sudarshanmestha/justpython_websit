from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    video = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "subtitle",
            "year",
            "description",
            "image",
            "video",
            "image_upload",
            "video_upload",
            "video_url",
            "link",
            "created_at",
        ]

    def get_image(self, obj):
        if obj.image_upload:
            request = self.context.get("request")

            if request:
                return request.build_absolute_uri(obj.image_upload.url)

            return obj.image_upload.url

        return None

    def get_video(self, obj):
        request = self.context.get("request")

        # Uploaded video
        if obj.video_upload:
            if request:
                return request.build_absolute_uri(obj.video_upload.url)

            return obj.video_upload.url

        # External video URL
        if obj.video_url:
            return obj.video_url

        return None