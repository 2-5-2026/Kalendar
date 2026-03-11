import tkinter as tk

class KalendarGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Kalendar")
        top_frame = tk.Frame(root)
        top_frame.pack(pady=40)
        self.btn_prev = tk.Button(top_frame, text="◀", width=5)
        self.btn_prev.grid(row=0, column=0, padx=5)
        self.lbl_mjesec = tk.Label(top_frame, text="Siječanj 2026", font=("Arial", 16))
        self.lbl_mjesec.grid(row=0, column=1, padx=20)
        self.btn_next = tk.Button(top_frame, text="▶", width=5)
        self.btn_next.grid(row=0, column=2, padx=5)
        self.btn_kalkulator = tk.Button(root, text="Kalkulator datuma", width=20)
        self.btn_kalkulator.pack(pady=5)

        okvir = tk.Frame(root)
        okvir.pack(pady=10)

        dani = ["Pon", "Uto", "Sri", "Čet", "Pet", "Sub", "Ned"]
        for col in range(7):
            lbl = tk.Label(okvir, text=dani[col], font=("Arial", 10, "bold"), width=8)
            lbl.grid(row=0, column=col, padx=2, pady=2)

        self.dani_buttons = []

        for row in range(1, 7):  
            row_buttons = []
            
            for col in range(7):  
                btn = tk.Button(okvir, text="", width=8, height=3)
                btn.grid(row=row, column=col, padx=2, pady=2)
                row_buttons.append(btn)
            self.dani_buttons.append(row_buttons)

if __name__ == "__main__":
    root = tk.Tk()
    app = KalendarGUI(root)
    root.mainloop()

