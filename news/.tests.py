# from rest_framework.reverse import reverse
# from rest_framework.test import force_authenticate
# from .api import *
from django.test import (
    TestCase, 
    # RequestFactory,
)
import os 
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import (
    Post, 
    UaPostBody, 
    EnPostBody,
)
from .tasks import send_media
from unittests.mock import patch, MagicMock



from dotenv import load_dotenv
load_dotenv('.env')


# Create your tests here.
class SendMediaTaskTestCase(TestCase):
    def setUp(self):
        self.media_host_url = os.getenv('MEDIA_HOST_URL')
        self.post = Post.objects.create(preview_image=SimpleUploadedFile("test_preview_image.jpg", b"some_content"))
        self.ua_post_body = UaPostBody.objects.create(post=self.post, image=SimpleUploadedFile("test_ua_body_image.jpg", b"some_content"))
        self.en_post_body = EnPostBody.objects.create(post=self.post, image=SimpleUploadedFile("test_en_body_image.jpg", b"some_content"))

    def tearDown(self):
        pass

    @patch('requests.post')
    @patch('requests.put')
    def test_send_media_post(self, mock_post):
        # mock_post.return_value = MagicMock(status_code=200)

        # Call the task with the existing post ID
        send_media(self.post.id)

        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        print('mock_post.call_args: ', mock_post.call_args)
        self.assertIn('files', kwargs)
        self.assertIn('file', kwargs['files'])



# class ApiRootTestCase(TestCase): 
#     def setUp(self):
#         self.factory = RequestFactory()
#         self.user = User.objects.create(username='testuser', password='testpassword')
        
#     def test_api_root(self):
#         request = self.factory.get('', format='json')
#         force_authenticate(request, user=self.user)
#         response = api_root(request)
#         expected_data = {
#             'users': reverse('user-list', request=request),    
#             'posts': reverse('post-list', request=request),    
#         }
#         self.assertEqual(response.data, expected_data)
#         self.assertEqual(response.status_code, 200)