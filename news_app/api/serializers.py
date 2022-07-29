# documentation
# https://www.django-rest-framework.org/api-guide/serializers/
# https://www.django-rest-framework.org/api-guide/serializers/#object-level-validation

from django.forms import ValidationError
from rest_framework import serializers
from news_app.models import Article, Journalist

from datetime import datetime
from django.utils.timesince import timesince


class SerializerArticle(serializers.ModelSerializer):
    # author = JournalistSerializer()
    time_since_publication = serializers.SerializerMethodField()
    # this gives author name insted of number.
    # author = serializers.StringRelatedField()

    class Meta:
        model = Article
        # to exclude perticular field and get rest of the fields
        exclude = ('body',)
        # fields = '__all__'  # to get all the fields of the model
        # fields = ('id',author','title')  # to get only perticular fields
        # Cannot set both 'fields' and 'exclude' options on serializer SerializerArticle.

    def get_time_since_publication(self, object):
        publication_date = object.published  # published date of the article
        now = datetime.now()
        return timesince(publication_date, now)

    # Object level validation, validation with more than one field or on multiple fields
    def validate(self, data):
        if data['title'] == data['heading']:
            raise serializers.ValidationError(
                'title and heading should be differrent')
        return data

    # field level validation, validation with in a single field
    def validate_title(self, value):
        if len(value) < 20:
            raise serializers.ValidationError(
                'title is too short')
        return value


class JournalistSerializer(serializers.ModelSerializer):
    # articles = serializers.HyperlinkedRelatedField(many=True,read_only = True, view_name = 'Article-Detail')
    articles = SerializerArticle(read_only=True, many=True)

    class Meta:
        model = Journalist
        fields = '__all__'

    # class SerializerArticle(serializers.Serializer):
    #     id = serializers.IntegerField(read_only=True)
    #     author = serializers.CharField()
    #     title = serializers.CharField()
    #     heading = serializers.CharField()
    #     body = serializers.CharField()
    #     published = serializers.DateField()
    #     created = serializers.DateTimeField(read_only=True)
    #     updated = serializers.DateTimeField(read_only=True)
    #     active = serializers.BooleanField()
    #     def create(self, validated_data):
    #         print(self.validated_data)
    #         return Article.objects.create(**validated_data)
    #     def update(self, instance, validated_data):
    #         instance.author = validated_data.get('author', instance.author)
    #         instance.title = validated_data.get('title', instance.title)
    #         instance.heading = validated_data.get('heading', instance.heading)
    #         instance.body = validated_data.get('body', instance.body)
    #         instance.published = validated_data.get(
    #             'publisged', instance.published)
    #         instance.active = validated_data.get('active', instance.active)
    #         instance.save()
    #         return instance
    #     # Object level validation, validation with more than one field
    #     def validate(self, data):
    #         if data['title'] == data['heading']:
    #             raise serializers.ValidationError(
    #                 'title and heading should be differrent')
    #         return data
    #     # field level validation, validation with in a single field
    #     def validate_title(self, value):
    #         if len(value) < 20:
    #             raise serializers.ValidationError(
    #                 'title is too short')
    #         return value
    
    
    
"""     
A `ModelSerializer` is just a regular `Serializer`, except that:
* A set of default fields are automatically populated.
* A set of default validators are automatically populated.(we have to add if we want any perticular validations)
* Default `.create()` and `.update()` implementations are provided.

Notes
FYI:
>>> Article.objects.all()
# we have two articles
<QuerySet [<Article: Sai django>, <Article: Suresh Python>]>


"" serialization ""

python manage.py shell
>>> from news_app.models import Article
>>> from news_app.api.serializers import SerializerArticle

>>> article_instance = Article.objects.first() # to take first artile
>>> article_instance
# to convert data into SerializerArticle
>>> serialzer = SerializerArticle(article_instance)
>>> serializer.data
{'id': 1, 'author': 'Sai', 'title': 'django', 'heading': 'django_REST_framework', 'body': 'this chapter will give you full details on django REST Framework',
    'published': '2022-07-09', 'created': '2022-07-09T15:07:13.629769Z', 'updated': '2022-07-09T15:07:13.629769Z', 'active': True}

now we have created a serializer (having serialized data)
to finalize the serialization we render data to json

>>> from rest_framework.renderers import JSONRenderer
>>> json = JSONRenderer().render(serializer.data)
>>> json
b'{"id":1,"author":"Sai","title":"django","heading":"django_REST_framework","body":"this chapter will
give you full details on django REST Framework","published":"2022-07-09","created":"2022-07-09T15:07:13.629769Z","updated":"2022-07-09T15:07:13.629769Z","active":true}'

now the serialization process is completed.

"To Deserialize"

>>> import io
>>> from rest_framework.parsers import JSONParser
>>> bytes_stream = io.BytesIO(json)
>>> converted_data = JSONParser().parse(bytes_stream)
>>> converted_data
{'id': 1, 'author': 'Sai', 'title': 'django', 'heading': 'django_REST_framework', 'body': 'this chapter will give you full details on django REST Framework',
    'published': '2022-07-09', 'created': '2022-07-09T15:07:13.629769Z', 'updated': '2022-07-09T15:07:13.629769Z', 'active': True}
>>>

Creating new Article ::

# instead of new data considered old article
>>> serializer = SerializerArticle(data = converted_data)
>>> serializer
SerializerArticle({'id': 1, 'author': 'Sai', 'title': 'django', 'heading': 'django_REST_framework', 'body': 'this chapter will give you full details on django REST Framework', 'published': '2022-07-09', 'created': '2022-07-09T15:07:13.629769Z', 'updated': '2022-07-09T15:07:13.629769Z', 'active': True}):
    id = IntegerField(read_only=True)
    author = CharField()
    title = CharField()
    heading = CharField()
    body = CharField()
    published = DateField()
    created = DateTimeField(read_only=True)
    updated = DateTimeField(read_only=True)
    active = BooleanField()

>>> serializer.is_valid()   # to check the given new data is valid or not
True
>>> serializer.validated_data
OrderedDict([('author', 'Sai'), ('title', 'django'), ('heading', 'django_REST_framework'), ('body',
            'this chapter will give you full details on django REST Framework'), ('published', datetime.date(2022, 7, 9)), ('active', True)])
>>> serializer.save()      # save
OrderedDict([('author', 'Sai'), ('title', 'django'), ('heading', 'django_REST_framework'), ('body',
            'this chapter will give you full details on django REST Framework'), ('published', datetime.date(2022, 7, 9)), ('active', True)])
<Article: Sai django>   # article is saved.

>>> Article.objects.all()
<QuerySet [<Article: Sai django>, <Article: Suresh Python>, <Article: Sai django>]>
# Article added.
"""
