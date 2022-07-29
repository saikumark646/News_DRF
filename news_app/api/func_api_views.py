from django.shortcuts import get_object_or_404
from news_app.api.serializers import SerializerArticle
from news_app.models import Article

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET', 'POST'])
def article_list_create_api_view(request):
    if request.method == 'GET':
        qs = Article.objects.filter(active=True)
        serializer = SerializerArticle(qs, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = SerializerArticle(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def article_detail_api_view(request, pk):
    # try:
    #     article = Article.objects.get(pk=pk)
    # except Article.DoesNotExist:
    #     return Response(
    #         {'error':
    #             {'code': 404,
    #              'message': 'product not found'}}
    #     )
    article = get_object_or_404(Article, pk=pk)
    # instead of above try and except block we can use this single line

    if request.method == 'GET':
        serializer = SerializerArticle(article)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = SerializerArticle(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


""" 
Response::
The Response class in REST framework is similar to HTTPResponse, except that
it is initialized with unrendered data, instead of a pre-rendered string.

The appropriate renderer is called during Django's template response rendering.
"""
