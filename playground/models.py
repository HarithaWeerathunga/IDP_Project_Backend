from django.db import models
import PIL.Image
import io
import numpy as np
from playground.config import Config
from tifffile import TiffFile


class MultimodalData(models.Model):
    preop_mri = models.ImageField(blank=True, null=True, upload_to='media')
    postop_mri = models.ImageField(blank=True, null=True, upload_to='media')
    biopsy = models.TextField(max_length=200)

    def __str__(self):
        return self.biopsy

class RgbImage(models.Model):
    #todo add image field
    #as a mask image field
    anatomical_annot = models.ImageField(blank=True, null=True, upload_to='media')

    def __str__(self):
        return self.anatomical_annot

class Patient(models.Model):
    patientID = models.CharField(max_length=20, default="1")

    #Has being worked on
    #works backs to the patient same as the multimodal data
    #hyper_spectral_image = models.ForeignKey(HyperSpectralImage, on_delete = models.CASCADE)
    #multi_modal_data = models.ForeignKey(MultimodalData, on_delete = models.CASCADE)

    def __str__(self):
        return self.patientID

class HyperSpectralImage(models.Model):
    #todo how to get the individual band from tiff file
    # id = models.IntegerField(primary_key=True)
    image_filename = models.CharField(max_length=200, null=True)
    imaging_data = models.TextField(max_length=200)
    resolution_height = models.IntegerField(null=True)
    resolution_width = models.IntegerField(null=True)
    resolution_depth = models.IntegerField(null=True)

    hyperspec_image = models.CharField(max_length=200)
    bands = models.PositiveIntegerField(null=True)
    frames = models.PositiveIntegerField(null=True)
    rgb_image = models.OneToOneField(RgbImage, null=True, on_delete = models.SET_NULL)
    patient = models.OneToOneField(Patient, null=True, on_delete = models.SET_NULL)
    multi_modal_Data = models.OneToOneField(MultimodalData, null=True, on_delete = models.SET_NULL)
    actual_image = models.ImageField(blank=True, null=True, upload_to='media')
    
    @staticmethod
    def _array_to_png(image_array: np.ndarray) -> io.BytesIO:
        png_buffer = io.BytesIO()
        image = PIL.Image.fromarray(image_array)
        image.save(png_buffer, format='png')
        png_buffer.seek(0)
        return png_buffer

    def get_preview_image(self) -> io.BytesIO | None:
        actual_image_filename = Config.SPECTRAL_IMAGE_DIR / self.image_filename

        match actual_image_filename.suffix.lower():
            case '.tif':
                with TiffFile(actual_image_filename) as tiff:
                    if (page_0 := tiff.pages[0]).ndim == 3:
                        return self._array_to_png(page_0.asarray())
        return None

    def get_band_image(self, n: int) -> io.BytesIO | None:
        if n < 0 or n > self.depth:
            print(f'{n}, {type(n)}')
            # The requested band does not exist.
            return None

        actual_image_filename = Config.SPECTRAL_IMAGE_DIR / self.image_filename

        match actual_image_filename.suffix.lower():
            case '.tif':
                with TiffFile(actual_image_filename) as tiff:
                    return self._array_to_png(tiff.pages[1 + n].asarray())
        return None

    def __str__(self):
        return self.image_filename
    
class HsiSoftware(models.Model):
    name = models.CharField(max_length=200, null=True)
    #Has being worked on
    #analysis_method = models.CharField(max_length=200)
    #analysis_duration = models.CharField(max_length=200)
    #works backwards to the image table
    #imaging = models.ForeignKey(Imaging, null = True, on_delete = models.CASCADE)
    def __str__(self):
         return self.name

class Imaging(models.Model):
    acquisition_type = models.CharField(max_length=200)
    light_intensity = models.CharField(max_length=200)
    light_source = models.CharField(max_length=200)
    device_name = models.CharField(max_length=200)
    analysis_method = models.CharField(max_length=200, null=True)
    analysis_duration = models.CharField(max_length=200, null=True)
    hsi_software = models.OneToOneField(HsiSoftware, null=True, on_delete = models.SET_NULL)
    hyper_spectral_image = models.ForeignKey(HyperSpectralImage, null = True, on_delete = models.CASCADE)

    def __str__(self):
        return  self.device_name

# for more delibration on how to use this model with the team based on saving
class ClassFeature(models.Model):
    class_feature = models.CharField(max_length=200)

    def __str__(self):
        return self.class_feature

# for more delibration on how to use this model with the team based on saving
class TissueClass(models.Model):
    tissue_type = models.CharField(max_length=200)
    class_feature = models.ForeignKey(ClassFeature, on_delete = models.CASCADE)

    def __str__(self):
        return self.tissue_type

class Diagnosis(models.Model):
    type = models.CharField(max_length=200)
    level = models.CharField(max_length=200)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.type

class Mask(models.Model):
    #to figure with haritha
    mask_image = models.CharField(max_length=200)
    diagnosis = models.ManyToManyField(Diagnosis)
    tissue_class = models.ManyToManyField(TissueClass)

    def __str__(self):
        return self.mask_image


class Annotation(models.Model):
    annot_image = models.CharField(max_length=200)
    mask = models.ForeignKey(Mask, on_delete = models.CASCADE)
    hyper_spectral_image = models.OneToOneField(HyperSpectralImage, null=True, on_delete = models.SET_NULL)




