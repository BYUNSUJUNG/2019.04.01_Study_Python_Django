from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_exempt
from survey.models import Survey, Answer
# Create your views here.

def main(request):
    survey = Survey.objects.filter(status="y").order_by("-survey_idx").first()

    return render_to_response("main.html",{"survey":survey})

def save_survey(request):
    dto = Answer(survey_idx=request.POST["survey_idx"],
    num=request.POST["num"])

    dto.save()
    return render_to_response("success.html")

def show_result(request):
    idx=request.GET['survey_idx']
    ans=Survey.objects.get(survey_idx=idx)
    answer=[ans.ans1,ans.ans2,ans.ans3,ans.ans4]

    surveyList=Survey.objects.raw(""""
    select
        survey_idx,num,count(num) sum_sum,
        round((select count(*) from survey_answer
                where survey_idx=a.survey_idx and num=a.num)*100.0 /
                (select count(*) form survey_answer where survey_idx=a.survey)
        from survey_answer a
        where survey_idx=%s
        group by survey_idx, num
        order by num
        """,idx)
   
    surveyList = zip(surveyList, answer)

    return render_to_response('request.html', {'surveyList':surveyList})