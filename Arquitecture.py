import sqlite3 as dbapi
from gi.repository import Gtk, Gdk

class Arquitectura:



    def __init__(self):
        #Conexión con la base de datos
        self.bd = dbapi.connect("basedatos.dat")
        self.cursor = self.bd.cursor()
        self.cursor.execute("CREATE TABLE Arquitectura (codigo VARCHAR(7) PRIMARY KEY NOT NULL,"
                            "empresa VARCHAR(20),"
                            "gerente VARCHAR(20),"
                            "fecha VARCHAR(50) ,"
                            "cliente VARCHAR(10),"
                            "cif VARCHAR(10),"
                           "telefono VARCHAR(56),"
                           "direccion VARCHAR(10))")

        #Abrimos y conectamos a la interfaz de Arquitectura
        self.builder = Gtk.Builder()
        self.builder.add_from_file("Arquitectura.glade")
        self.inicializar()
        self.ventana = self.builder.get_object("Arquitectura")

        #Declaramos los nombres de los métodos para que al pulsar el boton tenga función
        sinais = {"on_insertar_clicked": self.on_insertar_clicked,
                      "on_consultar_clicked": self.on_consultar_clicked,
                      "on_borrar_clicked": self.on_borrar_clicked,
                      "on_Modificar_clicked": self.on_Modificar_clicked,
                      "delete-event": Gtk.main_quit}
        self.builder.connect_signals(sinais)
        self.ventana.set_title("Arquitectura")
        self.ventana.show_all()


    def inicializar(self):
        #treeview o tabla, en el que se muestran los datos de la base de datos
        self.box = self.builder.get_object("box2")
        self.scroll = Gtk.ScrolledWindow()
        self.scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.vista = Gtk.TreeView()
        self.box.add(self.scroll)
        self.scroll.add(self.vista)
        self.scroll.set_size_request(500, 500)
        self.scroll.show()

        self.lista = Gtk.ListStore(str, str, str, str, str, str, str, str)

        self.lista.clear()
        self.cursor.execute("select * from Arquitectura")
        #print(self.cursor.fetchall())
        for merla in self.cursor:
            self.lista.append(merla)

        self.vista.set_model(self.lista)

        for i, title in enumerate(["codigo","empresa","gerente","fecha","cliente","cif", "telefono", "direccion"]):
            render = Gtk.CellRendererText()
            columna = Gtk.TreeViewColumn(title, render, text=i)
            self.vista.append_column(columna)

    # Método Consultar, imprime los datos de la base
    def on_consultar_clicked(self, control):
        self.actualizar()

    #Metodo borrar que borra seleccionando la fila en la tabla
    def on_borrar_clicked(self, widget):
        selection = self.vista.get_selection()
        model, selec = selection.get_selected()
        if selec != None:
            self.codigo = model[selec][0]
            self.cursor.execute("delete from Arquitectura where codigo ='" + self.codigo + "'")
            self.actualizar()
            self.bd.commit()
            self.popup("Borrado")

     #Método Modificar. Modifica a través de la primary Key
    def on_Modificar_clicked(self, modificar):
        codigo = self.builder.get_object("codigo").get_text()
        empresa = self.builder.get_object("empresa").get_text()
        gerente = self.builder.get_object("gerente").get_text()
        fecha = self.builder.get_object("fecha").get_text()
        cliente = self.builder.get_object("cliente").get_text()
        cifnif = self.builder.get_object("cifnif").get_text()
        telefono = self.builder.get_object("telefono").get_text()
        direccion = self.builder.get_object("direccion").get_text()

        self.cursor.execute("update Arquitectura set codigo ='" + codigo + "'"
                                             ",empresa='" + empresa + "'"
                                             ",fecha='" + fecha + "'"
                                             ",cliente='" + cliente + "'"
                                             ",cif='" + cifnif +"'"
                                             ",telefono='" + telefono +"'"
                                             ",direccion='" + direccion +"' where codigo='" + codigo + "'")
        self.popup("Modificado")
        self.bd.commit()
        self.actualizar()

    # Método insertar
    def on_insertar_clicked(self, control):
        codigo = self.builder.get_object("codigo").get_text()
        empresa = self.builder.get_object("empresa").get_text()
        gerente = self.builder.get_object("gerente").get_text()
        fecha = self.builder.get_object("fecha").get_text()
        cliente = self.builder.get_object("cliente").get_text()
        cifnif = self.builder.get_object("cifnif").get_text()
        telefono = self.builder.get_object("telefono").get_text()
        direccion = self.builder.get_object("direccion").get_text()
        try:
            self.cursor.execute(
                "insert into Arquitectura values('" + codigo + "'"
                                         ",'" + empresa + "'"
                                         ",'" + gerente + "'"
                                         ",'" + fecha+"'"
                                         ",'" + cliente + "'"
                                         ",'" + cifnif +"'"
                                         ",'" + telefono +"'"
                                         ",'" + direccion +"')")
            self.popup("Insertado")
            self.actualizar()
            # Siempre se debe hacer un commit al final de cada evento
            self.bd.commit()
        except dbapi.IntegrityError:
            self.popup("El cliente ya existe, por favor modifique el codigo :)")

    #Este metodo simplemente actualiza la tabla
    def actualizar(self):
        self.lista.clear()
        self.cursor.execute("select * from Arquitectura")
        #print(self.cursor.fetchall())
        for merla in self.cursor:
            self.lista.append(merla)

        self.vista.set_model(self.lista)

    def cerrar(self, widget):
        widget.destroy()

    #Este metodo abre una ventana emergente que muestra
    # el texto correspondiente a cada metodo
    def popup(self, texto):
        window = Gtk.Window(title="Aviso")
        label = Gtk.Label(texto)
        label.set_padding(15, 15)
        window.add(label)
        window.connect("delete-event", self.cerrar)
        window.set_position(Gtk.PositionType.RIGHT)
        window.show_all()
