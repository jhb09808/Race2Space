from django.db import migrations
from django.utils import timezone
from datetime import timedelta


# subject, author, message, hours-ago, [ (author, message, hours-ago), ... ]
DISCUSSIONS = [
    ("Chandrayaan-3 landing near the south pole — still can't believe India pulled it off",
     "Ananya", "Fourth country ever to soft-land on the Moon, and the FIRST anywhere near the south pole. On a budget smaller than some space movies. What a moment for ISRO.", 5,
     [("Diego", "The cost-efficiency is the part that blows my mind. Proof you don't need a NASA-sized budget to do frontier science.", 4),
      ("Kwame", "Genuinely inspiring for every emerging program watching. If India can do it, the door is open.", 3),
      ("Priya", "Was refreshing the livestream with my whole family. Cried a little not gonna lie 🚀", 2)]),

    ("Why do so many launch sites cluster near the equator?",
     "Mateo", "Noticed Brazil's Alcântara, Kenya's old San Marco platform, French Guiana... is it just the extra rotational speed boost or is there more to it?", 20,
     [("ChenWei", "Mostly the rotational velocity — you get a free ~460 m/s near the equator vs almost nothing at the poles. Cheaper to reach orbit.", 19),
      ("Leila", "Also easier access to a range of orbital inclinations without costly plane changes. Equatorial sites are geographically lucky.", 17),
      ("Mateo", "That makes Alcântara sound like a seriously underrated asset then.", 15)]),

    ("Kenya's Taifa-1 — what's next for African space programs?",
     "Ngozi", "First fully Kenyan-designed satellite is up and running. Between SANSA, EgSA, and now KENSA, Africa's momentum feels real. Who's next to reach a big milestone?", 30,
     [("Thabo", "Nigeria and South Africa have been quietly building capacity for years. Watch that space.", 28),
      ("Fatima", "Egypt's new agency HQ in the capital is no joke either. Serious long-term intent.", 25)]),

    ("Is the UAE's Hope Mars mission underrated?",
     "Zaid", "First Arab interplanetary mission, reached Mars on the first attempt, and it's delivering genuinely useful atmospheric science. Feels like it doesn't get enough credit.", 44,
     [("Sofia", "Completely agree. And they trained a whole new generation of engineers doing it — that's the real long-term payoff.", 42),
      ("Arjun", "Reaching Mars on a maiden attempt is absurdly hard. India and the UAE both did it. Wild decade for newcomers.", 40)]),

    ("Best free resources to actually learn orbital mechanics?",
     "Rafael", "Tired of hand-wavy explanations. Looking for something rigorous but approachable. Textbooks, courses, YouTube channels — hit me.", 52,
     [("Camila", "Curtis's 'Orbital Mechanics for Engineering Students' is the classic. Pair it with the KSP mod Principia if you want intuition.", 50),
      ("Yusuf", "MIT OCW 16.07 Dynamics is free and excellent. Also Scott Manley on YouTube for intuition first.", 48),
      ("Rafael", "Principia + Curtis is a great combo, thanks. Adding both.", 47)]),

    ("Azerbaijan and Indonesia both spend ~$220M — where does that money actually go?",
     "Lucia", "Two very different countries landing at almost the same budget. Satellites? Ground infrastructure? Salaries? Curious how the priorities differ.", 66,
     [("ChenWei", "For a lot of mid-size programs it's mostly comms satellites + the ground segment. The launch itself is often outsourced.", 64),
      ("Kofi", "Indonesia has the archipelago connectivity problem to solve, so satellite internet eats a big chunk. Different driver than Azerbaijan.", 61)]),

    ("Prediction: which developing nation reaches orbit on its own rocket next?",
     "Diego", "Right now the indigenous-launch club is small. Who breaks in next — and roughly when?", 80,
     [("Priya", "Brazil if Alcântara commercial partnerships take off. The site advantage is just too good to waste.", 78),
      ("Zaid", "South Korea already did it with Nuri, arguably crossing over from 'developing'. Next genuinely emerging one... I'd watch Brazil too.", 76),
      ("Amara", "Don't sleep on the long game from a couple of African programs. 10-year horizon though.", 73)]),

    ("The ISS is deorbiting around 2031 — what replaces it for smaller nations?",
     "Fatima", "So much emerging-nation science flew as ISS payloads or CubeSat deployments from it. When it's gone, what fills that gap for programs without their own station?", 96,
     [("Sofia", "Commercial stations (Axiom, Orbital Reef) are pitching exactly this — buy time instead of building a station.", 94),
      ("Kwame", "China's Tiangong is also open to international experiments. Could become a real option for the Global South.", 90)]),

    ("Ground stations across Africa — cooperation or competition?",
     "Thabo", "Multiple countries building tracking and receiving stations. Would a shared continental network be smarter than everyone going solo?", 120,
     [("Ngozi", "A shared network would be far more cost-effective, but sovereignty concerns always complicate the politics.", 117),
      ("Lucia", "The EU's approach to shared infrastructure via ESA is a decent template. Hard to copy the trust though.", 112)]),

    ("Unpopular opinion: small satellites matter more than crewed missions for developing nations",
     "Kofi", "Crewed flights grab headlines, but a $10M Earth-observation sat that improves crop yields or flood warnings changes more lives. Fight me.", 168,
     [("Camila", "Not even unpopular imo. Practical space > prestige space for most emerging programs.", 165),
      ("Mateo", "Both matter — prestige missions build the talent pipeline that later builds the useful sats. It's a flywheel.", 160),
      ("Yusuf", "The CubeSat revolution is exactly why so many new nations could enter at all. Cheap access changed everything.", 155)]),
]


def seed_forum(apps, schema_editor):
    Discussion = apps.get_model('home', 'Discussion')
    Reply = apps.get_model('home', 'Reply')

    # Clear the old placeholder threads
    Reply.objects.all().delete()
    Discussion.objects.all().delete()

    now = timezone.now()
    for subject, author, message, hours, replies in DISCUSSIONS:
        disc = Discussion.objects.create(subject=subject, name=author, message=message)
        # created_at is auto_now_add; override with a realistic past time
        Discussion.objects.filter(pk=disc.pk).update(created_at=now - timedelta(hours=hours))
        for r_author, r_message, r_hours in replies:
            rep = Reply.objects.create(discussion=disc, name=r_author, message=r_message)
            Reply.objects.filter(pk=rep.pk).update(created_at=now - timedelta(hours=r_hours))


def unseed_forum(apps, schema_editor):
    # Non-destructive reverse: leave data as-is.
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_delete_governmentspending_and_more'),
    ]

    operations = [
        migrations.RunPython(seed_forum, unseed_forum),
    ]
