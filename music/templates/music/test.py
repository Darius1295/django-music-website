from PIL import Image
import os


media_path = '/Users/Darius/Documents/python_work/django_projects/website/media'

image_path = os.path.join(media_path, 'Oasis_-_Whats_The_Story_Morning_Glory_album_cover.jpg')

image1 = Image.open(image_path)
image1.show()