from django.db import models

class Tag(models.Model):
    """Tag model
    fields:
        label (CharField): name of the tag
    """
    label = models.CharField(max_length=50)

    def __str__(self):
        return self.label