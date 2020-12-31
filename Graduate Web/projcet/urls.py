"""projcet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.conf import settings
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # 첫페이지 url 설정
    path('', views.r_index),

    # 뒤에 붙일 url주소는 page2, view에서 불러오는 함수는 i_to_p2,
    # 해당 패턴의 이름은 i_to_p2로 설정
    # 페이지 이동 url 패턴
    path('dbcheck/', views.r_dbcheck),
    path('upload/', views.r_upload),
    path('compare/', views.r_compare),

    # 다른 함수사용 url 패턴
    path('f_upload/', views.f_upload),
    path('f_test/', views.f_test),
]

# 미디어 루트 설정
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)
