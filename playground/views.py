import os
from django.shortcuts import render, HttpResponse
from django.http import HttpResponse, JsonResponse
# from .models import Drink
# from .serializers import DrinkSerializer
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import base64
from django.views.decorators.csrf import csrf_exempt
from tifffile import TiffFile, TiffWriter
from werkzeug.utils import secure_filename
from pathlib import Path
import PIL.Image
import numpy as np

from playground.models import HyperSpectralImage
from playground.config import Config

# Create your views here.
@csrf_exempt
def image_endpoint(request, name):
    if request.method == 'GET':
        file_name = name
        destination = 'binary-masks/'
        image_path = f'{destination}{file_name}'
        with open(image_path, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
        return JsonResponse({'state': True, 'message':'success', 'data': 'data:image/tiff;base64,' + image_data}, safe=False)
    elif request.method == 'DELETE':
        result = image_delete_endpoint(request, name)
        return JsonResponse({'state': True, 'message':'success', 'data': result}, safe=False)

def image_delete_endpoint(request, name):
    destination = 'binary-masks/' + name
    result = False
    # check if file exists or not
    if os.path.exists(destination ):
        os.remove(destination)
        result = True
    return result
        
@csrf_exempt
def image_post_endpoint(request):
    if request.method == 'POST':
        file = request.FILES['image']
        file_name = file.name



        destination = 'binary-masks/'
        isExist = os.path.exists(destination)
        if not isExist:
            # Create a new directory because it does not exist
            os.makedirs(destination)

        output = f'{destination}{file_name}'
        print(file_name)
        fn = open(output, 'wb+')
        for chunk in file.chunks():
            fn.write(chunk)
        fn.close
        return JsonResponse({'state': True, 'message':'success', 'data': file_name + ' is upload to the server successfully'}, safe=False)

def mtiff_get_endpoint(request, name):
    if request.method == 'GET':
        file_name = name
        destination = '\\binary-masks\\'
        image_path = f'{destination}{file_name}'
        absPath = os.path.abspath(os.getcwd()) + image_path
        mask, label = read_mtiff(absPath)
        return JsonResponse({'state': True, 'message':'success', 'data': {'label': label, 'mask': str(mask)}}, safe=False)

def mtiff_get_all_endpoint(request):
    if request.method == 'GET':
        destination = '\\binary-masks\\'
        folder = os.path.abspath(os.getcwd()) + destination
        result = load_images_from_folder(folder)
        return JsonResponse({'state': True, 'message':'success', 'data': str(result)}, safe=False)

#get spectral image, label return binary mask

def read_mtiff(filename):
    """
    Read a mask bitmap tiff.

    Mask bitmap tiff contains multiple pages of bitmap masks. The mask label
    is stored in tag 65001 in each page. The mask label is stored as an ASCII
    string that may contain unicode codepoints encoded as ASCII character
    sequences (see unicode-escape encoding in Python docs).

    :param filename:    filename of the mask tiff to read.
    :return:            Dict[label: str, mask: ndarray], where
                        label: the mask label
                        mask: the boolean bitmap associated with the label.


    10 different classes not all are used in every image
    """
    TIFFTAG_MASK_LABEL = 65001
    masks = dict()
    with TiffFile(filename) as tiff:
        print(tiff)
        for p in range(0, len(tiff.pages)):
            label_tag = tiff.pages[p].tags.get(TIFFTAG_MASK_LABEL)
            if label_tag is None:
                if p > 0:
                    print(f'** page {p}: no TIFF_MASK_LABEL tag. Ignored.')
                continue
            print("---------")
            label = label_tag.value.encode('ascii').decode('unicode-escape')
            print("Label")
            print(label)
            mask = tiff.asarray(key=p)
            masks[label] = mask > 0
            # print(masks[label])
            # return masks and the label


    return masks,label

def load_images_from_folder(folder):
    import random as r
    num = r.randint(0,9999)
    images = []
    reading_of_mtiffs = []
    for filename in os.listdir(folder):
        full_path = folder + filename
        print(type(full_path))
        mask, label = read_mtiff(full_path)
        reading_of_mtiffs.append({'mask': mask, 'label': label})
        
        print(filename)
        print("masks and labels")
        print(mask[label])
        print("-------String of masks----------")
        num = num + 1
        # insert_varibles_into_table(num, str(filename), labels, str(masks[labels]) )
        
    return reading_of_mtiffs





@csrf_exempt
def upload_spectral_image(request):
    if request.method == 'POST' or request.method == 'GET':
        file = request.FILES['image']

        destination = Config.SPECTRAL_IMAGE_DIR
        isExist = os.path.exists(destination)
        if not isExist: os.makedirs(destination)
        
        file_name = secure_filename(file.name)
        file_path = Path(f'{destination}\\{file_name}')
        fn = open(file_path, 'wb+')
        for chunk in file.chunks(): fn.write(chunk)
        fn.close

        with TiffFile(file_path) as tiff:
            # Page 0 may be an RGB color image or a grayscale image - so the shape may be (height, width, color bands)
            # or (height, width)... Tuple unpacking does not with this.
            # Page 1 should be always a grayscale image with shape (height, width).
            width, height = tiff.pages[1].shape
            bands = len(tiff.pages) - 1

            spectralImage = HyperSpectralImage()
            spectralImage.image_filename = str(file_path.relative_to(destination))
            spectralImage.resolution_height=height
            spectralImage.resolution_width=width
            spectralImage.resolution_depth=bands
            spectralImage.save()

        return JsonResponse({'state': True, 'message':'success', 'data': file_name + ' is upload to the server successfully'}, safe=False)

def _generate_png_image(image_array: np.ndarray, file_name):
    image = PIL.Image.fromarray(image_array)
    dummy = 'generate\\{file_name}'
    destination = Config.SPECTRAL_IMAGE_DIR
    file_path = Path(f'{destination}\\{dummy}')
    image.save(file_path, format='png')
    return _png_to_base_64(dummy)

def _generate_dummy_png_image(width: int, height: int):
    image = PIL.Image.new('RGB', (width, height), (128, 128, 128))
    dummy = 'generate\\dummy.png'
    destination = Config.SPECTRAL_IMAGE_DIR
    file_path = Path(f'{destination}\\{dummy}')
    image.save(file_path, format='png')
    return _png_to_base_64(dummy)

def _png_to_base_64(file_name):
    destination = Config.SPECTRAL_IMAGE_DIR
    file_path = Path(f'{destination}\\{file_name}')
    with open(file_path, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode('utf-8')
        return image_data

def show_spectral_image_preview_image(request, pk: int):
    # spectral_image = HyperSpectralImage.objects.get(pk)
    # image_data = spectral_image.get_preview_image()

    image_data = None
    if image_data is None: image_data = _generate_dummy_png_image(1024, 1024)

    return JsonResponse({'state': True, 'message':'success', 'data': 'data:image/png;base64,' + image_data}, safe=False)


def show_spectral_image_band_image(request, pk: int, band: int):
    # spectral_image = HyperSpectralImage.objects.get(pk)
    # png_data = spectral_image.get_band_image(band)

    image_data = None
    if image_data is None: image_data = _generate_dummy_png_image(1024, 1024)

    return JsonResponse({'state': True, 'message':'success', 'data': 'data:image/png;base64,' + image_data}, safe=False)



# def _generate_a_dummy_image(width: int, height: int) -> io.BytesIO:
#     image = PIL.Image.new('RGB', (width, height), (128, 128, 128))
#     png_data = io.BytesIO()
#     image.save(png_data, format='png')
#     png_data.seek(0)

#     return png_data
    
# def show_spectral_image_band_image(pk: int, band: int):
#     spectral_image = HyperSpectralImage.objects.get(pk)
#     png_data = spectral_image.get_band_image(band)

#     if png_data is None: png_data = _generate_a_dummy_image(spectral_image.width, spectral_image.height)

#     return send_file(png_data, 'image/png')

# def show_spectral_image_preview_image(request, pk):
    # spectral_image = HyperSpectralImage.objects.get(pk)
    # png_data = spectral_image.get_preview_image()

    # if png_data is None: png_data = _generate_a_dummy_image(spectral_image.width, spectral_image.height)

    # return send_file(png_data, 'image/png')

# class uploadPhoto(APIView):
#     def get(self, request):
#         file_name = "VisualizationAssignment4.PNG"
#         destination = 'media/'
#         image_path = f'{destination}{file_name}'
#         with open(image_path, "rb") as image_file:
#             image_data = base64.b64encode(image_file.read()).decode('utf-8')
#         return HttpResponse(image_data)
#         #<img src="data:image/png;base64,{{ image }}">

#     def post(self, request):
#         file = request.FILES['image']
#         file_name = file.name
#         destination = 'media/'
#         output = f'{destination}{file_name}'
#         print(file_name)
#         fn = open(output, 'wb+')
#         for chunk in file.chunks():
#             fn.write(chunk)
#         fn.close
#         return HttpResponse("%s is upload to the server successfully" % file_name)

# def say_hello(request):
#     #return HttpResponse('Hello World')
#     return render(request, 'hello.html', {'name': 'moo'})

# @api_view(['GET', 'POST'])
# def drink_list(request):

#     if request.method == 'GET':
#         drinks = Drink.objects.all()
#         serializer = DrinkSerializer(drinks, many=True)
#         return JsonResponse({"drinks": serializer.data}, safe=False)

#     if request.method == 'POST':
#         serializer = DrinkSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

# @api_view(['GET', 'PUT', 'DELETE'])
# def drink_detail(request, id):
#     try:
#         drink = Drink.objects.get(pk=id)
#     except Drink.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'GET':
#         serializer = DrinkSerializer(drink)
#         return Response(serializer.data)
    
#     elif request.method == 'PUT':
#         serializer = DrinkSerializer(drink, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#     elif request.method == 'DELETE':
#         drink.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
