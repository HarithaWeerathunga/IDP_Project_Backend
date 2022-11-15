from django.db import models

# Create your models here.
# class Drink(models.Model):
#     name = models.CharField(max_length=200)
#     description = models.CharField(max_length=500)
#     image = models.ImageField(null=True, blank=True, upload_to="image/")
#     url = models.URLField(blank=True)
#     def __str__(self):
#         return self.name + ' ' + self.description


class MultimodalData(models.Model):
    preop_mri = models.CharField(max_length=200)
    postop_mri = models.CharField(max_length=200)
    biopsy = models.CharField(max_length=200)

class RgbImage(models.Model):
    anatomical_annot = models.CharField(max_length=200)

class HyperSpectralImage(models.Model):
    hyperspec_image = models.CharField(max_length=200)
    imaging_data = models.CharField(max_length=200)
    resolution = models.CharField(max_length=200)
    bands = models.CharField(max_length=200)
    frames = models.CharField(max_length=200)
    rgb_image = models.OneToOneField(RgbImage, on_delete = models.CASCADE)
    
class Patient(models.Model):
    age = models.IntegerField()
    gender = models.CharField(max_length=1)
    hyper_spectral_image = models.ForeignKey(HyperSpectralImage, on_delete = models.CASCADE)
    multi_modal_data = models.ForeignKey(MultimodalData, on_delete = models.CASCADE)

class Imaging(models.Model):
    acquisition_type = models.CharField(max_length=200)
    light_intensity = models.CharField(max_length=200)
    light_source = models.CharField(max_length=200)
    device_name = models.CharField(max_length=200)
    hyper_spectral_image = models.ForeignKey(HyperSpectralImage, null = True, on_delete = models.CASCADE)

class HsiSoftware(models.Model):
    analysis_method = models.CharField(max_length=200)
    analysis_duration = models.CharField(max_length=200)
    imaging = models.ForeignKey(Imaging, null = True, on_delete = models.CASCADE)

class ClassFeature(models.Model):
    class_feature = models.CharField(max_length=200)

class TissueClass(models.Model):
    tissue_type = models.CharField(max_length=200)
    class_feature = models.ForeignKey(ClassFeature, on_delete = models.CASCADE)

class Diagnosis(models.Model):
    type = models.CharField(max_length=200)
    level = models.CharField(max_length=200)
    description = models.CharField(max_length=200)

class Mask(models.Model):
    mask_image = models.CharField(max_length=200)
    diagnosis = models.ManyToManyField(Diagnosis)
    tissue_class = models.ManyToManyField(TissueClass)

class Annotation(models.Model):
    annot_image = models.CharField(max_length=200)
    mask = models.ForeignKey(Mask, on_delete = models.CASCADE)
    hyper_spectral_image = models.OneToOneField(HyperSpectralImage, on_delete = models.CASCADE)


