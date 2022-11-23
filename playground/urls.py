from django.urls import path
from . import views
#from django.conf import settings
#from django.conf.urls.static import static

#URLConf
urlpatterns = [
    #path('hello/', views.say_hello),
    #path('drinks/', views.drink_list),
    #path('drinks/<int:id>', views.drink_detail),
    #path('upload', views.uploadPhoto.as_view(), name="upload"),

    # path('image/<str:name>', views.image_endpoint),
    # path('image', views.image_post_endpoint),
    # path('tiff/mask/<str:name>', views.mtiff_get_endpoint),
    # path('tiff/mask', views.mtiff_get_all_endpoint),
    


    path('upload/spectral_image', views.upload_spectral_image),
    path('spectral_image/preview/<int:pk>', views.show_spectral_image_preview_image),
    path('spectral_image/band/<int:pk>/<int:band>', views.show_spectral_image_band_image),
]
#+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)