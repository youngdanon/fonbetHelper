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
    sport_kind = models.ForeignKey(SportKind, on_delete=models.CASCADE, null=True, blank=True, related_name='segments')

    def __str__(self):
        return self.name


class Event(models.Model):
    fonkey = models.IntegerField('event_id')
    name = models.TextField('name', default='EventName')
    full_name = models.TextField('event_full_name')
    url = models.URLField('event_url')
    score1 = models.IntegerField('score1', null=True)
    score2 = models.IntegerField('score2', null=True)
    score_comment = models.CharField('comment', max_length=255, null=True)
    is_live = models.BooleanField('is_live')
    start_time = models.IntegerField('start_time')
    is_blocked = models.BooleanField('is_blocked', default=False)
    sport_segment = models.ForeignKey(SportSegment, on_delete=models.CASCADE, null=True, blank=True,
                                      related_name='events')

    def __str__(self):
        return self.full_name


class EventSegment(models.Model):
    fonkey = models.IntegerField('event_segment_id')
    name = models.CharField('event_segment_name', max_length=255)
    score1 = models.IntegerField('score1', null=True)
    score2 = models.IntegerField('score2', null=True)
    score_comment = models.CharField('comment', max_length=255, null=True)
    is_blocked = models.BooleanField('is_blocked', default='False')
    start_time = models.IntegerField('start_time')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True, related_name='segments')
    parent_id = models.IntegerField('parent_id', default=-1)
    is_live = models.BooleanField('is_live', default=False)

    def __str__(self):
        return self.name


class Factor(models.Model):
    fonkey = models.IntegerField('factor_name', choices=settings.FACTOR_NAMES)
    param = models.IntegerField('param_value', null=True)
    value = models.DecimalField('value', decimal_places=2, max_digits=100)
    is_blocked = models.BooleanField('is_blocked', default=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True, related_name='factors')
    event_segment = models.ForeignKey(EventSegment, on_delete=models.CASCADE, null=True, blank=True,
                                      related_name='factors')

    def __str__(self):
        return str(self.get_fonkey_display())


class BlockLog(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True, related_name='blocks')
    event_segment = models.ForeignKey(EventSegment, on_delete=models.CASCADE, null=True, blank=True,
                                      related_name='blocks')

    time = models.DateTimeField('block_time', auto_now=True)
    factor_name = models.CharField('factor_name', max_length=1024)
    factor_param = models.IntegerField('factor_param', null=True)
    factor_value = models.DecimalField('factor_value', decimal_places=2, max_digits=100)
    score = models.CharField('score', max_length=255)
