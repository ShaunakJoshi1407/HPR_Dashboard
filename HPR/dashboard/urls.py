from django.urls import path # type: ignore
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('run_script/', views.run_script, name='run_script'),
    path('plot_display/', views.plot_display, name='plot_display'),
    path('run_apple_analysis/', views.run_apple_analysis, name='run_apple_analysis'),
    path('plot_display_apple/', views.plot_display_apple, name='plot_display_apple'),
    path('run_tesla_analysis/', views.run_tesla_analysis, name='run_tesla_analysis'),  
    path('plot_display_tesla/', views.plot_display_tesla, name='plot_display_tesla'),
    path('run_spy_analysis/', views.run_spy_analysis, name='run_spy_analysis'),  
    path('plot_display_spy/', views.plot_display_spy, name='plot_display_spy'),
]
