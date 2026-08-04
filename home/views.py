from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from .models import AgencyProfile, Discussion, NewsArticle, Mission, TimelineEvent, SpaceObject
from .forms import DiscussionForm, ReplyForm



def _bar_color(rank):
    # Tiered accent colours for the horizontal bar charts.
    if rank < 2:
        return 'var(--accent)'
    if rank < 4:
        return 'var(--terra)'
    return 'var(--teal)'


def home_page(request):
    from collections import defaultdict

    # --- Objects launched, aggregated by country (merges stray 'Brazil,' etc.) ---
    raw = SpaceObject.objects.values('state_organization').annotate(c=Count('id'))
    tally = defaultdict(int)
    for row in raw:
        name = (row['state_organization'] or '').strip().rstrip(',').strip()
        if name:
            tally[name] += row['c']
    ranked = sorted(tally.items(), key=lambda kv: kv[1], reverse=True)[:10]
    max_obj = ranked[0][1] if ranked else 1
    objects_data = [
        {
            'country': name,
            'value': count,
            'pct': round(count * 100 / max_obj, 1),
            'color': _bar_color(i),
        }
        for i, (name, count) in enumerate(ranked)
    ]

    # --- Government spending (top spenders, in millions USD) ---
    spenders = (AgencyProfile.objects
                .exclude(annual_government_spending__isnull=True)
                .exclude(annual_government_spending=0)
                .order_by('-annual_government_spending')[:10])
    max_spend = spenders[0].annual_government_spending if spenders else 1
    spending_data = [
        {
            'country': a.country_name,
            'millions': round(a.annual_government_spending / 1_000_000),
            'pct': round(a.annual_government_spending * 100 / max_spend, 1),
            'color': _bar_color(i),
        }
        for i, a in enumerate(spenders)
    ]

    # --- Nations rail + stat strip ---
    agencies = AgencyProfile.objects.all().order_by('country_name')

    return render(request, 'home/home_page.html', {
        'objects_data': objects_data,
        'spending_data': spending_data,
        'agencies': agencies,
        'num_agencies': agencies.count(),
        'num_objects': SpaceObject.objects.count(),
    })

def dashboard(request):
    from collections import defaultdict
    from .space_data import WORLD_AGENCIES

    agencies = sorted(WORLD_AGENCIES, key=lambda a: a['budget'], reverse=True)

    total_budget = sum(a['budget'] for a in agencies)          # USD millions
    regions = sorted({a['region'] for a in agencies})

    by_region = defaultdict(float)
    for a in agencies:
        by_region[a['region']] += a['budget']
    region_data = sorted(
        [{'label': r, 'value': round(v)} for r, v in by_region.items()],
        key=lambda x: x['value'], reverse=True
    )

    agency_data = [
        {'acr': a['acr'], 'name': a['name'], 'country': a['country'],
         'region': a['region'], 'budget': a['budget'], 'founded': a['founded']}
        for a in agencies
    ]

    # --- Geo data for the "Space Agencies" map tab ---
    from django.urls import reverse
    agencies_geo = []
    for a in AgencyProfile.objects.all():
        try:
            flag = a.flag.url
        except Exception:
            flag = ''
        agencies_geo.append({
            'name': a.agency_name, 'country': a.country_name,
            'lat': a.latitude, 'lng': a.longitude, 'flag': flag,
            'url': reverse('agency_detail', args=[a.pk]),
        })

    return render(request, 'home/dashboard.html', {
        'num_agencies': len(agencies),
        'total_budget_b': round(total_budget / 1000, 1),   # → billions
        'num_regions': len(regions),
        'regions': regions,
        'agency_data': agency_data,
        'region_data': region_data,
        'agencies_geo': agencies_geo,
    })


def agency_list(request):
    from .space_data import AGENCY_WEBSITES
    profiles = list(AgencyProfile.objects.all())
    for p in profiles:
        p.website = AGENCY_WEBSITES.get(p.country_name)
    return render(request, 'home/agency_list.html', {'profiles': profiles})

def agency_detail(request, pk):
    from .space_data import AGENCY_WEBSITES
    profile = get_object_or_404(AgencyProfile, pk=pk)
    profile.website = AGENCY_WEBSITES.get(profile.country_name)
    space_objects = SpaceObject.objects.filter(state_organization=profile.country_name)
    return render(request, 'home/agency_detail.html', {'profile': profile, 'space_objects': space_objects})

_AVATAR_COLORS = ['#E1912A', '#C15A3E', '#2F7E72', '#5B7CB8', '#8C6BB1', '#B04A6E', '#4F8F5C']


def _avatar(name):
    n = (name or 'Anon').strip() or 'Anon'
    return {'initial': n[0].upper(), 'color': _AVATAR_COLORS[sum(map(ord, n)) % len(_AVATAR_COLORS)]}


def _flair(subject):
    s = (subject or '').lower()
    if '?' in (subject or ''):
        return 'Question'
    if any(w in s for w in ['launch', 'lands', 'landing', 'reaches', 'orbit', 'rocket']):
        return 'Launch'
    if any(w in s for w in ['news', 'announce', 'budget', 'spending', 'deorbit']):
        return 'News'
    if any(w in s for w in ['best', 'resource', 'learn', 'how ', 'recommend']):
        return 'Resource'
    return 'Discussion'


def _score(disc, comments):
    return (disc.id * 41) % 380 + comments * 14 + 11


def forum_home(request):
    sort = request.GET.get('sort', 'hot')
    discussions = list(Discussion.objects.all())
    for d in discussions:
        d.comment_count = d.replies.count()
        d.score = _score(d, d.comment_count)
        d.flair = _flair(d.subject)
        d.avatar = _avatar(d.name)
    if sort == 'new':
        discussions.sort(key=lambda x: x.created_at, reverse=True)
    elif sort == 'top':
        discussions.sort(key=lambda x: x.score, reverse=True)
    else:  # 'hot' — blend score with recent engagement
        discussions.sort(key=lambda x: x.score + x.comment_count * 25, reverse=True)
    return render(request, 'home/forum_home.html', {'discussions': discussions, 'sort': sort})

def start_discussion(request):
    if request.method == 'POST':
        form = DiscussionForm(request.POST)
        if form.is_valid():
            discussion = form.save(commit=False)
            discussion.author = request.user if request.user.is_authenticated else None
            discussion.name = form.cleaned_data.get('name') or 'Anonymous'
            discussion.save()
            return redirect('forum_home')
    else:
        form = DiscussionForm()
    return render(request, 'home/start_discussion.html', {'form': form})

def create_discussion(request):
    if request.method == 'POST':
        form = DiscussionForm(request.POST)
        if form.is_valid():
            discussion = form.save(commit=False)
            discussion.author = request.user if request.user.is_authenticated else None
            discussion.name = form.cleaned_data.get('name') or 'Anonymous'
            discussion.save()
            return redirect('forum_home')
    else:
        form = DiscussionForm()
    return render(request, 'home/start_discussion.html', {'form': form})

def discussion_detail(request, discussion_id):
    discussion = get_object_or_404(Discussion, id=discussion_id)
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.discussion = discussion
            reply.author = request.user if request.user.is_authenticated else None
            reply.name = form.cleaned_data.get('name') or 'Anonymous'
            reply.save()
            return redirect('discussion_detail', discussion_id=discussion_id)
    else:
        form = ReplyForm()
    replies = list(discussion.replies.all().order_by('created_at'))
    discussion.avatar = _avatar(discussion.name)
    discussion.comment_count = len(replies)
    discussion.score = _score(discussion, discussion.comment_count)
    discussion.flair = _flair(discussion.subject)
    for r in replies:
        r.avatar = _avatar(r.name)
        r.rscore = (r.id * 17) % 90 + 3
    return render(request, 'home/discussion_detail.html', {
        'discussion': discussion, 'form': form, 'replies': replies,
    })

def map_view(request):
    agencies = AgencyProfile.objects.all()
    return render(request, 'home/map.html', {'agencies': agencies})

def _enrich_news(article):
    """Derive a byline (author) and a section 'kicker' from each article so
    the news page can be laid out like a real newsroom front."""
    import re
    from urllib.parse import urlparse

    summary = (article.summary or '').strip()
    author = re.split(r'\b(?:published|last updated|updated)\b', summary, maxsplit=1, flags=re.I)[0]
    author = author.strip(' -–·|')
    if not author or len(author) > 40:
        author = 'Space.com'

    parts = [p for p in urlparse(article.link or '').path.split('/') if p]
    if len(parts) >= 2:
        category = parts[0].replace('-', ' ').title()
    else:
        category = 'Space'
    if len(category) > 24:
        category = 'Space'

    palette = ['var(--accent)', 'var(--terra)', 'var(--teal)']
    color = palette[sum(ord(c) for c in category) % len(palette)]

    article.byline = author
    article.kicker = category
    article.kicker_color = color
    return article


def news_list(request):
    from django.utils import timezone
    # Live space news is fetched client-side from the Spaceflight News API so it
    # stays current without depending on the server's outbound network access.
    return render(request, 'home/news_list.html', {'today': timezone.localdate()})

def missions_list(request):
    missions = Mission.objects.all().order_by('-date')
    return render(request, 'home/missions_list.html', {'missions': missions})

def about(request):
    return render(request, 'home/about.html')


def google_site_verification(request):
    # Serves the Google Search Console HTML-file verification token.
    from django.http import HttpResponse
    return HttpResponse(
        "google-site-verification: google3a2842200f62ea11.html",
        content_type="text/html",
    )


def robots_txt(request):
    from django.http import HttpResponse
    sitemap = request.build_absolute_uri('/sitemap.xml')
    lines = ["User-agent: *", "Allow: /", "Disallow: /admin/", "", "Sitemap: " + sitemap]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def sitemap_xml(request):
    from django.http import HttpResponse
    from django.urls import reverse
    from django.utils import timezone

    static_pages = ['home', 'about', 'dashboard', 'agency_list', 'timeline_view',
                    'map_view', 'news_list', 'missions_list', 'forum_home']
    today = timezone.now().date().isoformat()

    urls = []
    for name in static_pages:
        priority = '1.0' if name == 'home' else '0.8'
        urls.append((request.build_absolute_uri(reverse(name)), priority, 'weekly'))
    for a in AgencyProfile.objects.all():
        urls.append((request.build_absolute_uri(reverse('agency_detail', args=[a.pk])), '0.7', 'monthly'))
    for d in Discussion.objects.all():
        urls.append((request.build_absolute_uri(reverse('discussion_detail', args=[d.id])), '0.5', 'weekly'))

    parts = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, priority, freq in urls:
        parts.append(
            f'<url><loc>{loc}</loc><lastmod>{today}</lastmod>'
            f'<changefreq>{freq}</changefreq><priority>{priority}</priority></url>'
        )
    parts.append('</urlset>')
    return HttpResponse("\n".join(parts), content_type="application/xml")


def timeline_view(request):
    from .space_data import TIMELINE_EVENTS
    events = sorted(TIMELINE_EVENTS, key=lambda e: e['year'])
    return render(request, 'home/timeline.html', {
        'events': events,
        'span_start': events[0]['year'] if events else '',
        'span_end': events[-1]['year'] if events else '',
    })
