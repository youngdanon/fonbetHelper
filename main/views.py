from django.shortcuts import render
from .models import SportKind
from main.utils.fonbet_parser import EventsParser

fb_parser = EventsParser()


def live_events_request(request):
    events_content = {}
    sport_kinds = SportKind.objects.all()
    for sk in sport_kinds:
        sk_buffer = {}
        sk_segments = sk.segments.all()
        for ss in sk_segments:
            ss_buffer = {}
            live_events = ss.events.filter(is_live=True, is_blocked=False)
            for event in live_events:
                factors = event.factors.all()
                segments = event.segments.filter(is_live=True)
                server_time = fb_parser.get_server_timestamp()
                ss_buffer[event.name] = {'url': event.url,
                                         'timer': server_time - event.start_time,
                                         'score1': event.score1,
                                         'score2': event.score2,
                                         'score_comment': event.score_comment,
                                         'factors': factors,
                                         'segments': segments}
            sk_buffer[ss.name] = ss_buffer
        events_content[sk.name] = sk_buffer

    return render(request, template_name='main/events_page.html',
                  context={'events_content': events_content})
