# report/admin.py
from .models import Report
# admin.py
from django.contrib import admin
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from django.http import HttpResponse
from reportlab.lib.styles import getSampleStyleSheet

from .models import Report

def download_report_pdf(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reports.pdf"'

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    styles = getSampleStyleSheet()
    title = Paragraph("Clinic Report", styles['Title'])
    elements.append(title)

    data = [[
        "Date Generated",
        "Dentist",
        "Patient",
        "Treatment",
        "Description",
    ]]
    data.extend([
        [report.date_generated, report.dentist, report.patient, report.service, report.description]
        for report in queryset
    ])

    table_style = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.gray),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]

    table = Table(data, style=table_style)


    elements.append(table)

    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

download_report_pdf.short_description = "Download selected reports as PDF"

class ReportAdmin(admin.ModelAdmin):
    list_display = ('dentist', 'date_generated', 'description')
    actions = [download_report_pdf]

admin.site.register(Report, ReportAdmin)
