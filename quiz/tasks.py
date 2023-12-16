from celery import shared_task

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from quiz.models import Quiz, IntervalQuiz, Question, ReportResult, TotalDegree

import datetime

from sentence_transformers import SentenceTransformer, util



def update_quiz_and_interval(q):
    Quiz.objects.filter(name=q.name).update(
        is_answered=True
    )
    IntervalQuiz.objects.get(quiz=q).delete()


channel_layer = get_channel_layer()


@shared_task
def interval():
    context = {}
    for q in Quiz.objects.filter(is_answered=False):
        current_time = datetime.datetime.utcnow() + datetime.timedelta(hours=2)

        q_time = datetime.datetime.strptime(q.start_quiz.strftime("%d/%m/%Y %H:%M:%S"), "%d/%m/%Y %H:%M:%S")
        c_time = datetime.datetime.strptime(current_time.strftime("%d/%m/%Y %H:%M:%S"), "%d/%m/%Y %H:%M:%S")
        print(q_time)
        print(c_time)

        if q_time >= c_time:
            context[str(q.id)] = {'time_now': str(abs(q_time - c_time)), 'is_start': False}

        else:
            if not IntervalQuiz.objects.filter(quiz=q).exists():
                hours, minutes = divmod(q.time, 60)
                quiz_interval = IntervalQuiz.objects.create(quiz=q,
                                                            intervalTime=datetime.time(hour=hours, minute=minutes))

                q_end_in = quiz_interval.intervalTime

                q_endin = datetime.datetime.strptime(q_end_in.strftime("%H:%M:%S"), "%H:%M:%S")

                q_interval = datetime.datetime.strptime(datetime.time(second=1).strftime("%H:%M:%S"), "%H:%M:%S")

                up = IntervalQuiz.objects.filter(quiz=quiz_interval.quiz)

                up.update(
                    intervalTime=str(q_endin - q_interval)
                )
                for loop in up:
                    context[str(q.id)] = {'time_now': str(loop.intervalTime), 'is_start': True}

            else:
                constant_time = datetime.time(hour=0, minute=0, second=0)

                get_current_interval = IntervalQuiz.objects.get(quiz=q)

                q_end_in = get_current_interval.intervalTime

                q_endin = datetime.datetime.strptime(q_end_in.strftime("%H:%M:%S"), "%H:%M:%S")

                q_interval = datetime.datetime.strptime(datetime.time(second=1).strftime("%H:%M:%S"), "%H:%M:%S")

                if not q_end_in == constant_time:
                    up = IntervalQuiz.objects.filter(quiz=get_current_interval.quiz)

                    up.update(
                        intervalTime=str(q_endin - q_interval)
                    )

                    for loop in up:
                        context[str(q.id)] = {'time_now': str(loop.intervalTime), 'is_start': True}

                else:
                    context[str(q.id)] = {'time_now': str(constant_time), 'is_start': 'ended'}

                    update_quiz_and_interval(q)


    async_to_sync(channel_layer.group_send)(
        'group_layer',
        {
            'type': 'send_interval_group',
            'message': context
        }
    )




def create_report_result(quiz, user, question, student_answer, correct_answer, is_true_answered, question_score):
       ReportResult.objects.create(
                user=user,
                quiz=quiz,
                question=question,
                student_answer=student_answer,
                correct_answer=correct_answer,
                is_true_answered=is_true_answered,
                question_score=question_score
            )

@shared_task
def check_theory(data, user, quiz_id):
    score = 0
    num_of_q = 0

    model_name = 'multi-qa-MiniLM-L6-cos-v1'
    quiz = Quiz.objects.get(id=int(quiz_id))

    for ids in data.keys():
        question = Question.objects.get(id=ids)

        if not data[ids]['answer'] == 'not_answered':

            if data[ids]['is_theory'] == 'True':
                model = SentenceTransformer(model_name)

                query_embedding = model.encode(question.theory_answer)
                passage_embedding = model.encode([data[ids]['answer']])

                dd = float(util.dot_score(query_embedding, passage_embedding)[0][0])

                if dd >= 0.2:
                    score += 1
                    num_of_q +=1
                    create_report_result(quiz, user, question.question, data[ids]['answer'], question.theory_answer, 'Correct theory answer', 1)
                else:
                    num_of_q += 1
                    create_report_result(quiz, user, question.question, data[ids]['answer'], question.theory_answer, 'Incorrect theory answer', 0)

            else:
                correct_chose = question.correct_chosen

                if data[ids]['answer'] == correct_chose:
                    score += 1
                    num_of_q += 1
                    create_report_result(quiz, user, question.question, data[ids]['answer'], correct_chose, 'Correct chosen answer', 1)


                else:
                    num_of_q += 1
                    create_report_result(quiz, user, question.question, data[ids]['answer'], correct_chose, 'Incorrect chosen answer', 0)

        else:
            if data[ids]['is_theory'] == 'True':
                num_of_q +=1
                create_report_result(quiz, user, question.question, 'Not answered!!', question.theory_answer, 'Not answered!!', 0)
            else:
                num_of_q +=1
                create_report_result(quiz, user, question.question, 'Not answered!!', question.correct_chosen, 'Not answered!!', 0)
    TotalDegree.objects.create(
        user=user,
        quiz=quiz,
        score_to_pass=quiz.required_score_to_pass,
        total=score*100/num_of_q
    )

