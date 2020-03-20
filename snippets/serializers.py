from rest_framework import serializers
from snippets.models import Snippet,LANGUAGE_CHOICES,STYLE_CHOICES
from django.contrib.auth.models import User


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight',format='html')

    class Meta:
        model = Snippet
        fields = ['url','code','linenos','owner','title','id','highlight','language','style']

    def create(self,validated_data):
        """
        create and return a new 'snippet' instance , given the validated data.
        """
        return Snippet.objects.create(**validated_data)

    def update(self,instance,validated_data):
        """
        update and return an existing 'snippet' instance ,given the validated data.
        """
        instance.title = validated_data.get('title',instance.title)
        instance.code = validated_data

class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(many=True,view_name='snippet-detail',read_only=True)
    
    class Meta:
        model = User
        fields = ['url','id','username','snippets']

    def create(self,validated_data):
        """
        create and return a new 'user' instance , given the validated data.
        """
        return User.objects.create(**validated_data)

    def update(self,instance,validated_data):
        """
        update and return an existing 'snippet' instance, given the validated data.
        """
        instance.username = validated_data.get('username',instance.username)