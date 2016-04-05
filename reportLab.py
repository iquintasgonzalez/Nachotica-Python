from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate,Table,TableStyle,Paragraph,Spacer,Image
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

import time
import datetime
import sqlite3 as dbapi
from gi.repository import Gtk
class genpdf():
    """
    """
    def __init__(self):
        """
        Conexion con la base de datos
        """
        self.bd = dbapi.connect("basedatos.dat")
        self.cursor = self.bd.cursor()
        #foto = Image("./talleres-rodal.jpg")
        self.elementos = []

    def generatepdf(self):
        """
        """
        historialpdf ="Pdf"+ str(datetime.date.today()) +"_.pdf"
        c = canvas.Canvas(historialpdf, pagesize=A4)
        c.drawString(20,800,"Arquitectura Pro")

        #c.drawImage(foto,200,800)
        #c.drawImage(self.foto, 1*cm, 26*cm, 19*cm, 3*cm)

        tabla = self.table()
        tabla.wrapOn(c, 20, 30)
        tabla.drawOn(c, 25, 650)
        c.save()

        self.emergent("PDF Generado")
        #self.elements.append(tabla)
        #doc.build(elements)

    def table(self):
        """
        Metodo tabla:
        Este metodo genera la tabla en el pdf
        volcando el contenido de la base de datos
        """
        futbolistas = list(self.cursor.execute("select * from Arquitectura"))
        titulos = [["DNI", "EMPRESA","GERENTE", "FECHA", "CLIENTE", "CIF","TELEFONO","DIRECCION"]]

        clientes = titulos + futbolistas
        tabla = Table(clientes)

        tabla.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 2, colors.white),
                                   ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                   ('LEFTPADDING', (0, 0), (-1, -1), 3),
                                   ('RIGHTPADDING', (0, 0), (-1, -1), 3),
                                   ('FONTSIZE', (0, 1), (-1, -1), 10),
                                   ('BACKGROUND', (0,1),(-1,-1), colors.white),
                                   ('BACKGROUND', (0, 0), (-1, 0), colors.white)]))

        return tabla
    def close(self, widget):
        """"
        """
        widget.destroy()

    def emergent(self, texto):
        """
        """
        window = Gtk.Window(title="Warning")
        label = Gtk.Label(texto)
        label.set_padding(15,15)
        window.add(label)
        window.connect("delete-event", self.close)
        window.set_position(Gtk.PositionType.RIGHT)
        window.show_all()

genpdf().generatepdf()