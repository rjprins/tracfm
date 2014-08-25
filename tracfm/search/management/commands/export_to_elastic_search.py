from django.core.management.base import BaseCommand, CommandError
from elasticsearch import Elasticsearch

from polls.models import (
    DemographicQuestion,
    DemographicQuestionResponse,
    Poll,
    PollResponse,
    Respondent)


# Assuming we exporting to localhost:9200
es = Elasticsearch()


class Command(BaseCommand):
    help = 'Export poll data to an elasticsearch instance'

    def handle(self, *args, **options):
        export_all_respondents()
        export_all_polls()
        export_all_responses()
        export_all_questions()
        export_all_answers()


def export_all_respondents():
    for respondent in Respondent.objects.all():
        es.index(index="tracfm",
                 doc_type="respondent",
                 id=respondent.id,
                 body={'name': respondent.name})


def export_all_polls():
    for poll in Poll.objects.all():
        es.index(index="tracfm",
                 doc_type="poll",
                 id=poll.id,
                 body={'name': poll.name})


def export_all_responses():
    for response in PollResponse.objects.all():
        es.index(index="tracfm",
                 doc_type="response",
                 id=response.id,
                 body={'respondent': response.respondent.id,
                       'poll': response.poll.id,
                       'text': response.text,
                       'category': response.category.name})


def export_all_questions():
    for question in DemographicQuestion.objects.all():
        es.index(index="tracfm",
                 doc_type="demographic_question",
                 id=question.id,
                 body={'question': question.question})


def export_all_answers():
    for answer in DemographicQuestionResponse.objects.all():
        es.index(index="tracfm",
                 doc_type="demographic_answer",
                 id=answer.id,
                 body={'demographic_question': answer.question.id,
                       'respondent': answer.respondent.id,
                       'response': answer.response})
