import hashlib
from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from customerinfo import conf
from customerinfo.models import Customer

register = template.Library()

@register.filter
def uname_display(user, img_only=False):
    # ftnm: first letter of name
    ftnm = None
    name = None
    email = None
    if isinstance(user, Customer):
        name = user.display_name()
    elif isinstance(user, User):
        if user.first_name and user.last_name:
            name = "%s, %s" % (user.last_name, user.first_name)
        else:
            name = user.username
    email = user.email
    ftnm = name[0].lower()
    nhash = hashlib.sha224(name.encode(conf.ENCODING)).hexdigest()[:32]
    if img_only:
        html = """\
<img class="cis-Image" src="%s/26/%s/%s"/>""" % (conf.AVATAR_BASE_URL,
                                                 ftnm,
                                                 nhash)
    else:
        html = """\
<img class="cis-Image" src="%s/26/%s/%s"/>\
<span title="%s">%s</span>""" % (conf.AVATAR_BASE_URL,
                                 ftnm, nhash, email, name)
    return mark_safe(html)

