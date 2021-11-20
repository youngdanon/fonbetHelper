from django.db import models
from django.conf import settings
from .fonbet_parser import EventsParser
import schedule
import logging



class SportKind(models.Model):
    fonkey = models.IntegerField('sport_id')
    name = models.CharField('sport_name', max_length=255)

    def __str__(self):
        return self.name


class SportSegment(models.Model):
    fonkey = models.IntegerField('segment_id')
    name = models.CharField('segment_name', max_length=255)
    sport_kind = models.ForeignKey(SportKind, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    fonkey = models.IntegerField('event_id')
    full_name = models.TextField('event_full_name')
    url = models.URLField('event_url')
    team1 = models.CharField('team1', max_length=100)
    team2 = models.CharField('team2', max_length=100)
    score1 = models.IntegerField('score1')
    score2 = models.IntegerField('score2')
    score_comment = models.CharField('comment', max_length=255)
    is_live = models.BooleanField('is_live')
    start_time = models.DateTimeField('start_time')

    is_blocked = models.BooleanField('is_blocked', default=False)

    sport_segment = models.ForeignKey(SportSegment, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.full_name


class EventSegment(models.Model):
    fonkey = models.IntegerField('event_segment_id')
    name = models.CharField('event_segment_name', max_length=255)
    is_blocked = models.BooleanField('is_blocked', default='False')

    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Factor(models.Model):
    fonkey = models.IntegerField('factor_name', choices=settings.FACTOR_NAMES)
    param = models.IntegerField('param_value')
    value = models.DecimalField('value', decimal_places=2, max_digits=100)
    is_blocked = models.BooleanField('is_blocked', default=False)

    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)
    event_segment = models.ForeignKey(EventSegment, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.get_fonkey_display()