import loremipsum
import random

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError

from polls.models import (
    DemographicQuestion,
    DemographicQuestionResponse,
    Poll,
    PollResponse,
    Respondent)


lorem_words = loremipsum.Generator().words


class Command(BaseCommand):
    help = 'Generate some poll data'

    def handle(self, *args, **options):

        if Respondent.objects.count() < 20:
            for _ in range(20 - Respondent.objects.count()):
                generate_respondent()

        for active_poll in Poll.objects.filter(ended=None).exclude(started=None):
            if not active_poll.keywords.count():
                active_poll.end()

        owner, _ = User.objects.get_or_create(username="owner")

        for i in xrange(10):
            generate_a_poll(owner, ['A', 'B', 'C', 'D'])
            generate_a_poll(owner, ['yes', 'no'])
            generate_demographic_poll(owner)


def generate_respondent():
    respondent = Respondent()
    respondent.name = random_name()
    respondent.save()


def random_name():
    return random.choice(lorem_words) + str(random.randint(0, 2 ** 16))


def generate_a_poll(owner, choices):
    poll = Poll()
    poll.name = random_name()
    poll.user = owner
    poll.save()

    for choice in choices:
        create_category(poll, choice)

    poll.start()

    for respondent in Respondent.objects.all():
        response = PollResponse()
        response.poll = poll
        response.respondent = respondent
        choice = random.choice(choices)
        response.text = "LIFE %s %s" % (random.choice(lorem_words), choice)
        response.category = poll.find_category(choice, poll.categories)
        response.save()

    poll.end()


def create_category(poll, match):
    category = poll.categories.create(name=match)
    category.rules.create(match=match)
    category.save()


def generate_demographic_poll(owner):
    question = DemographicQuestion()
    question.question = loremipsum.get_sentence()
    question.created_by = owner
    question.modified_by = owner
    question.save()

    for respondent in Respondent.objects.all():
        answer = DemographicQuestionResponse()
        answer.question = question
        answer.respondent = respondent
        answer.response = loremipsum.get_sentence()
        answer.save()
