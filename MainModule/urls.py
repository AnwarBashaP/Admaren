from django.urls import path
from . import  views

urlpatterns = [
        path('', views.BlogView.as_view(), name='Blog Api view'), #Blog model
        path('blog', views.BlogList, name='Blog get Api view'), #Blog Details model
        path('taglist/',views.TagView.as_view(), name= 'Tag List view'), #Tag list view
        path('tagdetail/',views.TagDetailView.as_view(), name= 'Tag List view') #Tag details view
    ]