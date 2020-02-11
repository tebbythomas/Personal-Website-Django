from django.shortcuts import render
from django.http import HttpResponse
from personal_details.models import PersonalDetails
from certifications.models import Certificate
from portfolio.models import Portfolio
from work_ex.models import WorkEx



# Create your views here.

def index(request):
    # Get portfolio
    portfolio = Portfolio.objects.all()
    # Get certificates
    certificates = Certificate.objects.all()
    # Get personal details obj
    personal_detail = PersonalDetails.objects.first()
    # Get work experience obj
    work_ex = WorkEx.objects.all().order_by('-start_date')
    
    context = {
        'projects': portfolio,
        'certificates': certificates,
        'personal_detail': personal_detail,
        'jobs': work_ex
    }
    return render(request, 'pages/index.html', context)
