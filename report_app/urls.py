from django.urls import path
from .import views



urlpatterns = [
    path('report-pdf-order/', views.report_pdf_order, name='report_pdf_order'),
]