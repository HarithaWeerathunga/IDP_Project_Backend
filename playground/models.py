from django.db import models


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

    hyperspec_image = models.CharField(max_length=200)
    imaging_data = models.TextField(max_length=200)
    resolutionHeight = models.IntegerField(null=True)
    resolutionWidth = models.IntegerField(null=True)
    bands = models.PositiveIntegerField(null=True)
    frames = models.PositiveIntegerField(null=True)
    rgb_image = models.OneToOneField(RgbImage, null=True, on_delete = models.SET_NULL)
    patient = models.OneToOneField(Patient, null=True, on_delete = models.SET_NULL)
    multi_modal_Data = models.OneToOneField(MultimodalData, null=True, on_delete = models.SET_NULL)
    actual_image = models.ImageField(blank=True, null=True, upload_to='media')

    def __str__(self):
        return self.hyperspec_image
    
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




