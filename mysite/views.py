from django.contrib.auth.models import User, auth
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from service.models import service
from Gallery.models import gallery
from django.contrib.auth.decorators import login_required
from .forms import AppointmentForm
from django.http import HttpResponse,HttpResponseRedirect
from Appointment.models import Appointment
from django.http import JsonResponse
from Appointment.models import Slot
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction, IntegrityError
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from Appointment.models import UserProfile
from django.template.loader import get_template
from xhtml2pdf import pisa
from report.forms import ReportForm
from report.models import Report ,PatientReport
from patient.models import Patient
from django.shortcuts import get_object_or_404
from report.models import Report
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import io
from io import BytesIO

def report_detail_view(request, report_id):
    try:
        # Retrieve the report instance
        report_instance = Report.objects.get(id=report_id)
        
        # Access the patient's email from the report instance
        patient_email = report_instance.patient.email
        
        # Pass the report instance and patient's email to the template
        return render(request, 'report_detail.html', {'report': report_instance, 'patient_email': patient_email})
    except Report.DoesNotExist:
        # Handle the case where the report does not exist
        return render(request, 'report_not_found.html')


def download_report(request, report_id):
    # Retrieve the report object
    report = get_object_or_404(Report, pk=report_id)
    
    # Create the HttpResponse object with the appropriate PDF headers
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="report_{report.id}.pdf"'

    # Create a canvas for PDF generation
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()
    title = Paragraph("Clinic Report", styles['Title'])
    elements.append(title)

    # Populate data for the PDF table with the report details
    data = [
        ["Date Generated", report.date_generated],
        ["Dentist", report.dentist],
        ["Patient", report.patient],
        ["Treatment", report.service],
        ["Description", report.description],
    ]

    # Define styles for the PDF table
    table_style = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]

    # Create the PDF table
    table = Table(data, style=table_style)

    # Add the table to the elements list
    elements.append(table)

    # Build the PDF document
    doc.build(elements)

    # Get the PDF content from the buffer and write it to the response
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response



def generate_report_pdf(request):
    # Fetch data from the database
    report_data = Report.objects.all()

    # Render the template with data
    template = get_template('report_template.html')
    context = {'report_data': report_data}
    html = template.render(context)

    # Create PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Failed to generate PDF', status=500)
    return response

def generate_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('generate_report_pdf')
    else:
        form = ReportForm()
    return render(request, 'generate_report.html', {'form': form})




def send_email(request):
    # Example usage of send_mail
    subject = 'Test Email'
    message = 'This is a test email sent from Django.'
    from_email = 'ommalaviya25@gmail.com'  # Sender's email address
    recipient_list = ['omalviya111@gmail.com']  # List of recipient email addresses

    send_mail(subject, message, from_email, recipient_list)

    return HttpResponse('Email sent successfully!')


def get_available_slots(request):
    date = request.GET.get('date')
    if date:
        slots = Slot.objects.filter(date=date, booked=False)
        slot_data = [{'hour': slot.hour, 'minute': slot.minute , 'am_pm': slot.am_pm} for slot in slots]
        return JsonResponse({'slots': slot_data})
    else:
        return JsonResponse({'error': 'Date parameter is missing'})


# def get_available_slots(request):
#     date = request.GET.get('date')
#     if date:
#         slots = Slot.objects.filter(date=date)
#         slot_data = [{'start_time': slot.start_time} for slot in slots]
#         return JsonResponse({'slots': slot_data})
#     else:
#         return JsonResponse({'error': 'Date parameter is missing'})

# @login_required
# def profile(request):
#     return render(request, 'profile.html')


def homepage(request):
    

    servicesdata=service.objects.all

    data={
        'servicesdata':servicesdata
    }

    return render(request, "index.html",data)

# @login_required
# def appointment(request):
#     # Your view logic here
#     return render(request, 'appointment')


def view_appointments(request):
    if request.user.is_authenticated:
        user_appointments = Appointment.objects.filter(patient=request.user)
        return render(request, 'view_appointments.html', {'user_appointments': user_appointments})
    else:
        # Handle the case when the user is not authenticated
        return redirect('login')
    

def profile(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Retrieve user's appointments excluding cancelled appointments
        user_appointments = Appointment.objects.filter(patient=request.user).exclude(status='Cancelled')

        # Determine if any appointments have been cancelled
        appointment_cancelled = Appointment.objects.filter(patient=request.user, status='Cancelled').exists()
        
        # Fetch patient instance associated with the logged-in user using email
          # Retrieve the email of the logged-in user
        user_email = request.user.email

        # Retrieve the reports associated with the logged-in user's email
        patient_reports = Report.objects.filter(patient__email=user_email)

        user_data = User.objects.get(pk=request.user.pk)
        
        # Render the profile template with the appropriate context
        return render(request, 'profile.html', {
            'user_appointments': user_appointments,
            'appointment_cancelled': appointment_cancelled,
            'user_data': user_data,
            'patient_reports': patient_reports  # Include patient reports in the context
        })
    else:
        # If the user is not authenticated, redirect to the login page
        return redirect('login')

def parse_selected_time(selected_time):
    # Split the selected time string by space to separate hour-minute and am/pm
    time_parts = selected_time.split(' ')
    
    # Extract hour and minute from the first part (e.g., '3:10')
    hour, minute = map(int, time_parts[0].split(':'))
    
    # Extract am/pm from the second part (e.g., 'PM')
    am_pm = time_parts[1]
    
    return hour, minute, am_pm



def delete_user(request, user_id):
    user_to_delete = get_object_or_404(User, pk=user_id)

    try:
        with transaction.atomic():
            # Delete associated records in UserProfile
            UserProfile.objects.filter(user=user_to_delete).delete()

            # Now you can safely delete the user
            user_to_delete.delete()
    except IntegrityError:
        # Handle IntegrityError if necessary
        pass

    
def appointment(request):
    print("View function is executed")
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        # Redirect to the login page if the user is not authenticated
        return redirect('login')

    # Process the appointment booking form
    if request.method == 'POST':
        # Create an instance of the AppointmentForm with the POST data
        form = AppointmentForm(request.POST)
        # Check if the form is valid
        if form.is_valid():
            appointment = form.save(commit=False)
            selected_time = request.POST.get('time')
            hour, minute, am_pm = parse_selected_time(selected_time)
            try:
                slot = Slot.objects.get(hour=hour, minute=minute, am_pm=am_pm)
            except Slot.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Selected slot does not exist'})
            
            if not slot.booked:
                slot.booked = True
                slot.save()
                appointment.patient = request.user
                appointment.save()
                messages.success(request, 'Appointment booked successfully!')
                return redirect('homepage')  # Redirect to homepage     
            else:
                return JsonResponse({'success': False, 'error': 'Slot already booked.'})
        else:
            print(form.errors)
            # Return error response with form errors
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        # If request method is not POST, create a new instance of the form
        form = AppointmentForm()
    
    # Render the appointment.html template with the form
    return render(request, 'appointment.html', {'form': form })


# def appointment(request):
#     print("View function is executed")
#     # Check if the user is authenticated
#     if not request.user.is_authenticated:
#         # Redirect to the login page if the user is not authenticated
#         return redirect('login')

#     # Process the appointment booking form
#     if request.method == 'POST':
#         # Create an instance of the AppointmentForm with the POST data
#         form = AppointmentForm(request.POST)
#         # Check if the form is valid
#         if form.is_valid():
#             appointment = form.save(commit=False)
#             slot_id = form.cleaned_data['time']
#             slot = Slot.objects.get(pk=slot_id)
#             if not slot.booked:
#                 slot.booked = True
#                 slot.save()
#                 appointment.patient = request.user
#                 appointment.save()
#                 return JsonResponse({'success': True, 'message': 'Appointment booked successfully!'})
#             else:
#                 return JsonResponse({'success': False, 'error': 'Slot already booked.'})
#         else:
#             print(form.errors)
#             # Return error response with form errors
#             return JsonResponse({'success': False, 'errors': form.errors})
#     else:
#         # If request method is not POST or not AJAX, create a new instance of the form
#         form = AppointmentForm()
    
#     # Render the appointment.html template with the form
#     return render(request, 'appointment.html', {'form': form })



def convert_to_24_hour_format(time_str):
    # Implement the logic to convert AM/PM time format to 24-hour format
    # Example implementation:
    # Split the time string into hours, minutes, and AM/PM
    time_parts = time_str.split(' ')
    hours, minutes = map(int, time_parts[0].split(':'))
    am_pm = time_parts[1].upper()

    # Adjust hours for PM
    if am_pm == 'PM' and hours < 12:
        hours += 12

    # Adjust hours for AM if it's 12:00 AM
    if am_pm == 'AM' and hours == 12:
        hours = 0

    # Return the time in 24-hour format
    return '{:02d}:{:02d}'.format(hours, minutes)

# this is main function

# def appointment(request):
#     print("View function is executed")
#     # Check if the user is authenticated
#     if not request.user.is_authenticated:
#         # Redirect to the login page if the user is not authenticated
#         return redirect('login')
#         # Define available time slots
    

#     # Process the appointment booking form
#     if request.method == 'POST':
#         print("Form data:", request.POST)
#         # Create an instance of the AppointmentForm with the POST data
#         form = AppointmentForm(request.POST)
#         # Check if the form is valid
#         if form.is_valid():
#             print("Time value received:", form.cleaned_data['time'])
#             # time_value = form.cleaned_data['time']
#             # Save the appointment to the database
#             appointment_instance = form.save(commit=False)
#             appointment_instance.patient = request.user  # Set the patient to the current user
#             appointment_instance.save()
#             # Display success message
#             messages.success(request, 'Appointment booked successfully!')
#             # Redirect to the profile page
#             return redirect('homepage')
#         else:
#             print("Form errors:", form.errors)




    
# def appointment(request):
#     return render(request, "Appointment.html")

# def loginpage(request):
#     return render(request, "login.html")

def serviceDetails(request,serviceid):
    
    serviceDetails=service.objects.get(id=serviceid)
    data={
           'serviceDetails':serviceDetails
    }
    return render(request, "servicedetails.html",data)

def services(request):
    serviceDetail=service.objects.all()
    data={
           'serviceDetail':serviceDetail
    }
    return render(request, "service.html",data)

def Gallery(request):
    gallerydata=gallery.objects.all

    data={
        'gallerydata':gallerydata
    }

    return render(request, "gallery.html",data)

def aboutus(request):
    
    return render(request, "aboutus.html")
def signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('signup')

        # Check if email is already in use
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already in use")
            return redirect('signup')

        try:
            user = User.objects.create_user(username=email, email=email, password=password1,first_name=first_name ,last_name=last_name,)
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect('homepage')
        except Exception as e:
            messages.error(request, f"Error creating account: {e}")
            return redirect('signup')

    return render(request, 'signup.html')


# def login_view(request):
#       if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         try:
#              user=customer.objects.get(email=email)
#              if user:
#                  if user.password==password:
#                      request.session['customer_id']=user.id
#                      request.session['fullname']=user.fullname
#                      request.session['email']=user.email
#                      messages.success(request, "Login Successfully.")
#                      return render(request , "index.html" , {'user':user})
#                  else:
#                      messages.error(request,"invalid password")
#                      return redirect('login')
#         except ObjectDoesNotExist:
#            messages.error(request,"user not found")
#            return redirect('login')

                    


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        print("user=",user)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('homepage')
        else:
            messages.error(request, "Invalid email or password.")

    return render(request, 'login.html')

def loginpage(request):
    return render(request,'login.html')

def logout_view(request):
    logout(request)
    return redirect('homepage')

def logout_view_a(request):
    logout(request)
    return redirect('admin')

# views.py

from django.contrib.auth import logout
from django.shortcuts import redirect

def admin_logout(request):
    # Log out the user
    logout(request)
    # Redirect to a page after logout, for example, the admin login page
    return redirect('admin')  # Replace 'admin_login_page' with the URL name of your admin login page
