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



def home_page(request):
    # Space Objects Data
    space_data = SpaceObject.objects.values('state_organization').annotate(Objects_Launched=Count('id')).order_by('state_organization')
    space_df = pd.DataFrame(list(space_data))
    graphic_space_objects = create_graph(space_df, 'Number of Objects Launched into Space by Country', 'Country', 'Number of Objects Launched', None)

    # Government Spending Data
    gov_spending_data = AgencyProfile.objects.exclude(annual_government_spending__isnull=True).values('country_name', 'annual_government_spending').order_by('country_name')
    gov_spending_df = pd.DataFrame(list(gov_spending_data))

    # Define a custom formatter function for the y-axis
    def currency(x, pos):
        return f'${x:,.0f}'

    yformat = FuncFormatter(currency)

    graphic_gov_spending = create_graph(gov_spending_df, 'Government Spending on Space Programs', 'Country', 'Spending Amount (USD)', yformat)

    # Data for the redesigned homepage (nations rail + stat strip)
    agencies = AgencyProfile.objects.all().order_by('country_name')
    num_agencies = agencies.count()
    num_objects = SpaceObject.objects.count()

    return render(request, 'home/home_page.html', {
        'graphic_space_objects': graphic_space_objects,
        'graphic_gov_spending': graphic_gov_spending,
        'agencies': agencies,
        'num_agencies': num_agencies,
        'num_objects': num_objects,
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
