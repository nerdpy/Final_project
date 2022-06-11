import tkinter.messagebox
import os
import pygubu

class Pojisteny():
    def __init__(self, jmeno, email, telefon):
        self.jmeno = jmeno
        self.email = email
        self.telefon = telefon


class Databaze():
    pojistenci = []  #musíme to přečíst z listu v listboxu

    def __init__(self, soubor):
        self.soubor = soubor

    def novyPojistenecUloz(self, jmeno, email, telefon):
        """do databaze.csv uloží nového pojištěnce"""
        novy_pojistenec = Pojisteny(jmeno, email, telefon)
        with open(self.soubor, "a", encoding="utf-8") as databaze:
            databaze.write(f"{novy_pojistenec.jmeno};{novy_pojistenec.email};{novy_pojistenec.telefon}\n")

    def pridejPojistence(self, jmeno, email, telefon):
        """přidá pojištěnce do listu pojištěnců"""
        p = Pojisteny(jmeno, email, telefon)
        self.pojistenci.append(p)

    def nactiPojistence(self):
        """zobrazí pojištence"""
        self.pojistenci = []
        with open(self.soubor, "r", encoding="utf-8") as f:
            for p in f.readlines():
                jmeno, email, telefon = p.strip().split(";")
                self.pridejPojistence(jmeno, email, telefon)

    def vratVsechny(self):
        return self.pojistenci

class AplikacePojisteni():
    """vytvoří první okno, kde je přehled a odkaz na další okno"""
    def __init__(self, master):
        self.master = master
        cesta = os.path.join(os.getenv("APPDATA"), "DatabazePojisteni")
        try:
            cesta = os.path.join(os.getenv("APPDATA"), "DatabazePojisteni")
            if not os.path.exists(cesta):
                os.mkdir(cesta)
        except:
            tkinter.messagebox.showerror("Chyba", "Nepodařilo se vytvořit složku")

        self.db = Databaze(os.path.join(cesta, "databazePojisteni.csv"))
        self.builder = pygubu.Builder()
        self.builder.add_from_file("databaze_pojisteni_pygubu.ui")
        self.builder.get_object("frame1", self.master)
        self.builder.connect_callbacks(self)

    def tlacitkoNovyPojistenecClicked(self):
        """vytvoří druhý formulář, kde můžeme uložit nového pojištěnce"""
        novy_pojistenec_okno = tkinter.Tk()
        Okno_novy_pojisteny(novy_pojistenec_okno)
        # novy_pojistenec_okno.destroy()

    def tlacitkoNactiPojistenceClicked(self):
        """načte pojištěnce do listboxu"""
        try:
            self.db.nactiPojistence()
        except:
            tkinter.messagebox.showerror("Chyba", "Databázi se nepodařilo načíst, zřejmě neobsahuje žádná data.")
            return

        listbox = self.builder.get_object("databazePojistenych")
        listbox.delete(0, tkinter.END) #vymaže
        for p in self.db.vratVsechny(): #znovu načteme
            listbox.insert(tkinter.END, p.jmeno)

    def vypisDetailuPojistence(self, arg):
        """při pokliku kurzorem na pojištence v listboxu vypíše detaily"""
        listbox = self.builder.get_object("databazePojistenych")
        oznaceny_pojistenec = listbox.curselection()[0] + 1 if len(listbox.curselection()) > 0 else None
        if len(self.db.pojistenci) == 0 or oznaceny_pojistenec == None:
            return
        pojistenec = self.db.pojistenci[oznaceny_pojistenec - 1]  # - 1]
        jmeno_label = self.builder.get_object("labelJmeno")
        email_label = self.builder.get_object("labelEmail")
        telefon_label = self.builder.get_object("labelTelefon")
        jmeno_label["text"] = pojistenec.jmeno
        email_label["text"] = pojistenec.email
        telefon_label["text"] = pojistenec.telefon

class Okno_novy_pojisteny():
    """kód pro druhý formulář"""
    def __init__(self, master):
        self.master = master
        cesta = os.path.join(os.getenv("APPDATA"), "DatabazePojisteni")
        try:
            cesta = os.path.join(os.getenv("APPDATA"), "DatabazePojisteni")
            if not os.path.exists(cesta):
                os.mkdir(cesta)
        except:
            tkinter.messagebox.showerror("Chyba", "Nepodařilo se vytvořit složku")

        self.db_novy_pojistenc = Databaze(os.path.join(cesta, "databazePojisteni.csv"))
        self.builder_novy_pojistenec = pygubu.Builder()
        self.builder_novy_pojistenec.add_from_file("databaze_pojisteni_pygubu_2.ui")
        self.builder_novy_pojistenec.get_object("frame2", self.master)
        self.builder_novy_pojistenec.connect_callbacks(self)

    def tlacitkoNovyPojistenecUlozClicked(self):
        """při kliknutí na ulož uloží nového pojištěnce do databáze.csv"""
        cesta = os.path.join(os.getenv("APPDATA"), "DatabazePojisteni")
        jmeno = self.builder_novy_pojistenec.get_object("entry1").get()
        email = self.builder_novy_pojistenec.get_object("entry2").get()
        telefon = self.builder_novy_pojistenec.get_object("entry3").get()
        if jmeno == "" or email == "" or telefon == "":
            tkinter.messagebox.showinfo("Chyba", "Nezadal jsi všechny údaje")
        else:
            self.db = Databaze(os.path.join(cesta, "databazePojisteni.csv"))
            self.db.novyPojistenecUloz(jmeno, email, telefon)
            tkinter.messagebox.showinfo("Uloženo", "Data byla uložena")


okno = tkinter.Tk()
aplikace = AplikacePojisteni(okno)
okno.mainloop()