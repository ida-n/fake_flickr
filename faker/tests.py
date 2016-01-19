import datetime
import os
from statistics  import mean

from django.test import TestCase, RequestFactory
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.core.files import File
from django.contrib.auth.models import AnonymousUser, User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings

from .models import Image, Vote
from .views import my_images

def create_image(user, description):
	"""
	Creates an image with the given 'description', 'user'and 
	the test.jpg image file
	"""
	img = SimpleUploadedFile(
		name='test', 
		content=open(os.path.join(settings.BASE_DIR, 'faker', 'test.jpg'), 'rb').read(), 
		content_type='image/jpeg')
	return Image.objects.create(description=description,
							   user=user,
							   imgfile=img)

def create_vote(user, rate, image):
	"""Creates a vote with the given 'description', 'user' and 'image'"""
	return Vote.objects.create(rate=rate,
							   user=user,
							   image=image)

class ImageViewTest(TestCase):
	def setUp(self):
		# For testing with set request properties
		self.factory = RequestFactory()
		# Creating a test user to use in the tests
		self.user = User.objects.create_user(
			username='test', email='test@example.com', password='!password')
		self.img = create_image(self.user, "test image")

	def testAccessIndexAsAnonymousUser(self):
		"""
		All users should be able to view index page 
		and the images in the top daily and weekly list
		"""
		response = self.client.get(reverse('faker:index'))
		self.assertEqual(response.status_code, 200)
		self.assertQuerysetEqual(response.context['last_day_img_list'], ['<Image: test image>'])
		self.assertQuerysetEqual(response.context['last_week_img_list'], ['<Image: test image>'])
	
	def testAccessImagesAsAnonymousUser(self):
		"""
		All users should be able to view images page 
		and the list of all images
		"""
		response = self.client.get(reverse('faker:images'))
		self.assertEqual(response.status_code, 200)
		self.assertQuerysetEqual(response.context['img_list'], ['<Image: test image>'])

	def testAccessMyImagesAsAnonymousUser(self):
		"""
		Anonymous User users should not be able to access my images page
		"""
		request = self.factory.get('faker:my_images')
		request.user = AnonymousUser()
		response = my_images(request)
		self.assertEqual(response.status_code, 302)

	def testAccessMyImagesAsLoggedInUser(self):
		"""
		Loged in User users should be able to access my images page
		"""
		request = self.factory.get('faker:my_images')
		request.user = self.user
		response = my_images(request)
		self.assertEqual(response.status_code, 200)


	def tearDown(self):
		self.user.delete()
		self.img.delete()


class ImageMethodTest(TestCase):
	def setUp(self):
		self.user1 = User.objects.create_user(
			username='test1', email='test1@example.com', password='!password')
		self.user2 = User.objects.create_user(
			username='test2', email='test2@example.com', password='!password')
		self.img1 = create_image(self.user1, "test image1")
		self.img2 = create_image(self.user2, "test image2")

	def testGetSingleTopImageSingleVote(self):
		"""
		The function should return a list of one image with highest rating
		"""
		create_vote(self.user1, 2, self.img1)
		create_vote(self.user1, 4, self.img2)
		last_day = timezone.now() - datetime.timedelta(days=1)
		top_images = Image.get_top_images(last_day, 1)
		self.assertEqual(len(top_images), 1)
		self.assertEqual(top_images[0].id, self.img2.id)

	def testGetSingleTopImageMoreVotes(self):
		"""
		The function should return a list of one image with highest average rating
		"""
		create_vote(self.user1, 2, self.img1)
		create_vote(self.user1, 4, self.img2)
		create_vote(self.user2, 3, self.img1)
		create_vote(self.user2, 4, self.img2)
		last_day = timezone.now() - datetime.timedelta(days=1)
		top_images = Image.get_top_images(last_day, 1)
		self.assertEqual(len(top_images), 1)
		self.assertEqual(top_images[0].id, self.img2.id)

	def testGetTopImagesSingleVote(self):
		"""
		The function should return a list of two images with highest rating
		"""
		create_vote(self.user1, 2, self.img1)
		create_vote(self.user1, 4, self.img2)
		last_day = timezone.now() - datetime.timedelta(days=1)
		top_images = Image.get_top_images(last_day, 2)
		self.assertEqual(len(top_images), 2)
		self.assertEqual(top_images[0].id, self.img2.id)
		self.assertEqual(top_images[1].id, self.img1.id)

	def testGetTopImagesInFuture(self):
		"""
		The function should return a list of two images with highest average rating
		"""
		create_vote(self.user1, 2, self.img1)
		create_vote(self.user1, 4, self.img2)
		last_day = timezone.now() + datetime.timedelta(days=1)
		top_images = Image.get_top_images(last_day, 1)
		self.assertEqual(len(top_images), 0)

	def testImageAvgRateSingleVote(self):
		"""
		The function should return the correct image's average rating
		"""
		create_vote(self.user1, 4, self.img1)
		avg_rate = self.img1.image_avg_rate
		self.assertEqual(avg_rate, 4)

	def testImageAvgRateMoreVotes(self):
		"""
		The function should return the correct image's average rating
		"""
		create_vote(self.user1, 3, self.img1)
		create_vote(self.user2, 4, self.img1)
		avg_rate = self.img1.image_avg_rate
		self.assertEqual(avg_rate, mean([3,4]))

	def testImageAvgRateNoVotes(self):
		"""
		The function should return None when image has no rating
		"""
		avg_rate = self.img1.image_avg_rate
		self.assertIsNone(avg_rate)


	def tearDown(self):
		self.user1.delete()
		self.user2.delete()
		self.img1.delete()
		self.img2.delete()


	