from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import datetime
import logs_analysis

def export_logs_to_pdf():
    filename = f"logs_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    text = c.beginText(40, height - 50)
    text.setFont("Courier", 9)

    # Gather logs
    log_sections = {
        "🔌 USB Logs": logs_analysis.get_usb_logs(),
        "🔐 Security Logs": logs_analysis.get_security_logs(),
        "⚙️ System Logs": logs_analysis.get_system_logs(),
        "🧠 Application Logs": logs_analysis.get_application_logs(),
        "🌐 DNS Logs": logs_analysis.get_dns_logs()
    }

    for title, content in log_sections.items():
        text.textLine(title)
        for line in content.splitlines():
            text.textLine(line)
        text.textLine("-" * 80)

        # New page if too long
        if text.getY() < 80:
            c.drawText(text)
            c.showPage()
            text = c.beginText(40, height - 50)
            text.setFont("Courier", 9)

    c.drawText(text)
    c.save()
    return filename
