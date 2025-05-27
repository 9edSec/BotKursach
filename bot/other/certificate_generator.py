from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import white 
from pdfrw import PdfReader, PdfWriter, PageMerge
from io import BytesIO
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def generate_certificate(full_name):
    pdfmetrics.registerFont(TTFont('DejaVuSans', 'bot/other/fonts/DejaVuSans.ttf'))

    template_path = "bot/other/template/certificate-template.pdf" 
    safe_full_name = full_name.replace(" ", "_").replace("/", "_").replace("\\", "_")
    output_path = f"certificate_{safe_full_name}.pdf"


    page_width, page_height = A4

    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)

    
    font_name = 'DejaVuSans' 
    font_size = 20

    
    text_width = can.stringWidth(full_name, font_name, font_size)
    x_centered = (page_width - text_width) / 2
    y = 200 

    can.setFont(font_name, font_size)
    can.setFillColor(white) 
    can.drawString(x_centered, y, full_name)
    can.save()

    packet.seek(0)
    new_pdf_data = PdfReader(packet) 

    # --- Работа с pdfrw для наложения на шаблон ---
    try:
        template_pdf = PdfReader(template_path)
        if not template_pdf.pages:
            print(f"Ошибка: PDF-шаблон '{template_path}' не содержит страниц.")
            return None 

        page_to_modify = template_pdf.pages[0] 

        
        if not new_pdf_data.pages:
            print(f"Ошибка: Сгенерированный PDF с именем '{full_name}' не содержит страниц.")
            return None 

        overlay_page = new_pdf_data.pages[0]

        # Наложение
        PageMerge(page_to_modify).add(overlay_page).render()

        
        writer = PdfWriter()
        writer.trailer = template_pdf 
        writer.addpages(template_pdf.pages) 
        writer.write(output_path)

    except FileNotFoundError:
        print(f"Ошибка: Файл шаблона '{template_path}' не найден.")
        return None 
    except Exception as e:
        print(f"Произошла ошибка при работе с PDF: {e}")
        return None 

    return output_path

