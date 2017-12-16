import uuid

from django.db import models


class DicomFieldMixin(object):
    def __init__(self, *args, group: str, element: str, **kwargs):
        self.group = group
        self.element = element
        super(DicomFieldMixin, self).__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super(DicomFieldMixin, self).deconstruct()

        kwargs['group'] = self.group
        kwargs['element'] = self.element

        return name, path, args, kwargs


class DicomCharField(DicomFieldMixin, models.CharField):
    pass


class DicomDateField(DicomFieldMixin, models.DateField):
    pass


class DicomTimeField(DicomFieldMixin, models.TimeField):
    pass


class UUIDModel(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


class Archive(UUIDModel):
    pass


class Patient(UUIDModel):
    MALE = 'M'
    FEMALE = 'F'
    OTHER = 'O'

    PATIENT_SEX_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
    )

    archive = models.ForeignKey('Archive', on_delete=models.CASCADE)

    # Type 1: manditory

    # Type 2: manditory, can be null
    name = DicomCharField(group='0010', element='0010', max_length=255)
    identifier = DicomCharField(group='0010', element='0020',
                                max_length=255)
    birth_date = DicomDateField(group='0010', element='0030')
    sex = DicomCharField(group='0010', element='0040',
                         max_length=1, choices=PATIENT_SEX_CHOICES)


class Study(UUIDModel):
    # Type 1
    instance_uid = DicomCharField(group='0020', element='000D', max_length=255)

    # Type 2
    date = DicomDateField(group='0008', element='0020')
    time = DicomTimeField(group='0008', element='0030')
    referring_physicians_name = DicomCharField(group='0008', element='0090',
                                               max_length=255)
    identifier = DicomCharField(group='0020', element='0010',
                                verbose_name='Study ID',
                                max_length=255)
    accession_number = DicomCharField(group='0008', element='0050',
                                      max_length=255)


class Series(UUIDModel):
    # Type 1
    instance_uid = DicomCharField(group='0020', element='000E', max_length=255)
    modality = DicomCharField(group='0008', element='0060', max_length=255)

    # Type 2
    number = DicomCharField(group='0020', element='0011', max_length=255)


class Image(UUIDModel):
    # Type 1
    number = DicomCharField(group='0020', element='0013', max_length=255)

    # Type 1, SOP Common
    sop_class_uid = DicomCharField(group='0008', element='0016',
                                   max_length=255)
    sop_instance_uid = DicomCharField(group='0008', element='0018',
                                      max_length=255)


class SecondaryCaptureEquipment(UUIDModel):
    DIGITIZED_VIDEO = 'DV'
    DIGITAL_INTERFACE = 'DI'
    DIGITIZED_FILM = 'DF'
    WORKSTATION = 'WSD'
    SCANNED_DOCUMENT = 'SD'
    SCANNED_IMAGE = 'SI'
    DRAWING = 'DRW'
    SYNTHETIC_IMAGE = 'SYN'

    CONVERSION_TYPE_CHOICES = (
        (DIGITIZED_VIDEO, 'Digitized Video'),
        (DIGITAL_INTERFACE, 'Digital Interface'),
        (DIGITIZED_FILM, 'Digitized Film'),
        (WORKSTATION, 'Workstation'),
        (SCANNED_DOCUMENT, 'Scanned Document'),
        (SCANNED_IMAGE, 'Scanned Image'),
        (DRAWING, 'Drawing'),
        (SYNTHETIC_IMAGE, 'Synthetic Image'),
    )

    # Type 1
    conversion_type = DicomCharField(group='0008', element='0064',
                                     max_length=3,
                                     choices=CONVERSION_TYPE_CHOICES)
