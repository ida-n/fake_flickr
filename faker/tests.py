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
	img = SimpleUploadedFile(
		name='test', 
		content=open(os.path.join(settings.BASE_DIR, 'faker', 'test.jpg'), 'rb').read(), 
		content_type='image/jpeg')
	return Image.objects.create(description=description,
							   user=user,
							   imgfile=img)

def create_vote(user, rate, image):
	return Vote.objects.create(rate=rate,
							   user=user,
							   image=image)

class ImageViewTest(TestCase):
	def setUp(self):
		self.factory = RequestFactory()
		self.user = User.objects.create_user(
			username='test', email='test@example.com', password='!password')
		self.img = create_image(self.user, "test image")

	def testAccessIndexAsAnonymousUser(self):
		response = self.client.get(reverse('faker:index'))
		self.assertEqual(response.status_code, 200)
		self.assertQuerysetEqual(response.context['last_day_img_list'], ['<Image: test image>'])
		self.assertQuerysetEqual(response.context['last_week_img_list'], ['<Image: test image>'])
	
	def testAccessImagesAsAnonymousUser(self):
		response = self.client.get(reverse('faker:images'))
		self.assertEqual(response.status_code, 200)
		self.assertQuerysetEqual(response.context['img_list'], ['<Image: test image>'])

	def testAccessMyImagesAsAnonymousUser(self):
		request = self.factory.get('faker:my_images')
		request.user = AnonymousUser()
		response = my_images(request)
		self.assertEqual(response.status_code, 302)

	def testAccessMyImagesAsLoggedInUser(self):
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
		create_vote(self.user1, 2, self.img1)
		create_vote(self.user1, 4, self.img2)
		last_day = timezone.now() - datetime.timedelta(days=1)
		top_images = Image.get_top_images(last_day, 1)
		self.assertEqual(len(top_images), 1)
		self.assertEqual(top_images[0].id, self.img2.id)

	def testGetSingleTopImageMoreVotes(self):
		create_vote(self.user1, 2, self.img1)
		create_vote(self.user1, 4, self.img2)
		create_vote(self.user2, 3, self.img1)
		create_vote(self.user2, 4, self.img2)
		last_day = timezone.now() - datetime.timedelta(days=1)
		top_images = Image.get_top_images(last_day, 1)
		self.assertEqual(len(top_images), 1)
		self.assertEqual(top_images[0].id, self.img2.id)

	def testGetTopImagesSingleVote(self):
		create_vote(self.user1, 2, self.img1)
		create_vote(self.user1, 4, self.img2)
		last_day = timezone.now() - datetime.timedelta(days=1)
		top_images = Image.get_top_images(last_day, 2)
		self.assertEqual(len(top_images), 2)
		self.assertEqual(top_images[0].id, self.img2.id)
		self.assertEqual(top_images[1].id, self.img1.id)

	def testGetTopImagesInFuture(self):
		create_vote(self.user1, 2, self.img1)
		create_vote(self.user1, 4, self.img2)
		last_day = timezone.now() + datetime.timedelta(days=1)
		top_images = Image.get_top_images(last_day, 1)
		self.assertEqual(len(top_images), 0)

	def testImageAvgRateSingleVote(self):
		create_vote(self.user1, 4, self.img1)
		avg_rate = self.img1.image_avg_rate
		self.assertEqual(avg_rate, 4)

	def testImageAvgRateMoreVotes(self):
		create_vote(self.user1, 3, self.img1)
		create_vote(self.user2, 4, self.img1)
		avg_rate = self.img1.image_avg_rate
		self.assertEqual(avg_rate, mean([3,4]))

	def testImageAvgRateNoVotes(self):
		avg_rate = self.img1.image_avg_rate
		self.assertIsNone(avg_rate)
	
	

	def tearDown(self):
		self.user1.delete()
		self.user2.delete()
		self.img1.delete()
		self.img2.delete()


	