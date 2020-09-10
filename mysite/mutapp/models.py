from django.db import models

class Covid19metadata(models.Model):
    virus_strain_name = models.CharField(max_length=255)
    accession_id = models.CharField(max_length=255, blank=True)
    data_source = models.CharField(max_length=255, blank=True)
    related_id = models.CharField(max_length=255, blank=True)
    nuc_completeness = models.CharField(max_length=255, blank=True)
    sequence_length = models.IntegerField(default=0, blank=True)
    sequence_quality = models.CharField(max_length=255, blank=True)
    quality_assessment = models.TextField(blank=True)
    host = models.CharField(max_length=255, blank=True)
    sample_collection_date = models.DateTimeField(blank=True)
    location = models.TextField(blank=True)
    originating_lab = models.TextField(blank=True)
    submission_date = models.DateTimeField(blank=True)
    submission_lab = models.TextField(blank=True)
    create_time = models.DateTimeField(blank=True)
    last_update_time = models.DateTimeField(blank=True)

    def __str__(self):
        return self.virus_strain_name + ':   ' + self.location

class SampleMutlist(models.Model):
    virus_strain_name = models.CharField(max_length=255)
    mutation = models.TextField(blank=True)
    metadata = models.ForeignKey(Covid19metadata, on_delete=models.CASCADE)

    def __str__(self):
        return self.virus_strain_name

class MutSamplelist(models.Model):
    ti_tv = models.CharField(max_length=255, blank=True)
    start = models.IntegerField(blank=True)
    end = models.IntegerField(blank=True)
    ref_var = models.TextField(blank=True)
    gene = models.CharField(max_length=255, blank=True)
    ns_s = models.CharField(max_length=255, blank=True)
    count = models.IntegerField(blank=True)
    sample = models.TextField(blank=True)

    def __str__(self):
        return self.ref_var + '  at: ' + str(self.start)


