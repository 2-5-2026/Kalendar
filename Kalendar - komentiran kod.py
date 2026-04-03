import tkinter as tk  # za GUI; gumbi, prozor, itd.
import calendar
from tkinter import simpledialog, messagebox   # za a) prozorčić koji traži događaj i
                                               # b) drugi pop-up (upisan događaj)

import json  # za pohranjivanje događaja u program


class KalendarGUI:      # definicija klase (objekt cijelog kalendara)
    def __init__(self, root):    # self-objekt; root - taj (glavni) GUI prozor
        self.root = root
        self.root.title("Kalendar")      # naslov

# prvi mjesec i 2026. godina - otvaranjem programa uvijek time kreće
        self.mjesec = 1
        self.godina = 2026
        self.datoteka_dogadaja = "dogadaji.json"  # datoteka u kojoj se događaji spremaju

    # pokušaj učitavanja događaja iz datoteke; pretvaranje ključeva
    # jer json ne podržava određene oblike podataka 
        try:
            with open(self.datoteka_dogadaja, "r") as f:
                self.dogadaji = {tuple(map(int, k.split(","))): v for k, v in json.load(f).items()}
        except FileNotFoundError:
            self.dogadaji = {}    # ako datoteke nema - prazan rječnik


        top_frame = tk.Frame(root)    # okvir za sve elemente
        top_frame.pack(pady=40)

# gumbi za mijenjanje mjeseca
        self.gumb_iza = tk.Button(top_frame, text="◀", width=5, command=self.pred_mjesec)
        self.gumb_iza.grid(row=0, column=0, padx=5)

        self.gumb_sljed = tk.Button(top_frame, text="▶", width=5, command=self.sljed_mjesec)
        self.gumb_sljed.grid(row=0, column=2, padx=5)

        self.oznaka_mjesec = tk.Label(top_frame, text="", font=("Arial", 16))
        self.oznaka_mjesec.grid(row=0, column=1, padx=20)

# gumb za kalkulator
        self.gumb_kalkulator = tk.Button(root, text="Kalkulator datuma", width=20, command=self.kalkulator_datuma)
        self.gumb_kalkulator.pack(pady=5)

# tablica kalendara 
        okvir = tk.Frame(root)
        okvir.pack(pady=10)

# petljom se stvaraju dani pon-ned:
        dani = ["Pon", "Uto", "Sri", "Čet", "Pet", "Sub", "Ned"]
        for col in range(7):
            lbl = tk.Label(okvir, text=dani[col], font=("Arial", 10, "bold"), width=8)
            lbl.grid(row=0, column=col, padx=2, pady=2)

# gumbi za sve dane
        self.gumbi_dani = []
        for red in range(1, 7):      # max 6 redova
            red_gumbi = []
            for stupac in range(7):
                btn = tk.Button(
                    okvir,
                    text="",
                    width=8,
                    height=3,     # klik na dan poziva upravljanje događajem
                    command=lambda r=red, s=stupac: self.upravljaj_dogadaj(r, s)
                )  # lambda - funkcija za pamćenje red-stupac
                btn.grid(row=red, column=stupac, padx=2, pady=2)
                red_gumbi.append(btn)
            self.gumbi_dani.append(red_gumbi)

# prikaz se mijenja
        self.update_oznaka()
        self.prikaz()

# funkcija za update teksta mjeseca
    def update_oznaka(self):
        mjeseci = ["Siječanj","Veljača","Ožujak","Travanj","Svibanj","Lipanj",
                   "Srpanj","Kolovoz","Rujan","Listopad","Studeni","Prosinac"]
        self.oznaka_mjesec.config(text=f"{mjeseci[self.mjesec-1]} {self.godina}")

# funkcija za prethodni mjesec
    def pred_mjesec(self):
        self.mjesec -= 1
        if self.mjesec < 1:    # vraćanje na prošlu godinu
            self.mjesec = 12
            self.godina -= 1
        self.update_oznaka()
        self.prikaz()

# funkcija za sljedeći mjesec
    def sljed_mjesec(self):
        self.mjesec += 1
        if self.mjesec > 12:       # prijelaz na sljedeću godinu
            self.mjesec = 1
            self.godina += 1
        self.update_oznaka()
        self.prikaz()

# prikaz kalendara
    def prikaz(self):
        kal = calendar.monthcalendar(self.godina, self.mjesec)
        for i in range(6):   # petlja kroz dane
            for j in range(7):
                if i < len(kal) and kal[i][j] != 0:   # provjera postojanja dana
                    dan = kal[i][j]
                    kljuc = (dan, self.mjesec, self.godina)
                    tekst = str(dan)
                    if kljuc in self.dogadaji and self.dogadaji[kljuc]:   # ako postoji događaj, dodaje se znak
                        tekst += " •"
                    self.gumbi_dani[i][j].config(text=tekst)
                else:
                    self.gumbi_dani[i][j].config(text="")

# dohvaća koji je dan kliknut
    def upravljaj_dogadaj(self, red, stupac):
        kal = calendar.monthcalendar(self.godina, self.mjesec)
        if red-1 < len(kal):
            dan = kal[red-1][stupac]
            if dan == 0:
                return
            kljuc = (dan, self.mjesec, self.godina)

            if kljuc in self.dogadaji and self.dogadaji[kljuc]:
                self.prikaz_dogadaja(kljuc)        # ako već ima događaj
            else:
                self.unos_dogadaja(kljuc)     # ako nema događaj - omogućuje unos

# unos događaja
    def unos_dogadaja(self, kljuc):
        dogadaj = simpledialog.askstring("Unos događaja",                # pop-up za unos
             f"Unesi događaj za {kljuc[0]}.{kljuc[1]}.{kljuc[2]}:")
        if dogadaj:
            if kljuc not in self.dogadaji:
                self.dogadaji[kljuc] = []
            self.dogadaji[kljuc].append(dogadaj)    # spremanje događaja
            self.spremi_dogadaje()         # spremanje događaja u datoteku
            self.prikaz()
            messagebox.showinfo("Spremno", f"Događaj spremljen za {kljuc[0]}.{kljuc[1]}.{kljuc[2]}.")

    def prikaz_dogadaja(self, kljuc):
        top = tk.Toplevel(self.root)     # novi prozor za prikaz događaja
        top.title(f"Događaji {kljuc[0]}.{kljuc[1]}.{kljuc[2]}")

        for widget in top.winfo_children():
            widget.destroy()

        for idx, dogadaj in enumerate(self.dogadaji[kljuc], start=1):    # lista događaja
            frame = tk.Frame(top)
            frame.pack(fill="x", padx=10, pady=2)

            lbl = tk.Label(frame, text=f"{idx}. {dogadaj}", anchor="w")
            lbl.pack(side="left", fill="x", expand=True)

# gumb za brisanje
            def brisanje(idx):
                return lambda: self.obrisi_dogadaj(kljuc, idx-1, top)
            btn_del = tk.Button(frame, text="Obriši", command=brisanje(idx))
            btn_del.pack(side="right")

# funkcija za dodavanje novog
        def dodaj_novi():
            self.unos_dogadaja(kljuc)
            top.destroy()

        btn_dodaj = tk.Button(top, text="Dodaj novi događaj", command=dodaj_novi)
        btn_dodaj.pack(pady=5)

# funkcija za brisanje događaja
    def obrisi_dogadaj(self, kljuc, idx, top):
        del self.dogadaji[kljuc][idx]   # briše jedan događaj
        if not self.dogadaji[kljuc]:    # ako nema više događaja, briše se datum
            del self.dogadaji[kljuc]
        self.spremi_dogadaje()    # spremanje svih promjena
        self.prikaz()
        top.destroy()
        if kljuc in self.dogadaji:
            self.prikaz_dogadaja(kljuc)

# funkcije kalkulatora datuma
    def kalkulator_datuma(self):
        datum_str = simpledialog.askstring("Kalkulator datuma", "Unesi datum (dd.mm.gggg.):") # pop-up za unos
        if datum_str:
            try:
                d, m, g = map(int, datum_str.rstrip('.').split("."))
                dani_hr = ["ponedjeljak", "utorak", "srijeda", "četvrtak",
                           "petak", "subota", "nedjelja"]
                dan_tjedna = dani_hr[calendar.weekday(g, m, d)]   
                messagebox.showinfo("Dan u tjednu", f"{d}.{m}.{g}. je {dan_tjedna}.") # rezultat
            except:
                messagebox.showerror("Greška", "Neispravan format datuma!")  # ako pogreška

    def spremi_dogadaje(self):
        # sprema rječnik u json, pretvori tuple u string (jer ne podržava)
        s = {f"{k[0]},{k[1]},{k[2]}": v for k, v in self.dogadaji.items()}
        with open(self.datoteka_dogadaja, "w") as f:
            json.dump(s, f)    # sprema u datoteku


# glavni dio
if __name__ == "__main__":    # pokreće program  
    root = tk.Tk()            # glavni prozor
    app = KalendarGUI(root)   # kreira kalendar kao "aplikaciju"
    root.mainloop()           # pokreće GUI

    # kraj
