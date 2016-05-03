# -*- coding: utf-8 -*-
# モデル
from __future__ import unicode_literals


from django.db import models
from django.utils import timezone

# importだけでもfromと同じ他のコード（モジュール）の読み込みができる
# fromと異なり、フルパスで使用する必要がある
# importだけで指定する場合、from ... import ...の後方に設定すること
# 例）from django.db import modelsはmodelsだけで使えるが、import modelsはdjango.db.modelsと書かないと使えない
import datetime

# Create your models here.

# Questionモデル
class Question(models.Model):
    # テキストフィールド
    # 最大200文字
    question_text = models.CharField(max_length=200)
    # 日付フィールド
    pub_date = models.DateTimeField('date published')

    # オブジェクト直接参照時にフィールドquestion_textを返す
    def __str__(self):
        return self.question_text

    # フィールドpub_dateが現在日時から1日以内かをチェックし、boolを返す
    def was_published_recently(self):
        # 未来日時に対応できないバグのためコメントアウト
        # return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
        # バグ修正
        # 現在日時を取得
        now = timezone.now()
        # 1日以内（前日より先）かつ現在日時以内を条件としてboolを返す
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

# Choiceモデル
class Choice(models.Model):
    # Questionを外部キーとし、Question1つにChoiceが結びつく
    # 制約はDELETE CASCADE
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # テキストフィールド
    # 最大200文字
    choice_text = models.CharField(max_length=200)
    # 数値フィールド
    # デフォルト値0
    votes = models.IntegerField(default=0)

    # オブジェクト直接参照時にフィールドchoice_textを返す
    def __str__(self):
        return self.choice_text