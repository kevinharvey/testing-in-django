from django import template
from django.conf import settings

register = template.Library()

@register.inclusion_tag("includes/user_votes.html", takes_context=True)
def user_votes(context, question):
    votes = context['request'].session.get('%s%s' % (settings.TORQUEMADA_SESSION_VOTES_PREFIX, question.pk), False)
    context['votes'] = votes
    return context

@register.inclusion_tag("includes/user_vote_links.html", takes_context=True)
def user_vote_links(context, question):
    vote = context['request'].session.get('%s%s' % (settings.TORQUEMADA_SESSION_VOTES_PREFIX, question.pk), 0)
    context['vote'] = vote
    return context
