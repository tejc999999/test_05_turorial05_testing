# -*- coding: utf-8 -*-
# URLマッピング

from django.conf.urls import url

from . import views

# 名前空間polls設定
app_name = 'polls'
# アクセスされたURLに対して、応答するビューを指定
urlpatterns = [
    # ex: /polls/
    # http://○○/polls/ にアクセスされた場合、汎用ビューIndexViewに渡す
    url(r'^$', views.IndexView.as_view(), name='index'),
    # ex: /polls/5/
    # http://○○/polls/番号/ にアクセスされた場合、汎用ビューDetailViewに渡す
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    # ex: /polls/5/results/
    # http://○○/polls/番号/result にアクセスされた場合、汎用ビューResultViewに渡す
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    # ex: /polls/5/vote/
    # http://○○/polls/番号/vote にアクセスされた場合、ビューvoteに渡す
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),

]