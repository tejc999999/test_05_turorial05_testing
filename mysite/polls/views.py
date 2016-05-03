# -*- coding: utf-8 -*-
# ビュー

# 他ファイルからのコード読み込み
# JavaのimportやC言語のincludeと同様
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

# 1つ上のフォルダmodelsから読み込み(.modules)
from .models import Choice, Question

# index用汎用ビュー
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        # return Question.objects.order_by('-pub_date')[:5]
        # 現在日時以前のクエリセットを取得するように修正
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

# detail用汎用ビュー
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        # 現在日時のQuestionを取得
        return Question.objects.filter(pub_date__lte=timezone.now())

# results用汎用ビュー
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    # index用のビュー、HttpRequestを受け取り、HttpResponseを返す
    # 初期表示画面
    '''
    def index(request):
        # pub_dateの降順でDBからQuestionを取得
        latest_question_list = Question.objects.order_by('-pub_date')[:5]
        # テンプレートを読み込み
        template = loader.get_template('polls/index.html')
        # 取得した複数のQuestionを辞書登録
        context = {
            'latest_question_list': latest_question_list,
        }
        # render()を使わないパターン
        # return HttpResponse(template.render(context, request))
        # render()を使うパターン
        return render(request, 'polls/index.html', context)
    '''

    # detail用のビュー
    # 詳細表示画面
    '''
    def detail(request, question_id):
        # pkを受け取ったIDとして検索、取得データがない場合は404を受け取る
        # return HttpResponse("You're looking at question %s." % question_id)
        question = get_object_or_404(Question, pk=question_id)
        return render(request, 'polls/detail.html', {'question': question})
    '''
    # results用のビュー
    # 投票結果画面
    '''
    def results(request, question_id):
        # 受け取った番号でDBからQuestionを取得、ない場合は404を取得
        question = get_object_or_404(Question, pk=question_id)
        return render(request, 'polls/results.html', {'question': question})
    '''

# vote用のビュー
# 投票画面？
def vote(request, question_id):
    # 受け取った番号でDBからQuestionを取得、ない場合は404を取得
    question = get_object_or_404(Question, pk=question_id)
    # 例外処理、Javaのtry～catchと同様、elseはtryでエラーが発生しなかった場合に動作するブロック
    try:
        # POSTされてきた番号をpkとしてquestionに紐づいたchoiceを取得する
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    # データが存在しないエラーをキャッチ
    except (KeyError, Choice.DoesNotExist):
        # detail.htmlを返す
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        # choiceに投票されたとしてフィールドvoteを+1
        selected_choice.votes += 1
        # DBに保存
        selected_choice.save()
        # リダイレクト先をURLconfから取得
        # args()がよく分からないが、URLの後ろに/番号/を付ける処理と思われる
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

# Create your views here.
