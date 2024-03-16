from django.core.validators import FileExtensionValidator


image_extension     = FileExtensionValidator(['jpeg', 'jpg', 'png'])
doc_extension       = FileExtensionValidator(['doc', 'docx', 'pdf'])

    