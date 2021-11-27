from main.models import SportKind, SportSegment, Event, EventSegment, Factor


def init_db_clean():
    SportKind.objects.all().delete()
    SportSegment.objects.all().delete()
    Event.objects.all().delete()
    EventSegment.objects.all().delete()
    Factor.objects.all().delete()


def init_sport(sport):
    if sport.get('kind') == 'sport':
        SportKind(fonkey=sport.get('id'), name=sport.get('name')).save()
    else:
        sport_kind = SportKind.objects.get(fonkey=sport.get('parentId'))
        SportSegment(fonkey=sport.get('id'), name=sport.get('name'), sport_kind=sport_kind).save()


def init_event(event):
    if event.get('name'):
        event_name = event.get('name')
    else:
        event_name = f"{event.get('team1', '')} - {event.get('team2', '')}"
    if event.get('level') == 1:
        event_ss = SportSegment.objects.get(fonkey=event.get('sportId'))
        event_sk = event_ss.sport_kind
        event_fullname = f"{event_sk.name} / {event_ss.name} / {event_name}"
        event_url = f"https://www.fonbet.ru/sports/{event_sk.fonkey}/{event_ss.fonkey}/{event.get('id')}"
        Event(fonkey=event.get('id'),
              name=event_name,
              full_name=event_fullname,
              url=event_url,
              is_live=event.get('place') == 'live',
              start_time=event.get('startTime'),
              sport_segment=event_ss
              ).save()
    elif event.get('level') == 2:
        parent_event = Event.objects.get(fonkey=event.get('parentId'))
        EventSegment(fonkey=event.get('id'),
                     name=event_name,
                     start_time=event.get('startTime'),
                     event=parent_event,
                     is_live=event.get('place') == 'live'
                     ).save()
    else:
        EventSegment(fonkey=event.get('id'),
                     name=event_name,
                     start_time=event.get('startTime'),
                     parent_id=event.get('parentId'),
                     is_live=event.get('place') == 'live'
                     ).save()


def init_event_misc(misc):
    current_event = Event.objects.filter(fonkey=misc.get('id')).first()
    if not current_event:
        current_event = EventSegment.objects.filter(fonkey=misc.get('id')).first()
        if not current_event:
            return True
    current_event.score_comment = misc.get('comment')
    current_event.score1 = misc.get('score1')
    current_event.score2 = misc.get('score2')
    current_event.save()


def init_factor(event):
    is_event = True
    current_event = Event.objects.filter(fonkey=event.get('e')).first()
    if not current_event:
        is_event = False
        current_event = EventSegment.objects.filter(fonkey=event.get('e')).first()
    for factor in event.get('factors'):
        if is_event:
            Factor(fonkey=factor.get('f'),
                   param=factor.get('p'),
                   value=factor.get('v'),
                   event=current_event).save()
        else:
            Factor(fonkey=factor.get('f'),
                   param=factor.get('p'),
                   value=factor.get('v'),
                   event_segment=current_event).save()


def init_event_block(block):
    current_event = Event.objects.filter(fonkey=block.get('eventId')).first()
    if not current_event:
        current_event = EventSegment.objects.filter(fonkey=block.get('eventId')).first()
    if block.get('state') == 'blocked':
        current_event.is_blocked = True
    elif block.get('state') == 'unblocked':
        current_event.is_blocked = False
    elif block.get('state') == 'partial':
        for factor_fonkey in block.get('factors'):
            factor = current_event.factors.filter(fonkey=factor_fonkey).first()
            print(factor)
            if not factor:
                continue
            factor.is_blocked = True
            factor.save()
    current_event.save()
