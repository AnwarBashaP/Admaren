import datetime

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import PostModel, TagsModel


class BlogView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        request.POST._mutable = True
        try:
            validate_data = PostModel.objects.create(snippets=request.data['snippets'], title=request.data['title'],
                                                     content=request.data['content'], created_by=request.user)
            TagsModel.objects.create(Post=validate_data, Tag=f'{request.data["title"]} - {request.data["title"]}')

            return Response({"message", "successfully saved"}, status=status.HTTP_200_OK)
        except KeyError as e:
            return Response({"message": f'{e} data is missing. please provide all valid data'},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        except Exception as e:
            return Response({"message": f'{e}'}, status=status.HTTP_406_NOT_ACCEPTABLE)

    def get(self, request):
        try:
            serializedData = PostModel.objects.filter(status= True).values()
            return Response(serializedData, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": f'{e}'}, status=status.HTTP_204_NO_CONTENT)

    def put(self, request, title):
        request_data = request.data
        try:
            obj = PostModel.objects.get(title=title)
            for key, value in request_data.items():
                setattr(obj, key, value)
            obj.published_at = datetime.datetime.now()
            obj.status = True
            obj.save()
            return Response({"message": "successfully updated"}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "something went wrong try again!"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, title):
        try:
            obj = PostModel.objects.filter(title=title)
            obj.status = False
            obj.save()
            return Response({"message": "successfully updated"}, status=status.HTTP_200_OK)
        except:
            return Response({"message": "something went wrong try again!"}, status=status.HTTP_400_BAD_REQUEST)


class TagView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        output = TagsModel.objects.filter(status = True).values('Tag')
        return Response({output}, status=status.HTTP_200_OK)

class TagDetailView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        output = TagsModel.objects.filter(status=True).values('Tag','Post__title','Post__snippets','Post__content','Post__published_at')
        return Response({output}, status=status.HTTP_200_OK)

def BlogList(self, request):
    queryset_data = PostModel.objects.values()
    count_querset = PostModel.objects.all().count()
    return Response({"message": queryset_data, "Count": count_querset}, status=status.HTTP_200_OK)