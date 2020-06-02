from django.db import models
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator

class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file_name = models.CharField(max_length=128)

    def __str__(self):
        return self.file_name

class Word(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    word_name = models.CharField(max_length=128)
    files = models.ManyToManyField(File, through='Tdidf')

    def __str__(self):
        return self.word_name

class Tdidf(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    tdidf = models.FloatField(validators=[MinValueValidator(0.00), MaxValueValidator(1.00)])