import datetime
import io
import os

from django.shortcuts import render, redirect, get_object_or_404
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_JUSTIFY
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm, inch, mm
from reportlab.lib.utils import ImageReader

from AppVg import settings
from AppVg.settings import MEDIA_BASE_DIR
from backoffice.models.client import Client
from backoffice.models.pool import Pool
from backoffice.models.quotation import Quotation
from io import BytesIO
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, A4, portrait
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, Image, SimpleDocTemplate, Paragraph
from PIL import Image

from backoffice.forms import QuotationForm


def quotations(request):
    quotationsList = Quotation.objects.all()
    context = {
        'quotations': quotationsList,
    }
    return render(request, 'quotation/quotations.html', context)


def new_quotation(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    form = QuotationForm(client=client)

    if request.method == 'POST':
        form = QuotationForm(request.POST, request.FILES, client=client)
        if form.is_valid():
            form.save()
            return redirect('quotations')

    addresses = client.address_set.all()
    pools = Pool.objects.filter(address__in=addresses)
    return render(request, 'quotation/new_quotation.html', {'form': form, 'client': client})


def edit_quotation(request, quotation_id):
    quotation = get_object_or_404(Quotation, id=quotation_id)
    client = quotation.client

    if request.method == 'POST':
        form = QuotationForm(request.POST, instance=quotation, client=client, quotation=quotation)
        if form.is_valid():
            form.save()
            return redirect('quotation_details', quotation_id=quotation_id)
    else:
        form = QuotationForm(instance=quotation, client=client, quotation=quotation)
    return render(request, 'quotation/edit_quotation.html', {'form': form})


def quotation_details(request, quotation_id):
    quotation = get_object_or_404(Quotation, id=quotation_id)
    context = {
        'quotation': quotation,
    }
    return render(request, 'quotation/quotation_details.html', context)


def quotation_delete(request, quotation_id):
    quotation = get_object_or_404(Quotation, id=quotation_id)
    quotation.delete()
    return redirect('quotations')


def print_quotation(request, quotation_id):
    quotation = Quotation.objects.get(id=quotation_id)

    # create a buffer to store PDF
    buffer = BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont("Helvetica", 12)

    # --------------------- HEADER ---------------------------
    p.setFontSize(11)
    p.setFillColorRGB(0.7, 0.7, 0.7)
    p.drawString(30, 800, "Original")
    p.drawString(505, 800, f"Proposta {quotation.quotation_id}")

    # --------------------- LOGO ---------------------------
    center_x = (A4[0] - inch) / 2
    img = ImageReader('backoffice/media/logo/logo.png')
    p.drawImage(img, center_x, 600)

    # --------------------- TITLE ---------------------------
    p.setFontSize(12)
    p.setFillColorRGB(0, 0, 0)
    p.drawString(30, 500, f"Proposta {quotation.quotation_id}")
    p.drawString(470, 500, f"Data {datetime.date.today()}")

    # --------------------- TYPE ---------------------------
    quotation_type_text = "Tipo de Proposta"
    match quotation.quotation_type:
        case 'equipment':
            quotation_type_text = 'Fornecimento de Equipamento de Piscina'
        case 'renovation':
            quotation_type_text = 'Renovação de Piscina'

    p.drawString(30, 450, quotation_type_text)

    # --------------------- CLIENT ---------------------------
    p.drawString(60, 400, "Cliente:")
    p.drawString(105, 400, quotation.client.fiscal_name)
    p.drawString(80, 380, "A/C:")
    p.drawString(110, 380, quotation.client.name)
    p.drawString(110, 365, quotation.client_phone)
    p.drawString(110, 350, quotation.client_email)
    p.drawString(110, 335, quotation.client_address)
    p.drawString(110, 320, quotation.client.tax_number)

    # --------------------- GREETINGS ---------------------------
    greetings_style = getSampleStyleSheet()["Normal"]
    greetings_style.alignment = TA_JUSTIFY
    greetings_paragraph = Paragraph(quotation.greetings, greetings_style)
    greetings_paragraph.wrapOn(p, A4[0] - 2 * inch, A4[1])
    greetings_paragraph.drawOn(p, 30, 190)

    # --------------------- SIGNATURE ---------------------------
    p.drawString(110, 90, 'Vitor Filipe')

    # --------------------- FOOTER ---------------------------
    footer_img_size = 40
    footer_img = ImageReader('backoffice/media/logo/logo.png')
    p.drawImage(footer_img, 40, 40, width=footer_img_size, height=footer_img_size)

    pag_text = 'Pág. 1'
    p.drawString(A4[0] - 20 - p.stringWidth(pag_text), 20, pag_text)

    # --------------------- SECOND PAGE --------------------------------------------------------------
    p.showPage()

    # --------------------- HEADER ---------------------------
    p.drawString(30, 800, "Original")
    p.drawString(505, 800, f"Proposta {quotation.quotation_id}")

    # --------------------- POOL ---------------------------
    p.drawString(60, 750,
                 "A proposta, está baseada nos elementos fornecidos à VITORGEST, e têm as seguintes características:")
    table_data = [['Designação', 'Número', 'Área(m^2)', 'Forma', 'Prof. Máx.', 'Prof. Min.', 'Volume (m^2)',
                   'Tipo de Circulação'],
                  [f'{quotation.pool.length}x{quotation.pool.width}m', '1', quotation.pool.surface_area, 'Rectangular',
                   quotation.pool.max_depth, quotation.pool.min_depth, quotation.pool.volume,
                   quotation.pool.circulation_type],
                  ]
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ])
    table = Table(table_data, style=table_style)
    table.wrapOn(p, A4[0] - 2 * inch, A4[1])
    table.drawOn(p, 30, 680)

    address = str(quotation.pool.address)
    address_coord_x = str(quotation.pool.address.coordinate_x)
    address_coord_y = str(quotation.pool.address.coordinate_y)
    coordinates = f'{address_coord_x}, {address_coord_y} '
    p.drawString(100, 640, "Localização da obra:")
    p.drawString(120, 620, address)
    p.drawString(120, 600, f'Coordenadas: {coordinates}')
    p.drawString(100, 550, "Estrutura: A CARGO DO CLIENTE.")
    p.drawString(100, 530, "Revestimento: A CARGO DO CLIENTE.")

    p.drawString(100, 510, "Equipamento de Filtração:")
    filtrationEquip_style = getSampleStyleSheet()["Normal"]
    filtrationEquip_style.alignment = TA_JUSTIFY
    filtrationEquip = "A cargo da Vitorgest; Colocação dos materiais de encastrar. Depois da passagem da tubagem até a casa das máquinas é instalado todo o equipamento de filtração (bombas, filtros de areia…) quadro elétrico de proteção e comando e tratamento de água. Será fornecido e instalado todo o equipamento previsto nesta proposta de acordo com as normas em vigor."
    filtrationEquipParagraph = Paragraph(filtrationEquip, filtrationEquip_style)
    filtrationEquipParagraph.wrapOn(p, A4[0] - 2 * inch, A4[1])
    filtrationEquipParagraph.drawOn(p, 100, 450)

    p.drawString(100, 430, "Equipamento Suplementar: Ver proposta em opção.")
    p.drawString(100, 410, "Ligações à rede: Não estão previstas as ligações à rede eléctrica, água e esgotos")
    p.drawString(100, 390, "Casa das Máquinas: Não está prevista a sua construção.")
    p.drawString(100, 370, "Tanque de Compensação: Não previsto.")
    p.drawString(100, 350, "Escavação. Por conta do cliente ")
    p.drawString(100, 330, "Casa das Máquinas: Não está prevista a sua construção.")

    p.drawString(100, 310, "Acabamento:")
    p.drawString(100, 290, "Enchimento da piscina (água a cargo do Cliente).")
    p.drawString(100, 270, "Colocação dos equipamentos em funcionamento.")
    p.drawString(100, 250, "Testes e ensaios.")
    p.drawString(100, 230, "Entrega da piscina pronta a utilizar.")

    # --------------------- FOOTER ---------------------------
    p.drawImage(footer_img, 40, 40, width=footer_img_size, height=footer_img_size)

    pag_text = 'Pág. 2'
    p.drawString(A4[0] - 20 - p.stringWidth(pag_text), 20, pag_text)

    # --------------------- THIRD PAGE --------------------------------------------------------------
    p.showPage()

    # --------------------- HEADER ---------------------------
    p.drawString(30, 800, "Original")
    p.drawString(505, 800, f"Proposta {quotation.quotation_id}")

    # --------------------- EQUIPMENT ---------------------------
    p.drawString(60, 750, "Fornecimento de Equipamento")
    y = 650  # Initial y-coordinate
    line_height = 15
    max_y = 100  # Maximum y-coordinate before starting a new page

    for equipment in quotation.equipments.all():
        # Retrieve the equipment details
        name = equipment.name
        description = equipment.description
        equip_img_path = os.path.join(MEDIA_BASE_DIR, equipment.image.name)
        desired_height = 100

        with Image.open(equip_img_path) as img:
            # Calculate the desired width while maintaining the aspect ratio
            original_width, original_height = img.size
            aspect_ratio = original_width / original_height
            desired_width = desired_height * aspect_ratio

            # Resize the image with the calculated width and height
            img = img.resize((int(desired_width), desired_height), Image.ANTIALIAS)

            # Convert the PIL image to the ReportLab-compatible ImageReader format
            equip_img = ImageReader(img)
        # Check if there is enough space on the page for the next item
        if y < max_y:
            # Start a new page
            p.showPage()
            y = 700

        # Write the equipment details to the PDF
        p.drawImage(equip_img, 100, y-50, height=100)
        p.drawString(250, y, f'Name: {name}')
        p.drawString(250, y - line_height, f'Description: {description}')

        # Update the y-coordinate for the next equipment
        y -= line_height * 8

    # --------------------- FOOTER ---------------------------
    p.drawImage(footer_img, 40, 40, width=footer_img_size, height=footer_img_size)

    pag_text = 'Pág. 3'
    p.drawString(A4[0] - 20 - p.stringWidth(pag_text), 20, pag_text)

    # --------------------- SECOND PAGE --------------------------------------------------------------
    p.showPage()

    # --------------------- HEADER ---------------------------
    p.drawString(30, 800, "Original")
    p.drawString(505, 800, f"Proposta {quotation.quotation_id}")

    # --------------------- VALUES ---------------------------
    p.drawString(60, 750, 'I - VALORES')
    p.drawString(60, 740, '(Transporte incluído)')

    # --------------------- VALUES ---------------------------
    p.drawString(50, 700, "II – CONDIÇÕES DE PAGAMENTO")
    p.drawString(50, 680, "30% Com a adjudicação")
    p.drawString(50, 660, "30% Com a entrega de equipamento para início dos trabalhos")
    p.drawString(50, 640, "30% Na conclusão da instalação do equipamento")
    p.drawString(50, 620, "10% No final")
    p.drawString(50, 590, "III – ADJUDICAÇÃO")
    p.drawString(50, 570,
                 "VITORGEST, Lda.                                                                  O Cliente")
    p.drawString(50, 540, "______________________                                    _________________________")
    p.drawString(50, 520,
                 "                                                                      (concordo com as condições desta proposta)")
    p.drawString(50, 490, "Lisboa,____de_______________ de _____")
    p.drawString(50, 460, "Esta proposta é válida por 30 dias")

    p.showPage()
    # --------------------- VALUES ---------------------------
    text_x = 1 * inch
    text_y = 8 * inch

    p.drawString(text_x, text_y, "IV – GARANTIAS*")
    p.drawString(text_x, text_y - 0.2 * inch,
                 "Filtros e Bombas..............................................................3 Anos")
    p.drawString(text_x, text_y - 0.4 * inch,
                 "Equipamento de Tratamento...........................................3 Anos")
    p.drawString(text_x, text_y - 0.6 * inch,
                 "Magnapool + pH..............................................................3 Anos")
    p.drawString(text_x, text_y - 0.8 * inch, "Quadros Elétricos e Equipamentos.................................2 Anos")
    p.drawString(text_x, text_y - 1.0 * inch, "Revestimento em Tela Armada (estanquicidade)............10 Anos")
    p.drawString(text_x, text_y - 1.2 * inch, "*(Conforme norma dos fabricantes)")

    p.showPage()
    # --------------------- VALUES ---------------------------
    p.drawString(60, 600, 'IV - VALIDADE')

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # File response with the PDF content.
    pdf = buffer.getvalue()
    buffer.close()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="mypdf.pdf"'
    return response
