
from django.urls import path,include
from .import views
from .views import PostListView,PostCreateView,PostUpdateView#作ったViweをインポート
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView,RedirectView
from django.http import HttpResponse

'''

from django.urls import path,include from .import viewsのちがいで
from django.urls import path,includeはfromファイル名importメソッド名 
from .import viewsはfrom.（ディレクトリ名)fromファイル名だが

「どこから」「何を」インポートするかという点で決定的な違いあり
from django.urls import path, include: Djangoの外部ライブラリから、機能（関数）を取り込む。
from . import views: 現在と同じフォルダ内にある views.py を、モジュール全体として取り込む

'''
urlpatterns=[

    path('',PostListView.as_view(),name='post_list'),                #←←←←←←←←どうして path('', views.memo_list, name='post_list'), が一番か？
#↑name='login' にしてはいけないDjangoが用意したログイン専用のViewにすでに割り当照られているので、
# name='login' と付けてしまうと、名前が重複となる
    path('post/new/',PostCreateView.as_view(),name='post_create'),# クラスベース 
    #クラスベースはviewの中でのif request.method == "POST"の処理分岐がいらずmodel = Postという記載で処理してくれる
    
    path('post/<int:pk>/edit/',PostUpdateView.as_view(),name='post_edit'),
 
    path('',views.memo_list,name='memo_list'),#上の「path('',PostListView.～」第一引数同じなのでその場合下の行は無視される
    path('list',views.memo_list,name='memo_list'),# name='memo_list'は href="{% url 'memo_list' %}"で呼ばれるが第一引数を変えることで第一引数がかぶらなくなったので問題なし
    path('new/',views.memo_create,name='memo_create'),#関数ベース htmlから第3引数のボタン押されたら第1引数のURLで第2引数もメソッドが実行される
    path('edit/<int:pk>',views.memo_edit,name='memo_edit'),
    #↑第一引数のpkがviewsのmemo_editのurlでの表示のみで第2引数が指定される
    #またmemo_form.htmlでmemo_editの第2引数として指定されている
    path('delete/<int:pk>',views.memo_delete,name='memo_delete'),
  # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('ai-generate/',views.ai_generate,name='ai_generate'),

    #viewなしで遷移できるTemplatesview 
    path('aboutssss/',TemplateView.as_view(template_name="kkkk.html"),name="lllll"),
    #view,templatesなしで遷移できるTemplatesview 「中身のない静的なページ」であれば、urls.pyに1行足すだけで、views.pyに何も書かずに遷移を実現
    path('aboutssss2/',lambda request:HttpResponse("表示だけのテスト view、templatesなしでurlsに1行追加するだけでよいHttpResponse関数<br>またこのように改行もボタンも書ける<a href='/accounts/login/'>遷移ボタン</a>"),name="cccc") ,
    #↑HttpResponese関数の文字列に追加した遷移ボタンの遷移先だが{% url %}の書き方はテンプレートの中だけで動く書き方、この場合はurlの指定を'/accounts/login/'とする、
    #これでよい理由は親urlの上のほうでpath('accounts/', include('django.contrib.auth.urls'))としてるので
    #親のaccountsとsetteingsのLOGIN_URL = 'login'（#未ログイン時飛ばされるところ、またviewにはname=’login’という指定はない）を組み合わせ'/accounts/login/'で指定している(このurl/accounts/login/'は頭に/をつけてるが、つけないと相対パス(その時のurlからのパス)になるので注意、
    #またurlを/registration/login.htmlと直接指定しも遷移できないのは、ブラウザからのリクエストは必ず urls.py が受け取り、View（プログラム） が許可したものだけが画面に表示するので（Djangoはこの「直接指定」を禁止）(通常http://.../login.htmlとすれば開くかもしれんが)
    #またpath('aboutssss2/',lambda,HTTp.Response( ～としているが
    #↑もう1つ上のpath関数の第一引数aboutssssと被ると行が無視されるとのこと名でaboutssss2とした

    # 上記path関数の場合文字列を表示させるHPに移動させてボタン押させloginページに飛ばすが直接ログインp-時に飛ばすときは以下の RedirectView.asview(url'/accounts/login/'～とする
    path('old-link/', RedirectView.as_view(url='/accounts/login/'), name='go-to-login'),
   
    
]