import os
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, inch
from pdf2image import convert_from_path

# === CONFIGURACIÓN ===
pdf_original = "PORFOLIO.pdf"   # tu archivo original en la misma carpeta
dpi_pdf = 300                   # resolución final
partes = 4
final_pdf = "Porfolio_Liam_Andino.pdf"

# === DIVIDIR EL PDF EN PARTES IGUALES ===
reader = PdfReader(pdf_original)
total_paginas = len(reader.pages)
por_parte = total_paginas // partes
part_files = []

for i in range(partes):
    writer = PdfWriter()
    start = i * por_parte
    end = (i+1) * por_parte if i < partes-1 else total_paginas
    for j in range(start, end):
        writer.add_page(reader.pages[j])
    out_name = f"Porfolio_Liam_Andino_Parte{i+1}.pdf"
    with open(out_name, "wb") as f:
        writer.write(f)
    part_files.append(out_name)
    print(f"✅ Generada {out_name} con páginas {start+1}-{end}")

# === CREAR PÁGINAS DE TEXTO (portada, perfil, índice, conclusión) ===
def crear_pagina_texto(nombre, lineas):
    c = canvas.Canvas(nombre, pagesize=landscape((17*inch, 11*inch)))
    c.setFont("Times-Roman", 36)
    y = 8*inch
    for linea in lineas:
        c.drawCentredString(8.5*inch, y, linea)
        y -= 1*inch
    c.showPage()
    c.save()

crear_pagina_texto("Portada.pdf", ["Liam Y. Andino Cruz", "Universidad Politécnica de Puerto Rico"])
crear_pagina_texto("Perfil.pdf", [
    "Perfil Profesional",
    "Soy un arquitecto en formación con experiencia en diseño técnico y conceptual.",
    "Me especializo en planos, detalles constructivos y conceptualización de proyectos.",
    "Domino AutoCAD, AutoCAD 3D y SketchUp."
])
crear_pagina_texto("Indice.pdf", ["Índice", "Secciones:", "Perfil Profesional", "Proyectos", "Conclusión y contacto"])
crear_pagina_texto("Conclusion.pdf", [
    "Conclusión y Contacto",
    "Mi enfoque es diseñar soluciones arquitectónicas que integren técnica, funcionalidad y creatividad.",
    "✉️ Contacto: liamandino@gmail.com"
])

# === CONVERTIR PARTES A IMÁGENES 300 dpi Y RECREAR PDFs LIMPIOS ===
pdf_parts_final = []
for idx, parte in enumerate(part_files, start=1):
    print(f"🔄 Procesando {parte}...")
    images = convert_from_path(parte, dpi=dpi_pdf)
    out_name = f"Porfolio_Liam_Andino_Parte{idx}.pdf"

    c = canvas.Canvas(out_name, pagesize=landscape((17*inch, 11*inch)))
    for img in images:
        img_path = f"temp_page.png"
        img.save(img_path, "PNG")
        c.drawImage(img_path, inch*0.5, inch*0.5,
                    width=16*inch, height=10*inch,
                    preserveAspectRatio=True, anchor="c")
        c.showPage()
        os.remove(img_path)
    c.save()
    pdf_parts_final.append(out_name)
    print(f"✅ Exportado {out_name} en 300 dpi limpio")

# === UNIR TODO EN EL PDF FINAL ===
merger = PdfMerger()
merger.append("Portada.pdf")
merger.append("Perfil.pdf")
merger.append("Indice.pdf")
for part in pdf_parts_final:
    merger.append(part)
merger.append("Conclusion.pdf")
merger.write(final_pdf)
merger.close()

print(f"🎉 Portafolio final generado: {final_pdf}")
