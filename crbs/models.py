from django.db import models


# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)
    capacity = models.IntegerField()
    projector = models.BooleanField(default=False)


class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date = models.DateField()
    comment = models.TextField()

    class Meta:
        unique_together = ("room", "date")
