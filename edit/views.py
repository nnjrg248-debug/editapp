
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
            messagaes=[
                {"role":"system","content":"あなたは優秀なライターです。続きを執筆してください。"},
                {"role":"user","content":f"以下の文章の続きを書いてください{user_input}"},
            ],
            maz_tokens=200#1ドル予算なので1度に使いすぎぬよう短めに制限
        )   
        ai_text=response.choices[0].message.content
        return JsonResponse({'result':ai_text})
    except Exception as e:
            # ターミナルに具体的なエラー内容を表示させる
            print(f"エラーが発生しました: {e}")
            return JsonResponse({'error': str(e)}, status=500)
