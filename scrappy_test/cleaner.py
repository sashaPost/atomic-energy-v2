# EXECUTE THE SCRIPT WITH 'python manage.py shell' to avoid import conflicts.
# Get the root directory of your Django project (where manage.py is located)
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
SETTINGS_MODULE = 'atomic_energy.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', SETTINGS_MODULE)

# Now you can safely import your Django settings
import django
django.setup()

from django.db.models import Q
from bs4 import BeautifulSoup
from news.models import *



ua_bodies = UaPostBody.objects.exclude(image=False)
en_bodies = EnPostBody.objects.exclude(image=False)



# !!! PREPARED FOR 'varitas.space' !!!
# rename 'div' to 'a' after that & add style (vikt - tg)

def fix_ua(bodies):
    for body in bodies:
        img = body.image
        print(img)
        soup = BeautifulSoup(body.message_ua, 'html.parser')
        # divs_with_src = soup.find_all('div', {'src': True})
        divs = soup.find_all('div')
        
        for div in divs:
            div.decompose()
            
        # !!! FIX THIS '<div>' TO DESIRED ELEMENT !!!
        # new_div = soup.new_tag('div')
        new_a = soup.new_tag('a')
        image_name = str(img).split('/')[-1]
        # !!! CHANGE DOMAIN !!!
        new_img = soup.new_tag('img', src=os.path.join('https://varitas.space/media/images', image_name))
        # new_img = soup.new_tag('img', src=os.path.join('https://172.31.254.92/media/images', image_name))
        new_img['style'] = "width: 100%;"
        new_a.append(new_img)
        soup.append(new_a)
        print(soup)
        db_img = os.path.join('images', image_name)
        body.image = db_img
        body.message_ua = str(soup)
        body.save()
        print('----------')
        print(body)
        print('################################################################')

    return True

def fix_eng(bodies):
    for body in bodies:
        img = body.image
        print(img)
        soup = BeautifulSoup(body.message_eng, 'html.parser')
        # divs_with_src = soup.find_all('div', {'src': True})
        divs = soup.find_all('div')
        
        for div in divs:
            div.decompose()
            
        # !!! FIX THIS '<div>' TO DESIRED ELEMENT !!!
        # new_div = soup.new_tag('div')
        new_a = soup.new_tag('a')
        image_name = str(img).split('/')[-1]    
        # !!! CHANGE DOMAIN !!!
        new_img = soup.new_tag('img', src=os.path.join('https://varitas.space/media/images', image_name))
        # new_img = soup.new_tag('img', src=os.path.join('https://172.31.254.92/media/images', image_name))
        new_img['style'] = "width: 100%;"
        
        new_a.append(new_img)
        soup.append(new_a)
        print(soup)
        db_img = os.path.join('images', image_name)
        body.image = db_img
        body.message_eng = str(soup)
        body.save()
        print('----------')
        print(body)
        print('################################################################')

    return True

print(fix_ua(ua_bodies))
print(fix_eng(en_bodies))
