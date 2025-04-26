# Define the models for Recipe and Comment

# myapp/models.py
from django.db import models
from django.core.exceptions import ValidationError


def validate_file_type(value):
    allowed_extensions = ['jpeg', 'jpg', 'png']
    file_extension = value.name.split('.')[-1].lower()  # Extract the file extension
    if file_extension not in allowed_extensions:
        raise ValidationError(f"Unsupported file extension. Allowed types are: {', '.join(allowed_extensions)}.")

class Recipe(models.Model):
    id_recipe = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='media/',validators=[validate_file_type])
    user = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Comment(models.Model):
    user = models.CharField(max_length=255)
    id_recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments')
    message = models.TextField()

    def __str__(self):
        return f"Comment by {self.user} on {self.id_recipe.name}"

class Favori(models.Model):
    user = models.CharField(max_length=255)
    id_recipe = models.ForeignKey(Recipe, on_delete=models.DO_NOTHING, related_name='favoris')
    

    def __str__(self):
        return f"{self.user} favori is {self.id_recipe.name}"