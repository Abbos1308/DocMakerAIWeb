from django.db import models
from docmakerai.regex import parse_github_repo
# Create your models here.

class Repo(models.Model):
    url = models.URLField()
    doc = models.TextField(blank=True)
    shortcut = models.TextField()
    def __str__(self):
        return self.shortcut
    
    def save(self, *args, **kwargs):
        self.shortcut = "_".join(parse_github_repo(self.url))
        super().save(*args, **kwargs)
        