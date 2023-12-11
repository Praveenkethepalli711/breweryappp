from django.db import models
import uuid
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.
class Brewery(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    brewery_type = models.CharField(max_length=50)
    address_1 = models.CharField(max_length=255)
    phone = models.CharField( max_length=10)

    def __str__(self):
        return self.name
    
class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_instance(self):
        return self
    def __str__(self):
        return self.user.first_name

class Rating(models.Model):
    stars = models.PositiveBigIntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    brewery_name = models.CharField(max_length=255)  # Add this line to store the brewery name
    
    @classmethod
    def create_rating(cls, brewery, stars, comment):
        # Set the brewery_name field when creating the Rating object
        brewery_name = brewery.name
        return cls.objects.create(brewery_name=brewery_name, stars=stars, comment=comment)
    @classmethod
    def delete_rating(cls, rating_id):
        # Delete a rating by its ID
        cls.objects.filter(id=rating_id).delete()

    @classmethod
    def get_ratings_for_brewery(cls, brewery):
        # Get all ratings for a specific brewery
        return cls.objects.filter(brewery_name=brewery.name)

    @classmethod
    def get_average_rating_for_brewery(cls, brewery):
        # Get the average rating for a specific brewery
        ratings = cls.objects.filter(brewery_name=brewery.name)
        if ratings.exists():
            return ratings.aggregate(models.Avg('stars'))['stars__avg']
        return None

    def __str__(self):
        return f"{self.brewery_name} - {self.stars} stars"