from django import forms
from .models import Memo
class MemoForm(forms.ModelForm):
    class Meta:
        #class Meta: フォームに関するメタデータ（モデルや使用フィールド）を指定する内部クラスです。
        model=Memo#class Meta: フォームに関するメタデータ（モデルや使用フィールド）を指定する内部クラスです。
        #titleとcontentフィールドを持つフォームを生成
        fields=['title','content']#フォームに表示・保存するモデルのフィールドを指定
        #このフォームを使用することで、ビューでのデータ保存がform.save()だけで完結し、バリデーションも自動化