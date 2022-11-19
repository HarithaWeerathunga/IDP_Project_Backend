from django.db import models


class MultimodalData(models.Model):
    #image files for both
    preop_mri = models.CharField(max_length=200)
    postop_mri = models.CharField(max_length=200)

    #text field
    biopsy = models.CharField(max_length=200)

    def __str__(self):
        return self.biopsy

class RgbImage(models.Model):
    #todo add image field

    #as a mask image field
    anatomical_annot = models.CharField(max_length=200)

    def __str__(self):
        return self.anatomical_annot

class HyperSpectralImage(models.Model):
    #todo how to get the individual band from tiff file

    hyperspec_image = models.CharField(max_length=200)
    #text field
    imaging_data = models.CharField(max_length=200)
    #eg both int
    resolutionHeight = models.CharField(max_length=200)
    resolutionWidth = models.CharField(max_length=200)

    #band and frames + integer
    bands = models.CharField(max_length=200)
    frames = models.CharField(max_length=200)
    rgb_image = models.OneToOneField(RgbImage, on_delete = models.CASCADE)

    actual_image = models.ImageField(blank=True, null=True, upload_to='media')

    def __str__(self):
        return self.hyperspec_image
    
class Patient(models.Model):
    #age = models.IntegerField()
    patientID = models.CharField(max_length=20, default="1")
    #gender = models.CharField(max_length=1)

    #works backs to the patient same as the multimodal data
    hyper_spectral_image = models.ForeignKey(HyperSpectralImage, on_delete = models.CASCADE)
    multi_modal_data = models.ForeignKey(MultimodalData, on_delete = models.CASCADE)

    def __str__(self):
        return self.patientID

class Imaging(models.Model):
    acquisition_type = models.CharField(max_length=200)
    light_intensity = models.CharField(max_length=200)
    light_source = models.CharField(max_length=200)
    device_name = models.CharField(max_length=200)

    analysis_method = models.CharField(max_length=200)
    analysis_duration = models.CharField(max_length=200)

    hyper_spectral_image = models.ForeignKey(HyperSpectralImage, null = True, on_delete = models.CASCADE)

    def __str__(self):
        return  self.device_name

class HsiSoftware(models.Model):
    # analysis_method = models.CharField(max_length=200)
    # analysis_duration = models.CharField(max_length=200)

    #works backwards to the image table
    imaging = models.ForeignKey(Imaging, null = True, on_delete = models.CASCADE)

    def __str__(self):
        return self.analysis_method

class ClassFeature(models.Model):
    # for more delibration on how to use this model with the team based on saving
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
    hyper_spectral_image = models.OneToOneField(HyperSpectralImage, on_delete = models.CASCADE)




