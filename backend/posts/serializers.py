from rest_framework import serializers

from users.models import CustomUser

from .models import Like, Post


class CreateUpdateDeletePostSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(
        max_length=None,
        required=False,
        allow_empty_file=False,
        use_url=True,
    )

    class Meta:
        model = Post
        exclude = ('author', )

    def create(self, validated_data):
        author = self.context.get('request').user
        post = Post.objects.create(author=author, **validated_data)
        post.save()
        return post

    def update(self, instance, validated_data):
        if validated_data.get('title'):
            instance.title = validated_data.pop('title')
        if validated_data.get('text'):
            instance.text = validated_data.pop('text')
        if validated_data.get('image'):
            instance.image = validated_data.pop('image')
        instance.save()
        return instance


class ShowPostsAuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'id')


class ShowPostSerializer(serializers.ModelSerializer):
    author = ShowPostsAuthorSerializer(read_only=True)

    class Meta:
        model = Post
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = '__all__'
