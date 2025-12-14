import os
from reportlab.lib.pagesizes import landscape, A5
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

PDF_OUTPUT_DIR = "generated_tickets"
os.makedirs(PDF_OUTPUT_DIR, exist_ok=True)


def draw_header(c, width, height):
    """Yellow curved boarding-pass header area."""
    c.setFillColorRGB(1, 0.75, 0)  # yellow
    c.roundRect(0, height - 55, width, 55, 12, fill=1, stroke=0)

    c.setFont("Helvetica-Bold", 26)
    c.setFillColor(colors.white)
    c.drawString(20, height - 35, "BOARDING PASS")


def draw_stub_divider(c, width, height):
    """Dotted tear-line between main ticket and stub."""
    c.setStrokeColorRGB(0.8, 0.8, 0.8)
    c.setDash(4, 4)
    c.setLineWidth(1)
    c.line(width - 120, 0, width - 120, height)
    c.setDash()  # reset dash


def generate_ticket_pdf(booking, flight):
    filename = f"{booking.pnr}.pdf"
    filepath = os.path.join(PDF_OUTPUT_DIR, filename)

    c = canvas.Canvas(filepath, pagesize=landscape(A5))
    width, height = landscape(A5)

    # --------------------------------------------------------------------
    # HEADER
    # --------------------------------------------------------------------
    draw_header(c, width, height)

    # --------------------------------------------------------------------
    # MAIN TICKET SECTION
    # --------------------------------------------------------------------
    c.setFillColor(colors.black)

    # Passenger info
    c.setFont("Helvetica-Bold", 12)
    c.drawString(20, height - 90, "PASSENGER NAME:")
    c.setFont("Helvetica", 12)
    c.drawString(150, height - 90, booking.passenger_name)

    # PNR
    c.setFont("Helvetica-Bold", 12)
    c.drawString(20, height - 115, "PNR:")
    c.setFont("Helvetica", 12)
    c.drawString(150, height - 115, booking.pnr)

    # Booking Date
    c.setFont("Helvetica-Bold", 12)
    c.drawString(20, height - 140, "BOOKED ON:")
    c.setFont("Helvetica", 12)
    c.drawString(150, height - 140, str(booking.booking_time))

    # Flight Number
    c.setFont("Helvetica-Bold", 12)
    c.drawString(20, height - 165, "FLIGHT:")
    c.setFont("Helvetica", 12)
    c.drawString(150, height - 165, flight.flight_id)

    # Route - Big text (like sample boarding pass)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(20, height - 215, flight.departure_city.upper())
    c.setFont("Helvetica-Bold", 24)
    c.drawString(180, height - 215, "✈")
    c.drawString(220, height - 215, flight.arrival_city.upper())

    # Fare
    c.setFont("Helvetica-Bold", 12)
    c.drawString(20, height - 245, "FARE PAID:")
    c.setFont("Helvetica", 12)
    c.drawString(150, height - 245, f"₹{booking.final_price}")

    # --------------------------------------------------------------------
    # TEAR-OFF STUB (Right side)
    # --------------------------------------------------------------------
    draw_stub_divider(c, width, height)

    stub_x = width - 110

    c.setFont("Helvetica-Bold", 12)
    c.drawString(stub_x, height - 90, "PNR")
    c.setFont("Helvetica", 12)
    c.drawString(stub_x, height - 105, booking.pnr)

    c.setFont("Helvetica-Bold", 12)
    c.drawString(stub_x, height - 135, "FLIGHT")
    c.setFont("Helvetica", 12)
    c.drawString(stub_x, height - 150, flight.flight_id)

    c.setFont("Helvetica-Bold", 12)
    c.drawString(stub_x, height - 180, "FROM")
    c.setFont("Helvetica", 12)
    c.drawString(stub_x, height - 195, flight.departure_city)

    c.setFont("Helvetica-Bold", 12)
    c.drawString(stub_x, height - 225, "TO")
    c.setFont("Helvetica", 12)
    c.drawString(stub_x, height - 240, flight.arrival_city)

    # --------------------------------------------------------------------
    # FOOTER
    # --------------------------------------------------------------------
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(20, 20, "Thank you for choosing FlightEasy. Have a pleasant journey!")

    c.save()
    return filepath
