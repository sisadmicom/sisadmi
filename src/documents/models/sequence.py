from django.db import models


class DocumentSequence(models.Model):

    code = models.CharField(
        max_length=50,
        unique=True
    )

    name = models.CharField(
        max_length=100
    )

    prefix = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )

    last_number = models.IntegerField(
        default=0
    )

    padding = models.IntegerField(
        default=9
    )

    establishment = models.CharField(max_length=3)
    
    emission_point = models.CharField(max_length=3)

    def next_number(self):

        self.last_number += 1
        self.save()

        number = str(self.last_number).zfill(self.padding)

        if self.prefix:
            return f"{self.prefix}{number}"  
            #if self.name else self.name

        return number