
from django.shortcuts import render, redirect, get_object_or_404
from .models import Memo,Post
from .forms import MemoForm#フォーム使ってる場合
from django.contrib.auth.mixins import LoginRequiredMixin#ログインしてないアクセスはsettingsのURLに戻る設定
from django.views.generic import ListView,CreateView,UpdateViwe,DeteteView
from django.urls import reverse_lazy#管廊後の移動先指定につかう

#1.記事一覧（誰でも見れる）
class PostListView(ListView):
    modeo=Post
    template_name='post_list.html'

#2記事作成（ログインが必要）
class PostCreateView(LoginRequiredMixin,CreateView):
    model=Post
    fields=['title','']
    template_name='post_form.html'
    success_url=reverse_lazy('post_list.html')

#3.記事編集(ログインが必要)
class PostUpdateView(LoginRequiredMixin,UpdateView):
    model=Post
    fields=['title','content']
    template_name='post_form.html'
    success_url=reverse_lazy('post_list.html')

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

