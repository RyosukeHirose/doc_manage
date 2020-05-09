# from django.db import models
# from django.core.validators import FileExtensionValidator

# class Files(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4 editable=False)
#     attach=models.FileFeild(
#         upload_to='uploads/%Y%/%m/%d',
#         verbose_name='添付ファイル',
#         validators=[FileExtensionValidator(['pdf', 'docx', 'ppt',])],
#     )