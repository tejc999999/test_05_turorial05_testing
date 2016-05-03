# -*- coding: utf-8 -*-
# テスト
from django.test import TestCase

# Create your tests here.
from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import Question

import datetime

# テスト対象クラス：Question
class QuestionMethodTests(TestCase):

    # テスト対象メソッド：was_published_recently
    # 内容：未来日付がFalseで返るか
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is in the future.
        """
        # 未来日時（現在日時＋30日）作成
        time = timezone.now() + datetime.timedelta(days=30)
        # 未来日時のQuestionを作成
        future_question = Question(pub_date=time)
        # テスト：未来日時でwas_published_recentlyを使うとFalseが返る
        # assertEqualは２つの値が同じかどうかチェックする
        self.assertEqual(future_question.was_published_recently(), False)

    # テスト対象メソッド：was_published_recently
    # 内容：過去日時（30日以前）がFlaseで返るか
    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is older than 1 day.
        """
        # 現在日時から30日以前の日時を取得
        time = timezone.now() - datetime.timedelta(days=30)
        # 過去日時のQuestionを作成
        old_question = Question(pub_date=time)
        # テスト：過去日時でwas_published_recentlyを使うとFalseが返る
        self.assertEqual(old_question.was_published_recently(), False)

    # テスト対象メソッド：was_published_recently
    # 内容：最近日時（1時間以前）がTrueで返るか
    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() should return True for questions whose
        pub_date is within the last day.
        """
        #
        # 現在日時から1時間以内の日時を取得
        time = timezone.now() - datetime.timedelta(hours=1)
        # 最近日時のQuestionを作成
        recent_question = Question(pub_date=time)
        # テスト：最近日時でwas_published_recentlyを使うとTrueが返る
        self.assertEqual(recent_question.was_published_recently(), True)

# クラス内に記述しない（インデントなしで定義する）メソッドはクラスの持ち物ではなく、クラスと同列に扱われると思われる
# つまりClassがオブジェクトであるように、メソッドもオブジェクト扱いになると推測
# テスト用メソッド
# 指定した日付のQuestionを作成
def create_question(question_text, days):
    """
    Creates a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

# テスト対象ビュー：index
class QuestionViewTests(TestCase):

    # テスト対象：indexビュー
    # 内容：Questionがない状態で動作をチェック
    #  以下３点をチェック
    # ・HTTP200(正常）が返る
    # ・レスポンスのコンテンツに文字列「No polls are available.」が含まれる
    # ・レスポンスのコンテンツ「latest_question_list」のリストが空
    def test_index_view_with_no_questions(self):
        """
        If no questions exist, an appropriate message should be displayed.
        """
        # indexビューへのレスポンス生成
        response = self.client.get(reverse('polls:index'))
        # テスト：HTTP 200(正常）が返る
        self.assertEqual(response.status_code, 200)
        # テスト：レスポンス内容に規定の文字列が返る
        # assertContainsはレスポンスのコンテンツに指定のtextが含まれるか確認するメソッド
        # TestCase.assertContains(response, text, count=None, status_code=200)
        # response=レスポンス、text=チェック対象文字列、count=出現回数、status_code=HTTPステータス
        self.assertContains(response, "No polls are available.")
        # テスト：コンテンツ内の指定リストが空である
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    # テスト対象：indexビュー
    # 内容：Questionが過去日時（30日以前）の状態で動作をチェック
    # 以下をチェック
    # ・レスポンスのコンテンツ「latest_question_list」にリストに作成したQuestionが存在
    def test_index_view_with_a_past_question(self):
        """
        Questions with a pub_date in the past should be displayed on the
        index page.
        """
        create_question(question_text="Past question.", days=-30)
        # indexビューへのレスポンス生成
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    # テスト対象：indexビュー
    # 内容：Questionが未来日時（30日後の状態で動作をチェック
    # 以下２点をチェック
    # ・HTTP200(正常）が返る
    # ・レスポンスのコンテンツ「latest_question_list」のリストが空
    def test_index_view_with_a_future_question(self):
        """
        Questions with a pub_date in the future should not be displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        # indexビューへのレスポンス生成
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.",
                            status_code=200)
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    # テスト対象：indexビュー
    # 内容：Questionが２つ、過去日時（30日以前）と未来日時（30日後）の状態で動作をチェック
    # 以下をチェック
    # ・レスポンスのコンテンツ「latest_question_list」にリストに作成した２つのQuestionが存在
    def test_index_view_with_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        should be displayed.
        """
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        # indexビューへのレスポンス生成
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    # テスト対象：indexビュー
    # 内容：Questionが２つ、過去日時（30日以前）過去日時（5日後）の状態で動作をチェック
    # 以下をチェック
    # ・レスポンスのコンテンツ「latest_question_list」にリストに作成した２つのQuestionが存在
    def test_index_view_with_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        # indexビューへのレスポンス生成
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )

# テスト対象ビュー：detail
class QuestionIndexDetailTests(TestCase):

    # テスト対象：detailビュー
    # 内容：Questionが未来日時（1日後）の状態で動作をチェック
    #  以下をチェック
    # ・HTTP404(エラー）が返る
    def test_detail_view_with_a_future_question(self):
        """
        The detail view of a question with a pub_date in the future should
        return a 404 not found.
        """
        future_question = create_question(question_text='Future question.', days=5)
        response = self.client.get(reverse('polls:detail',
                                   args=(future_question.id,)))
        self.assertEqual(response.status_code, 404)

    # テスト対象：detailビュー
    # 内容：Questionが過去日時（5日前）の状態で動作をチェック
    #  以下をチェック
    # ・HTTP200(正常）が返る
    def test_detail_view_with_a_past_question(self):
        """
        The detail view of a question with a pub_date in the past should
        display the question's text.
        """
        past_question = create_question(question_text='Past Question.', days=-5)
        response = self.client.get(reverse('polls:detail',
                                   args=(past_question.id,)))
        self.assertContains(response, past_question.question_text,
                            status_code=200)