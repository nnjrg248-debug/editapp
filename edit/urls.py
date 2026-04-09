
from django.urls import path,include
from .import views
from .views import PostListView,PostCreateView,PostUpdateView#作ったViweをインポート
'''

from django.urls import path,include from .import viewsのちがいで
from django.urls import path,includeはfromファイル名importメソッド名 
from .import viewsはfrom.（ディレクトリ名)fromファイル名だが

「どこから」「何を」インポートするかという点で決定的な違いあり
from django.urls import path, include: Djangoの外部ライブラリから、機能（関数）を取り込む。
from . import views: 現在と同じフォルダ内にある views.py を、モジュール全体として取り込む


'''
urlpatterns=[

    path('',PostListView.as_view(),name='post_list'),
    path('post/new/',PostCreateView.as_view(),name='post_create'),
    path('post/<int:pk>/edit/',PostUpdateView.as_view(),name='post_edit'),
 
    path('',views.memo_list,name='memo_list'),
    path('new/',views.memo_create,name='memo_create'),
    path('edit/<int:pk>',views.memo_edit,name='memo_edit'),
    #↑第一引数のpkがviewsのmemo_editのurlでの表示のみで第2引数が指定される
    #またmemo_form.htmlでmemo_editの第2引数として指定されている
    path('delete/<int:pk>',views.memo_delete,name='memo_delete'),
]