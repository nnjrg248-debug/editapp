
from django.shortcuts import render, redirect, get_object_or_404
from .models import Memo
from .forms import MemoForm#フォーム使ってる場合

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

