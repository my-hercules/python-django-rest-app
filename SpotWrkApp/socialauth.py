# coding=utf-8

from django.shortcuts import render_to_response
from django.template.context import RequestContext
from SpotWrkApp.models import *
from django.shortcuts import render

logger = logging.getLogger(__name__)


def get_user_avatar(backend, details, response, social_user, uid,
                    user, *args, **kwargs):
    """
    url = None
    if backend.__class__ == FacebookBackend:
        url = "http://graph.facebook.com/%s/picture?type=large" % response['id']

    if url:
        Profile = user.profile
        avatar = urlopen(url).read()
        fout = open("upload/"+user.username, "wb") #filepath is where to save the image
        fout.write(avatar)
        fout.close()
        Profile.profile_pic = url_to_image("upload/"+user.username) # depends on where you saved it
        Profile.save()
    """
    user.save()