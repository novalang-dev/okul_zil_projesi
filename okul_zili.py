#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import threading
import subprocess
import platform
from datetime import datetime
import requests
import customtkinter as ctk

# ==========================================
# SUPABASE VE YAPILANDIRMA
# ==========================================
SUPABASE_URL = "https://hwaracybbfvonchqimla.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imh3YXJhY3liYmZ2b25jaHFpbWxhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTE1Mzk1OTYsImV4cCI6MjEwNzExNTU5Nn0.y6OCOwFo3Ma76SMFjw-mnFbQu0dwNCuJ7hcrWFQaPrU"

def kaynak_yolu_al(goreceli_yol):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, goreceli_yol)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), goreceli_yol)

SES_DOSYALARI = {
    "ogrenci": kaynak_yolu_al(os.path.join("sesler", "ogrenci.mp3")),
    "ogretmen": kaynak_yolu_al(os.path.join("sesler", "ogretmen.mp3")),
    "cikis": kaynak_yolu_al(os.path.join("sesler", "cikis.mp3")),
    "istiklal": kaynak_yolu_al(os.path.join("sesler", "istiklal.mp3")),
    "siren": kaynak_yolu_al(os.path.join("sesler", "siren.mp3"))
}

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")


# ==========================================
# AYARLAR PENCERESİ (GÖRSEL 1 İLE BİREBİR)
# ==========================================
class AyarlarPenceresi(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Okul Zili Ayarları")
        self.geometry("580x620")
        self.resizable(False, False)
        
        # Sekmeli Yapı
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)

        self.tabview.add("Hemen Çal")
        self.tabview.add("Saatler")
        self.tabview.add("Melodiler")
        self.tabview.add("Müzik Yayını")
        self.tabview.add("Hafta Sonu")

        self.tabview.set("Melodiler")
        self.melodiler_sekmesini_tasarla()

    def melodiler_sekmesini_tasarla(self):
        tab = self.tabview.tab("Melodiler")

        # --- 1. Öğrenci Zili ---
        f1 = ctk.CTkFrame(tab)
        f1.pack(fill="x", padx=10, pady=8)
        
        lbl1 = ctk.CTkLabel(f1, text="Öğrenci Zili", font=ctk.CTkFont(weight="bold", size=13))
        lbl1.pack(anchor="w", padx=10, pady=(5, 2))

        r1 = ctk.CTkFrame(f1, fg_color="transparent")
        r1.pack(fill="x", padx=10, pady=2)
        ctk.CTkOptionMenu(r1, values=["Melodi 1.mp3", "Melodi 2.mp3", "Melodi 5.mp3"], width=180).pack(side="left", padx=5)
        ctk.CTkButton(r1, text="Dinle", width=70, fg_color="#e2e8f0", text_color="#0f172a", hover_color="#cbd5e1").pack(side="left", padx=5)
        ctk.CTkLabel(r1, text="Ses:").pack(side="left", padx=(10, 2))
        ctk.CTkEntry(r1, width=45, placeholder_text="80").pack(side="left")
        ctk.CTkLabel(r1, text="%").pack(side="left", padx=2)

        cb1 = ctk.CTkCheckBox(f1, text="Anonslu")
        cb1.select()
        cb1.pack(anchor="w", padx=15, pady=(5, 2))

        cb2 = ctk.CTkCheckBox(f1, text="1. zil sıra için olduğundan anons yapma")
        cb2.select()
        cb2.pack(anchor="w", padx=15, pady=(2, 8))

        # --- 2. Öğretmen Zili ---
        f2 = ctk.CTkFrame(tab)
        f2.pack(fill="x", padx=10, pady=8)
        
        lbl2 = ctk.CTkLabel(f2, text="Öğretmen Zili", font=ctk.CTkFont(weight="bold", size=13))
        lbl2.pack(anchor="w", padx=10, pady=(5, 2))

        r2 = ctk.CTkFrame(f2, fg_color="transparent")
        r2.pack(fill="x", padx=10, pady=2)
        ctk.CTkOptionMenu(r2, values=["Melodi 6.mp3", "Melodi 3.mp3"], width=180).pack(side="left", padx=5)
        ctk.CTkButton(r2, text="Dinle", width=70, fg_color="#e2e8f0", text_color="#0f172a", hover_color="#cbd5e1").pack(side="left", padx=5)
        ctk.CTkLabel(r2, text="Ses:").pack(side="left", padx=(10, 2))
        ctk.CTkEntry(r2, width=45, placeholder_text="80").pack(side="left")
        ctk.CTkLabel(r2, text="%").pack(side="left", padx=2)

        cb3 = ctk.CTkCheckBox(f2, text="Anonslu")
        cb3.select()
        cb3.pack(anchor="w", padx=15, pady=(5, 8))

        # --- 3. Çıkış Zili ---
        f3 = ctk.CTkFrame(tab)
        f3.pack(fill="x", padx=10, pady=8)
        
        lbl3 = ctk.CTkLabel(f3, text="Çıkış Zili", font=ctk.CTkFont(weight="bold", size=13))
        lbl3.pack(anchor="w", padx=10, pady=(5, 2))

        r3 = ctk.CTkFrame(f3, fg_color="transparent")
        r3.pack(fill="x", padx=10, pady=2)
        ctk.CTkOptionMenu(r3, values=["Melodi 1.mp3", "Melodi 4.mp3"], width=180).pack(side="left", padx=5)
        ctk.CTkButton(r3, text="Dinle", width=70, fg_color="#e2e8f0", text_color="#0f172a", hover_color="#cbd5e1").pack(side="left", padx=5)
        ctk.CTkLabel(r3, text="Ses:").pack(side="left", padx=(10, 2))
        ctk.CTkEntry(r3, width=45, placeholder_text="80").pack(side="left")
        ctk.CTkLabel(r3, text="%").pack(side="left", padx=2)

        # Alt Oynatma Barı
        bot_frame = ctk.CTkFrame(tab, fg_color="transparent")
        bot_frame.pack(fill="x", side="bottom", padx=10, pady=10)
        ctk.CTkSlider(bot_frame).pack(side="left", fill="x", expand=True, padx=(0, 10))
        ctk.CTkButton(bot_frame, text="Durdur", width=80, fg_color="#e2e8f0", text_color="#0f172a").pack(side="left")


# ==========================================
# ANA PENCERE (GÖRSEL 2 İLE BİREBİR)
# ==========================================
class AnaEkran(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Okul Zil Sistemi - Ana Menü")
        self.geometry("750x670")
        self.resizable(False, False)

        self.zil_durumu_aktif = True
        self.yerel_zil_cache = []

        self.ui_tasarla()

        # Arka Plan Saati ve Bulut Kontrol Thread'i
        threading.Thread(target=self.arka_plan_dongusu, daemon=True).start()

    def ui_tasarla(self):
        # Sol ve Sağ Kolon
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ================= SOL TARAFI: DERS SAATLERİ TABLOSU =================
        self.sol_frame = ctk.CTkFrame(self, fg_color="#f8fafc", border_width=1, border_color="#cbd5e1")
        self.sol_frame.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="nsew")

        # Üst Menü Butonu
        self.btn_menu = ctk.CTkButton(
            self.sol_frame, text="🔔 Menü", fg_color="#f1f5f9", text_color="#0f172a",
            hover_color="#e2e8f0", anchor="w", width=80, command=self.ayarlari_ac
        )
        self.btn_menu.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Başlıklar
        ctk.CTkLabel(self.sol_frame, text="Öğrenci\nGiriş", font=ctk.CTkFont(size=11, weight="bold")).grid(row=0, column=1, padx=2)
        ctk.CTkLabel(self.sol_frame, text="Öğretmen\nGiriş", font=ctk.CTkFont(size=11, weight="bold")).grid(row=0, column=2, padx=2)
        ctk.CTkLabel(self.sol_frame, text="Ders\nÇıkış", font=ctk.CTkFont(size=11, weight="bold")).grid(row=0, column=3, padx=2)

        # 16 Ders İçin Kutular
        self.ders_entries = []
        for i in range(16):
            r = i + 1
            ctk.CTkLabel(self.sol_frame, text=f"{r}. Ders", font=ctk.CTkFont(size=11)).grid(row=r, column=0, padx=5, pady=2, sticky="e")
            
            e1 = ctk.CTkEntry(self.sol_frame, width=55, height=22, justify="center")
            e1.insert(0, "--:--")
            e1.grid(row=r, column=1, padx=2, pady=2)

            e2 = ctk.CTkEntry(self.sol_frame, width=55, height=22, justify="center")
            e2.insert(0, "--:--")
            e2.grid(row=r, column=2, padx=2, pady=2)

            e3 = ctk.CTkEntry(self.sol_frame, width=55, height=22, justify="center")
            e3.insert(0, "--:--")
            e3.grid(row=r, column=3, padx=2, pady=2)

            self.ders_entries.append((e1, e2, e3))

        # Alt Buton
        btn_tepsi = ctk.CTkButton(self.sol_frame, text="Sistem Tepsisine Küçült", height=28)
        btn_tepsi.grid(row=17, column=0, columnspan=4, padx=10, pady=8, sticky="ew")

        # ================= SAĞ TARAF: KONTROL PANELERİ =================
        self.sag_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.sag_frame.grid(row=0, column=1, padx=(5, 10), pady=10, sticky="nsew")

        # --- 1. Sistem Saati ve Zil Durumu ---
        top_box = ctk.CTkFrame(self.sag_frame)
        top_box.pack(fill="x", pady=(0, 8))

        clock_frame = ctk.CTkFrame(top_box, fg_color="transparent")
        clock_frame.pack(side="left", padx=10, pady=5)
        ctk.CTkLabel(clock_frame, text="Sistem Saati", font=ctk.CTkFont(size=11)).pack()
        self.lbl_saat = ctk.CTkLabel(clock_frame, text="10:05:59", font=ctk.CTkFont(size=22, weight="bold"), text_color="#2563eb")
        self.lbl_saat.pack()

        status_frame = ctk.CTkFrame(top_box, fg_color="transparent")
        status_frame.pack(side="right", padx=10, pady=5)
        ctk.CTkLabel(status_frame, text="Zil Durumu", font=ctk.CTkFont(size=11)).pack()
        
        btn_row = ctk.CTkFrame(status_frame, fg_color="transparent")
        btn_row.pack()
        self.btn_durum_acik = ctk.CTkButton(btn_row, text="Açık", width=50, fg_color="#16a34a", command=self.zil_aktif_et)
        self.btn_durum_acik.pack(side="left", padx=2)
        self.btn_durum_kapat = ctk.CTkButton(btn_row, text="Kapat", width=50, fg_color="#cbd5e1", text_color="#0f172a", command=self.zil_kapat)
        self.btn_durum_kapat.pack(side="left", padx=2)

        # --- 2. Marşlar ve Siren ---
        mars_box = ctk.CTkFrame(self.sag_frame)
        mars_box.pack(fill="x", pady=5)
        ctk.CTkLabel(mars_box, text="Marşlar ve Siren", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=4)

        items = [
            ("İstiklal Marşı", lambda: self.ses_cal("istiklal")),
            ("1 dk Saygı Duruşu", None),
            ("1 dk Saygı Duruşu ve İstiklal Marşı", None),
            ("2 dk Saygı Duruşu ve İstiklal Marşı", None),
            ("Siren", lambda: self.ses_cal("siren"))
        ]
        for t, cmd in items:
            row = ctk.CTkFrame(mars_box, fg_color="transparent")
            row.pack(fill="x", padx=10, pady=2)
            ctk.CTkLabel(row, text=t, font=ctk.CTkFont(size=11)).pack(side="left")
            ctk.CTkButton(row, text="Çal", width=55, height=22, fg_color="#cbd5e1", text_color="#0f172a", command=cmd).pack(side="right")

        # --- 3. Ziller ---
        zil_box = ctk.CTkFrame(self.sag_frame)
        zil_box.pack(fill="x", pady=5)
        ctk.CTkLabel(zil_box, text="Ziller", font=ctk.CTkFont(size=12, weight="bold")).pack(anchor="w", padx=10, pady=4)

        ziller = [
            ("Öğrenci Giriş Zili", lambda: self.ses_cal("ogrenci")),
            ("Öğretmen Giriş Zili", lambda: self.ses_cal("ogretmen")),
            ("Ders Çıkış Zili", lambda: self.ses_cal("cikis"))
        ]
        for t, cmd in ziller:
            row = ctk.CTkFrame(zil_box, fg_color="transparent")
            row.pack(fill="x", padx=10, pady=2)
            ctk.CTkLabel(row, text=t, font=ctk.CTkFont(size=11)).pack(side="left")
            ctk.CTkButton(row, text="Çal", width=55, height=22, fg_color="#cbd5e1", text_color="#0f172a", command=cmd).pack(side="right")

        # --- 4. Ses Denetimi & Bilgisayar Kapat ---
        bot_box = ctk.CTkFrame(self.sag_frame, fg_color="transparent")
        bot_box.pack(fill="x", pady=5)
        bot_box.grid_columnconfigure(0, weight=1)
        bot_box.grid_columnconfigure(1, weight=1)

        # Ses Denetimi
        ses_frame = ctk.CTkFrame(bot_box)
        ses_frame.grid(row=0, column=0, padx=(0, 2), sticky="nsew")
        ctk.CTkLabel(ses_frame, text="Ses Denetimi", font=ctk.CTkFont(size=11)).pack(anchor="w", padx=8, pady=2)
        
        s_row = ctk.CTkFrame(ses_frame, fg_color="transparent")
        s_row.pack(fill="x", padx=5)
        ctk.CTkSlider(s_row, width=100).pack(side="left")
        ctk.CTkLabel(s_row, text="%100", font=ctk.CTkFont(size=10)).pack(side="left", padx=2)
        ctk.CTkButton(ses_frame, text="Sesi Kapat", height=22, fg_color="#cbd5e1", text_color="#0f172a").pack(padx=8, pady=5, fill="x")

        # Bilgisayar Kapat
        pc_frame = ctk.CTkFrame(bot_box)
        pc_frame.grid(row=0, column=1, padx=(2, 0), sticky="nsew")
        ctk.CTkLabel(pc_frame, text="Bilgisayar Kapat", font=ctk.CTkFont(size=11)).pack(anchor="w", padx=8, pady=2)
        ctk.CTkEntry(pc_frame, height=22, justify="center", placeholder_text="--:--").pack(padx=8, pady=2, fill="x")
        ctk.CTkButton(pc_frame, text="Kaydet", height=22, fg_color="#cbd5e1", text_color="#0f172a").pack(padx=8, pady=5, fill="x")

    def ayarlari_ac(self):
        AyarlarPenceresi(self)

    def zil_aktif_et(self):
        self.zil_durumu_aktif = True
        self.btn_durum_acik.configure(fg_color="#16a34a")
        self.btn_durum_kapat.configure(fg_color="#cbd5e1", text_color="#0f172a")

    def zil_kapat(self):
        self.zil_durumu_aktif = False
        self.btn_durum_kapat.configure(fg_color="#dc2626", text_color="#ffffff")
        self.btn_durum_acik.configure(fg_color="#cbd5e1", text_color="#0f172a")

    def ses_cal(self, tip):
        dosya = SES_DOSYALARI.get(tip)
        if dosya and os.path.exists(dosya):
            try:
                if platform.system() == "Linux":
                    subprocess.Popen(["mpg123", "-q", dosya])
                elif platform.system() == "Windows":
                    os.startfile(dosya)
            except Exception as e:
                print(f"Ses çalma hatası: {e}")

    def arka_plan_dongusu(self):
        while True:
            simdi = datetime.now()
            self.lbl_saat.configure(text=simdi.strftime("%H:%M:%S"))
            time.sleep(1)


if __name__ == "__main__":
    app = AnaEkran()
    app.mainloop()