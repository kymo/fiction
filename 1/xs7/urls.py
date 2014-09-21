from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from reader.views import error
from search.views import search, search_detail_style
from reader.views import register, index, login_view, logout_view
import settings
from fiction.views import fiction_home, get_all_chapters, type_ranking_list, grading, category, get_category_number
from fiction.views import board, newest_catch, load_fiction_from_type, get_chapter_url, read_book, add_click_time_fiction, add_click_time_chapter
from fiction.views import get_recommond, get_fiction_and_chapter, chapter_home, all_chapters
from reader.views import add_shelf , check_name, validate, home, member, remove_shelf, helps, contact, version, feedback, save_read_log,get_history, del_history
from iknow.views import index_iknow, get_advice
from django.contrib import admin
from crawler.views import spider_start, update_thread
admin.autodiscover()
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'xs7.views.home', name='home'),
    # url(r'^xs7/', include('xs7.foo.urls')),
    url(r'^$', index),
    url(r'^search/', search),
    url(r'^register/', register),
    url(r'^login/', login_view),
    url(r'^logout/', logout_view),
    url(r'^(?P<nid>\d+)', home),
    url(r'^fiction/(?P<nid>\d+)/catelog/(?P<pid>\d*)', all_chapters),
    url(r'^fiction/(?P<nid>\d+)/(?P<index>\d+)/', chapter_home),
    url(r'^fiction/(?P<nid>\d+)', fiction_home),
    url(r'^site_media/(?P<path>.*)$','django.views.static.serve', {'document_root':settings.MEDIA_ROOT}),
    url(r'^validate', validate),
    url(r'^check_id', check_name),
    url(r'^member', member),
    url(r'^category', category),
    url(r'^board', board),
    url(r'^help', helps),
    url(r'^xs7/spider_start/', spider_start),
    url(r'^xs7/update_start/', update_thread),
    url(r'^iknow/', index_iknow),
    url(r'^send_advice_iknow/', get_advice),
    
    url(r'^contact', contact),
    url(r'^read_book', read_book),
    url(r'^version', version),
    url(r'^feedback', feedback),
    #ajax request
    url(r'^add_shelf/$', add_shelf),
    url(r'^del_read_history/$', del_history),
    url(r'^get_history/$', get_history),
    url(r'^search_for_detail_style/$', search_detail_style),
    url(r'^newest_catch/$', newest_catch),
    url(r'^save_read_log/$', save_read_log),
    url(r'^get_recommond/$', get_recommond),
    url(r'^get_fiction_and_newest_chapter/$', get_fiction_and_chapter),
    url(r'^get_category_number/', get_category_number),
    url(r'^add_click_time_fiction/', add_click_time_fiction),
    url(r'^add_click_time_chapter/', add_click_time_chapter),
    url(r'^get_chapter_url/', get_chapter_url),
    url(r'^load_fiction_from_type/', load_fiction_from_type),
    url(r'^remove/$', remove_shelf),
    url(r'^grading/$', grading),
    url(r'^check_id/$', check_name),
    url(r'get_all_chapters/', get_all_chapters),
    url(r'type_ranking_list/', type_ranking_list),
    #error page
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^.*/', error),
)
