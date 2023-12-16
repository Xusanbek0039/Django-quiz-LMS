from quiz.models import Quiz, Question



def check_theory_q(quiz, dic):
    
    question = Question.objects.filter(quiz=quiz, is_theory_question=True)

    if question.count() >= quiz.number_of_theory_questions:
        return True
    else:
        dic[quiz.name] = quiz.number_of_theory_questions
        return False


def check_chose_q(quiz, dic):
    question = Question.objects.filter(quiz=quiz, is_theory_question=False)

    if question.count() >= quiz.number_of_chosen_questions:
        return True
    else:
        dic[quiz.name] = quiz.number_of_chosen_questions
        return False
