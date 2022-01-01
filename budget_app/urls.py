from django.contrib import admin
from django.urls import path,include, register_converter
from budget_app import views
from datetime import datetime

class DateConverter:
      regex = r'\d{4}-\d{2}-\d{2}'

      def to_python(self, value):
            return datetime.strptime(value, '%Y-%m-%d')
      
      def to_url(self, value):
            return value

register_converter(DateConverter, 'yyyy')


urlpatterns = [
      path('',views.index),
      path('login/',views.login),
      path('register/',views.register),
      path('budget/<int:pk>/overview/',views.overview_page),
      path('budget/<int:pk>/home/', views.home_page),
      path('budget/<int:pk>/profile/', views.profile_page),
      # path('home/<int:pk>/add_expense', views.add_expense),
      # path('home/<int:pk>/change_budget/', views.change_budget),
      # path('home/<int:pk>/delete/<int:pk1>', views.delete_expense),
      #path('home/date/<yyyy:date>/', views.show_dates),
      ]