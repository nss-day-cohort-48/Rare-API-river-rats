from django.db import models


class Post(models.Model):
    rare_user = models.ForeignKey("RareUser", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    title = models.CharField(max_length=25)
    publication_date = models.DateField()
    image_url = models.ImageField()
    content = models.CharField(max_length=250)
    approved = models.BooleanField()
