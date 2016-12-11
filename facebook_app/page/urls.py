from django.views.decorators.csrf import csrf_exempt
from django.conf.urls import url, patterns
from page.views import (PageView, list_page_view, Register, Login, UpdatePage)

urlpatterns = patterns('page.views',
                url(r'^v1/pages/$',
                    csrf_exempt(PageView.as_view())),
                url(r'^v1/register/$',
                    csrf_exempt(Register.as_view())),
                url(r'^v1/login/$',
                    csrf_exempt(Login.as_view())),
                url(r'^v1/listpage/(?P<user_id>\d+)$', 'list_page_view', name="list_page_view1"),
                url(r'^v1/updatepage/$',
                    csrf_exempt(UpdatePage.as_view())),
               )
              