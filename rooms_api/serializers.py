from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Vote, Story, Room

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id', 'user_id', 'vote']

class StorySerializer(serializers.ModelSerializer):
    votes = VoteSerializer(many = True)

    class Meta:
        model = Story
        fields = ['id', 'name', 'votes']

class RoomSerializer(serializers.ModelSerializer):
    stories = StorySerializer(many = True)
    users = serializers.PrimaryKeyRelatedField(queryset = User.objects.all(), many = True)

    class Meta:
        model = Room
        fields = ['id', 'title', 'stories', 'step', 'created', 'updated', 'users', 'is_over']
        read_only_fields = ('created', 'updated')

    def create(self, validated_data):
        stories_data = validated_data.pop('stories', [])
        users_data = validated_data.pop('users', [])

        room = Room.objects.create(**validated_data)
        room.users.add(self.context['request'].user)

        room.users.add(*users_data)

        for story_data in stories_data:
            votes_data = story_data.pop('votes', [])
            story = Story.objects.create(**story_data)
            for vote_data in votes_data:
                Vote.objects.create(**vote_data, story=story)
            room.stories.add(story)

        return room

    def update(self, instance, validated_data):
        stories_data = validated_data.pop('stories', None)
        users_data = validated_data.pop('users', None)

        instance.title = validated_data.get('title', instance.title)
        instance.step = validated_data.get('step', instance.step)
        instance.is_over = validated_data.get('is_over', instance.is_over)
        instance.save()

        if users_data:
            instance.users.set(users_data)

        if stories_data:
            for story_data in stories_data:

                story_id = story_data.get('id')
                if story_id:
                    story = instance.stories.get(id = story_id)
                    story.name = story_data.get('name', story.name)
                    story.save()

                    votes_data = story_data.get('votes', [])
                    for vote_data in votes_data:
                        vote_id = vote_data.get('id')
                        if vote_id:
                            vote = story.votes.get(id = vote_id)
                            vote.vote = vote_data.get('vote', vote.vote)
                            vote.save()
                        else:
                            Vote.objects.create(**vote_data, story=story)
                else:
                    votes_data = story_data.pop('votes', [])
                    story = Story.objects.create(**story_data)
                    for vote_data in votes_data:
                        Vote.objects.create(**vote_data, story=story)
                    instance.stories.add(story)

        return instance