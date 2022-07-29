from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from news_app.api.serializers import SerializerArticle, JournalistSerializer
from news_app.models import Article, Journalist


class ArticleListCreateView(APIView):
    def get(self, request):
        article = Article.objects.filter(active=True)
        serializer = SerializerArticle(article, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SerializerArticle(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDetailView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Article, pk=pk)

    def get(self, request, pk):
        article = self.get_object(pk)
        serializer = SerializerArticle(article)
        return Response(serializer.data)

    def put(self, request, pk):
        article = self.get_object(pk)
        serializer = SerializerArticle(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        article = self.get_object(pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class JournalistcreateListView(APIView):
    def get(self, request):
        journalist = Journalist.objects.all()
        serializer = JournalistSerializer(journalist,
                                          many=True,
                                          context={'request': request})  # context must be specified to execute a hyperlink for journals.
        return Response(serializer.data)

    def post(self, request):
        serializer = JournalistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JournalistDetailView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Journalist, pk=pk)

    def get(self, request, pk):
        journalist = self.get_object(pk)
        serializer = JournalistSerializer(journalist)
        return Response(serializer.data)

    def put(self, request, pk):
        journalist = self.get_object(pk)
        serializer = JournalistSerializer(journalist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        journalist = self.get_object(pk)
        journalist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
