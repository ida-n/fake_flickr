from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

class Image(models.Model):
	description = models.CharField(max_length=250)
	imgfile = models.ImageField(upload_to='images/%Y/%m/%d')
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
	)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
	comment_text = models.CharField(max_length=250)
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
	)
	image = models.ForeignKey(
		'Image',
		on_delete=models.CASCADE,
	)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class Vote(models.Model):
	rate = models.PositiveSmallIntegerField(
		validators=[
			MaxValueValidator(5),
			MinValueValidator(1)
        ]
    )
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
	)
	image = models.ForeignKey(
		'Image',
		on_delete=models.CASCADE,
	)

	class Meta:
		unique_together = ('user', 'image')

