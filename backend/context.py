from account.models import User
from frontend.models import Tags, Category, About, News, Privacy, Services, Blog, Testimonial, Details, Advert, Career, Contact, Faq, Header, Footer, ServiceHeader, FAQHeader, TestimonialHeader, AboutHeader, CareerHeader, ContactHeader, Steps
from applications.models import Loan, Investment
from newsletter.models import Mails, Subscriber

def processors(request):
   total_users                   = User.objects.all().exclude(is_active=False).exclude(is_superuser=True).count()
   total_superusers              = User.objects.filter(is_superuser=True, is_staff=True, is_active=True).count()
   total_staff                   = User.objects.filter(is_staff=True, is_active=True).exclude(is_superuser=True).count()
   total_staffs                  = User.objects.filter(is_superuser=True, is_staff=True, is_active=True).count()
   total_regular                 = User.objects.filter(is_active=True).exclude(is_superuser=True).exclude(is_staff=True).count()
   total_ban                     = User.objects.filter(is_active=False).count()
    
   loan                          = Loan.objects.all()
   total_loan                    = Loan.objects.all().count()
   total_loan_pending            = Loan.objects.filter(status=0).count()
   total_loan_approved           = Loan.objects.filter(status=1).count()
   total_loan_disapproved        = Loan.objects.filter(status=2).count()
   
   investment                    = Investment.objects.all()
   total_investment              = Investment.objects.all().count()
   total_investment_pending      = Investment.objects.filter(status=0).count()
   total_investment_approved     = Investment.objects.filter(status=1).count()
   total_investment_disapproved  = Investment.objects.filter(status=2).count()
   
   total_contact                 = Contact.objects.all().count()
   total_subscriber              = Subscriber.objects.all().count()
   
   tags                          = Tags.objects.all()
   category                      = Category.objects.all()
   service                       = Services.objects.all()
   testimonials                  = Testimonial.objects.all()
   detail                        = Details.objects.all()
   advert                        = Advert.objects.all()
   about                         = About.objects.all()
   
   careers                       = Career.objects.all()
   news                          = News.objects.all().order_by('-date_created')
   faq                           = Faq.objects.all()
   privacy                       = Privacy.objects.all()
   header                        = Header.objects.all()
   footer                        = Footer.objects.all()
   
   total_blog                    = Blog.objects.all().count()
   blog_pending                  = Blog.objects.filter(status=0).count()
   blog_approved                 = Blog.objects.filter(status=1).count()
   blog_disapproved              = Blog.objects.filter(status=2).count()
   
   service_header                = ServiceHeader.objects.all()
   faq_header                    = FAQHeader.objects.all()
   testimonial_header            = TestimonialHeader.objects.all()
   about_header                  = AboutHeader.objects.all()
   career_header                 = CareerHeader.objects.all()
   contact_header                = ContactHeader.objects.all()
   steps                         = Steps.objects.all()
   
    
   context = {
      'total_superusers': total_superusers, 'total_users':total_users, 'total_staff':total_staff, 'total_regular':total_regular, 'loan':loan, 'news':news,
      'total_ban':total_ban, 'tags':tags, 'category':category, 'service':service, 'testimonials':testimonials, 'investment':investment, 'steps': steps,
      'detail':detail, 'advert':advert, 'careers':careers, 'total_loan':total_loan, 'total_contact':total_contact, 'service_header': service_header,
      'total_loan_pending':total_loan_pending, 'total_loan_approved': total_loan_approved, 'total_loan_disapproved':total_loan_disapproved, 'about': about,
      'total_investment':total_investment, 'total_investment_pending':total_investment_pending, 'total_investment_approved':total_investment_approved,
      'total_investment_disapproved':total_investment_disapproved, 'total_blog':total_blog, 'blog_pending':blog_pending, 'blog_approved':blog_approved,
      'blog_disapproved':blog_disapproved, 'faq':faq, 'header':header, 'footer':footer, 'faq_header':faq_header, 'testimonial_header': testimonial_header,
      'about_header':about_header, 'career_header':career_header, 'contact_header': contact_header, 'total_subscriber':total_subscriber, 'total_staffs':total_staffs,
      'privacy':privacy
      
      }
   return context