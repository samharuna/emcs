from django.shortcuts import get_object_or_404
from frontend.models import HeaderLogo, FooterLogo, Loan, Investment, Post, Tags, Category, Comment, Reply, About, Title, Occupation, Service, Purpose, Statement, Team, Testimony, Newsletter, Mail, Career, Advert, Contact, ContactDetail, Faq, Event, Gallery
from accounts.models import User
import datetime

def processors(request):
# START OF BACKEND
   total_loan                    = Loan.objects.all().count()
   total_loan_pending            = Loan.objects.filter(status=0).count()
   total_loan_approved           = Loan.objects.filter(status=1).count()
   total_loan_disapproved        = Loan.objects.filter(status=2).count()

   total_investment              = Investment.objects.all().count()
   total_investment_pending      = Investment.objects.filter(status=0).count()
   total_investment_approved     = Investment.objects.filter(status=1).count()
   total_investment_disapproved  = Investment.objects.filter(status=2).count()
   
   tags                          = Tags.objects.all()
   category                      = Category.objects.all()

   total_tags                    = Tags.objects.all().count()
   total_categories              = Category.objects.all().count()

   total_users                   = User.objects.all().count()
   total_superusers              = User.objects.filter(is_superuser=True).count()
   total_staffusers              = User.objects.filter(is_staff=True).exclude(is_superuser=True, is_active=True).count()
   total_activeusers             = User.objects.filter(is_active=True).exclude(is_superuser=True).exclude(is_staff=True).count()
   total_bannedusers             = User.objects.filter(is_active=False).count()

   post_total                    = Post.objects.all().count()
   post_pending                  = Post.objects.filter(status=0).count()
   post_approve                  = Post.objects.filter(status=1).count()
   post_disapprove               = Post.objects.filter(status=2).count()

   total_subscriber              = Newsletter.objects.all().count()
   total_title                   = Title.objects.all().count()
   total_service                 = Service.objects.all().count()
   total_occupation              = Occupation.objects.all().count()
   total_team                    = Team.objects.all().count()
   total_advert                  = Advert.objects.all().count()
   total_testifer                = Testimony.objects.all().count()
   total_purpose                 = Purpose.objects.all().count()
   total_statement               = Statement.objects.all().count()
   total_contact                 = Contact.objects.all().count()
   total_mail                    = Mail.objects.all().count()
   total_career                  = Career.objects.all().count()
   total_comment                 = Comment.objects.all().count()
   total_reply                   = Reply.objects.all().count()
# END OF BACKEND

# START OF FRONTEND
   week_ago                      = datetime.date.today() - datetime.timedelta(days=14)
   trending                      = Post.objects.filter(date_created__gte = week_ago).order_by('-view_count')

   current_datetime              = datetime.datetime.now()
   
   team                          = Team.objects.all().order_by("team")
   testimony                     = Testimony.objects.all().order_by("-id")
   service                       = Service.objects.all()
   faq                           = Faq.objects.all()

   gallery                       = Gallery.objects.all().order_by("title")
   event                         = Event.objects.all().order_by("name")

   latest                        = Post.objects.filter(status=1).order_by('-id')[0:5]
   recently_view                 = Post.objects.filter(status=1).order_by('-last_view')[0:5]

   title                         = Title.objects.all()
   
   advert                        = Advert.objects.all().order_by('id')[:1]
   advert1                       = Advert.objects.all().order_by('-id')[1:2]
   
   
   detail                        = ContactDetail.objects.all()
   statement                     = Statement.objects.all()
   about                         = About.objects.all()
   header                        = HeaderLogo.objects.all()
   footer                        = FooterLogo.objects.all()
# END OF FRONTEND

   context = {
      'total_users':total_users, 'total_superusers':total_superusers, 'total_staffusers':total_staffusers, 'total_activeusers':total_activeusers, 'total_bannedusers':total_bannedusers, 'total_comment':total_comment,
      'total_tags':total_tags, 'total_categories':total_categories, 'post_total':post_total, 'post_approve':post_approve, 'post_disapprove':post_disapprove, 'post_pending':post_pending, 'total_reply':total_reply,
      'tags':tags, 'category': category, 'total_loan':total_loan, 'total_loan_pending':total_loan_pending, 'total_loan_approved': total_loan_approved, 'total_statement':total_statement, 'total_contact':total_contact,
      'total_loan_disapproved':total_loan_disapproved, 'total_investment':total_investment, 'total_investment_pending':total_investment_pending, 'total_investment_approved':total_investment_approved, 'faq': faq,
      'total_investment_disapproved':total_investment_disapproved, 'statement':statement, 'team':team, 'detail':detail, 'testimony':testimony, 'latest':latest, 'advert':advert, 'total_career': total_career,
      'total_mail':total_mail, 'total_subscriber':total_subscriber, 'total_title':total_title, 'total_service':total_service, 'total_occupation':total_occupation, 'total_team':total_team, 'total_advert':total_advert,
      'total_testifer':total_testifer, 'total_purpose':total_purpose, 'recently_view': recently_view, 'trending':trending, 'title':title, 'service':service, 'gallery':gallery, 'about':about, 'event':event,
      'header': header, 'footer': footer, 'current_datetime':current_datetime, 'advert1':advert1
   }
   return context