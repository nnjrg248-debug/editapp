
from django.shortcuts import render, redirect, get_object_or_404
from .models import Memo,Post
from django.http import JsonResponse
from openai import OpenAI
from django.conf import settings

from .forms import MemoForm#フォーム使ってる場合
from django.contrib.auth.mixins import LoginRequiredMixin#ログインしてないアクセスはsettingsのURLに戻る設定
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy#管廊後の移動先指定につかう
from django.contrib.auth.decorators import login_required#関数ベースのログイン制限

from django.core.mail import send_mail
from django.http import HttpResponse
import logging
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.core.mail import send_mail


#上記関数のインポートで波線立ってるので以下のように対処
#ターミナルで pip show django
#Ctrl + Shift + P (Macは Cmd + Shift + P) を押す。
#「Python: Select Interpreter」 と入力して選択。
#「インタープリターパスを入力」　を選択
#リストの中から 「('venv': venv)」 
#とするのは仮想環境が別のフォルダに作ってある場合でこのPCではまだ作ってないので以下のようにする
#python -m venv venv
#Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Proce#s
#venv\Scripts\activate
#「pip install django openai」
#Ctrl + Shift + P (Macは Cmd + Shift + P) を押す。
#「Python: Select Interpreter」 と入力して選択。
#リストの中から 「('venv': venv)」 など、Djangoをインストールした仮想環境のパスが含まれるものを選択



#1.記事一覧（誰でも見れる）
class PostListView(ListView):
    model = Memo
    template_name='edit/post_list.html'

#2記事作成（ログインが必要）
class PostCreateView(LoginRequiredMixin,CreateView):
    model=Post
    fields=['title','']
    template_name='post_form.html'
    success_url=reverse_lazy('post_list')

#3.記事編集(ログインが必要)
class PostUpdateView(LoginRequiredMixin,UpdateView):
    model=Post
    fields=['title','content']
    template_name='post_form.html'
    success_url=reverse_lazy('post_list')

@login_required # これ追加で未ログイン時ここに飛ばされない
def memo_list(request):
    memos=Memo.objects.all().order_by('-created_at')
    return render(request,'edit/memo_list.html',{'memos':memos})

# Create your views here.
def memo_create(request):
    if request.method=="POST":
        form=MemoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('memo_list')
    else:
            form=MemoForm() # 空のフォームを用意
    return render(request,'edit/memo_form.html',{'form':form})

def memo_edit(request,pk):
     #pk(ID)に一致するメモを取得、なければ404エラーを出す
     memo=get_object_or_404(Memo,pk=pk)
#↑ﾃﾞｰﾀﾍﾞｰｽMemoを探しに行ってる（なかったらここでエラー(強制終了)を出し
# あったらMemoのDBがはいる）
     if request.method=="POST":
        #既存のデータ(instance=memo)をベースに入力内容(request.POST)を反映
        form=MemoForm(request.POST,instance=memo)
        if form.is_valid():
             form.save()
             return redirect('memo_list')
     else:
        #編集画面を開いたときに、既存の内容をフォームに表示させる
        form=MemoForm(instance=memo)
     return render(request,'edit/memo_form.html',{'form':form})

def memo_delete(request,pk):
    memo=get_object_or_404(Memo,pk=pk)
    if request.method=="POST":
        memo.delete()
        return redirect('memo_list')
#POST（ボタン押下）でないときは、確認画面(html)を出すだけ
    return render(request,'edit/memo_confirm_delete.html',{'memo':memo})

def ai_generate(request):
    try:
        #ユーザが入力した「タイトル」、「冒頭の分を取得」
        user_input=request.GET.get('text','')

        client = OpenAI(api_key=settings.OPENAI_API_KEY)

        #AIにリクエスト送る
        response=client.chat.completions.create(
            model="gpt-4o-mini", # 安くて速いモデル。gpt-5-nanoより安定
            messages=[
                {"role":"system","content":"あなたは優秀なライターです。続きを執筆してください。"},
                {"role":"user","content":f"以下の文章の続きを書いてください{user_input}"},
            ],
            max_tokens=200#1ドル予算なので1度に使いすぎぬよう短めに制限
        )   
        ai_text=response.choices[0].message.content
        return JsonResponse({'result':ai_text})
    except Exception as e:
            # ターミナルに具体的なエラー内容を表示させる
            print(f"エラーが発生しました: {e}")
            return JsonResponse({'error': str(e)}, status=500)
    



def test_email_view(request):
    send_mail(
        'AI料理アプリ（テスト）',
        '受け取りました。これから解析します！',
        'from@example.com',
        ['nnjrg248@gmail.com'],
        fail_silently=False,
    )
    return HttpResponse("テストメールを送信しました。")





logger = logging.getLogger(__name__) #グローバル変数（外部変数）のようなもの

@csrf_exempt  # SendGridからの外部アクセスを許可
def handle_inbound_email(request):
    if request.method == 'POST':
        # 1. データの抽出
        sender = request.POST.get('from')    # 送信者のメールアドレス
        subject = request.POST.get('subject') # メールの件名
        body = request.POST.get('text')      # メールの本文
       
        # 添付ファイル（写真）がある場合
        if request.FILES:
            for file_name in request.FILES:
                photo = request.FILES[file_name]
                # ここで写真を保存したり、AI（Gemini等）に渡したりする
                logger.info(f"写真を受信しました: {photo.name}")

        # 2. とりあえずの自動返信（土台作り）
        send_mail(
            f"Re: {subject}",
            "メールを受け取りました！現在AIが料理を考えています...",
            'admin@1q1q.xyz',  # 送信元（自分のドメイン）
            [sender],         # 送ってきた相手へ返信
            fail_silently=False,
        )

        return HttpResponse(status=200) # SendGridに成功を伝える
   
    return HttpResponse(status=405)