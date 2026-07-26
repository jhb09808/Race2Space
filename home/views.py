from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from .models import AgencyProfile, Discussion, NewsArticle, Mission, TimelineEvent, SpaceObject
from .forms import DiscussionForm, ReplyForm
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import pandas as pd  # Ensure this import is included
from matplotlib.ticker import FuncFormatter

def create_graph(data, title, xlabel, ylabel, yformat):
    buffer = io.BytesIO()
    plt.figure(figsize=(12, 8))  # Increase figure size for better spacing
    sns.barplot(x=data.columns[0], y=data.columns[1], data=data, palette='coolwarm')
    plt.xticks(rotation=45, ha='right', fontsize=8)  # Rotate and adjust x-axis labels
    plt.xlabel(xlabel)
    plt.ylabel(ylabel, labelpad=40)  # Further increase padding for the y-axis label
    plt.title(title)
    plt.tight_layout(rect=[0.1, 0.1, 0.95, 0.95])  # Adjust layout to prevent clipping

    # Apply y-axis formatter if specified
    if yformat:
        plt.gca().yaxis.set_major_formatter(yformat)

    # Save the plot to a buffer
    plt.savefig(buffer, format='png', bbox_inches='tight')  # Use tight bounding box to include all elements
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    return base64.b64encode(image_png).decode('utf-8')



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

def agency_list(request):
    profiles = AgencyProfile.objects.all()
    return render(request, 'home/agency_list.html', {'profiles': profiles})

def agency_detail(request, pk):
    profile = get_object_or_404(AgencyProfile, pk=pk)
    space_objects = SpaceObject.objects.filter(state_organization=profile.country_name)
    return render(request, 'home/agency_detail.html', {'profile': profile, 'space_objects': space_objects})

def forum_home(request):
    discussions = Discussion.objects.all()
    return render(request, 'home/forum_home.html', {'discussions': discussions})

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
    return render(request, 'home/discussion_detail.html', {'discussion': discussion, 'form': form})

def map_view(request):
    agencies = AgencyProfile.objects.all()
    return render(request, 'home/map.html', {'agencies': agencies})

def news_list(request):
    news_articles = NewsArticle.objects.all().order_by('-published_date')
    return render(request, 'home/news_list.html', {'news_articles': news_articles})

def missions_list(request):
    missions = Mission.objects.all().order_by('-date')
    return render(request, 'home/missions_list.html', {'missions': missions})

def timeline_view(request):
    events = TimelineEvent.objects.all().order_by('date')
    return render(request, 'home/timeline.html', {'events': events})
