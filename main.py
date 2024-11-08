import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector as mysql
from dataclasses import dataclass
from typing import List
try:
    import tkcalendar as tkc
except ImportError:
    tkc = None

@dataclass
class DBConfig:
    host: str = "localhost"
    user: str = "root"
    password: str = ""
    database: str = "arabaotomasyonu"

class AracOtomasyonu:
    def __init__(self):
        self.setup_database()
        self.setup_ui()
        self.pencere.mainloop()

    def setup_database(self):
        try:
            self.db = mysql.connect(
                host=DBConfig.host,
                user=DBConfig.user,
                password=DBConfig.password
            )
            self.cursor = self.db.cursor()
            self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DBConfig.database}")
            self.cursor.execute(f"USE {DBConfig.database}")
            self.create_tables()
        except mysql.Error as err:
            messagebox.showerror("Hata", f"MySQL bağlantısı kurulamadı: {err}")
            exit(1)

    def create_tables(self):
        tables = {
            "musteribilgileri": """
                CREATE TABLE IF NOT EXISTS musteribilgileri (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    ad VARCHAR(255),
                    soyad VARCHAR(255),
                    tcNo VARCHAR(11),
                    dogumTarihi DATE,
                    adres VARCHAR(255),
                    telefonNo VARCHAR(15),
                    meslek VARCHAR(255),
                    ehliyet VARCHAR(10),
                    medeniHal VARCHAR(20),
                    egitim VARCHAR(50)
                )
            """,
            "arababilgileri": """
                CREATE TABLE IF NOT EXISTS arababilgileri (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    marka VARCHAR(255),
                    model VARCHAR(255),
                    uretimYili INT(4),
                    yakitTuru VARCHAR(50),
                    vites VARCHAR(20),
                    motorGucu INT(5),
                    kasaTipi VARCHAR(50),
                    motorHacmi INT(5),
                    cekisTuru VARCHAR(50),
                    kapiSayisi INT(2),
                    renk VARCHAR(50),
                    motorNo VARCHAR(50),
                    sasiNo VARCHAR(50),
                    gunlukKiralamaUcreti DECIMAL(10,2) DEFAULT 100,
                    kiradaMi BOOLEAN DEFAULT FALSE,
                    kullanimDisi BOOLEAN DEFAULT FALSE
                )
            """,
            "kiralamabilgileri": """
                CREATE TABLE IF NOT EXISTS kiralamabilgileri (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    musteri_id INT,
                    araba_id INT,
                    kiralamaSuresi INT,
                    nereyeGidecek VARCHAR(255),
                    ucret DECIMAL(10,2),
                    FOREIGN KEY (musteri_id) REFERENCES musteribilgileri(id),
                    FOREIGN KEY (araba_id) REFERENCES arababilgileri(id)
                )
            """
        }
        for table_sql in tables.values():
            self.cursor.execute(table_sql)

    def setup_ui(self):
        self.pencere = tk.Tk()
        self.pencere.title("Araç Otomasyon Programı - V1.0 - By: Hamza ORTATEPE")
        self.pencere.configure(bg="#353535")
        self.pencere.geometry("940x600")
        self.pencere.resizable(False, False)

        self.create_menu()
        # BAşlık
        tk.Label(
            self.pencere,
            text="Araç Otomasyon Programı",
            font=("Helvetica 20 bold"),
            bg="#353535",
            fg="white"
        ).grid(row=0, column=0, columnspan=4, pady=20)
        self.create_main_buttons()

    def create_menu(self):
        menu = tk.Menu(self.pencere)
        self.pencere.config(menu=menu)

        yardım_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Yardım", menu=yardım_menu)
        yardım_menu.add_command(label="Nasıl çalışır", command=self.help_page)
        yardım_menu.add_command(label="Hakkında", command=self.about_page)
        yardım_menu.add_separator()
        yardım_menu.add_command(label="Çıkış", command=self.pencere.quit)

        veritabani_menu = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Veritabanı", menu=veritabani_menu)
        veritabani_menu.add_command(label="Müşteri Veritabanı", command=self.kayitli_musterileri_goruntule)
        veritabani_menu.add_command(label="Araba Veritabanı", command=self.kayitli_arabalari_goruntule)

    def create_main_buttons(self):
        btn_info = [
            ("Müşteri Kayıt", self.musteri_bilgileri_ekrani),
            ("Araba Kayıt", self.araba_bilgileri_ekrani),
            ("Araç Kiralama", self.arac_kiralama_ekrani),
            ("Kirada Olan Araçlar", self.kirada_olan_araclar_ekrani)
        ]
        for idx, (text, command) in enumerate(btn_info):
            tk.Button(
                self.pencere,
                text=text,
                width=25,
                height=8,
                command=command,
                font="Helvetica 10 bold",
                bg="white",
                fg="black",
                borderwidth=5
            ).grid(row=10, column=idx, pady=150, padx=10)

    def musteri_bilgileri_ekrani(self):
        self.musteri_kayit = tk.Toplevel(self.pencere)
        self.musteri_kayit.title("Müşteri Kayıt")
        self.musteri_kayit.configure(bg="#3c6e71")
        self.musteri_kayit.geometry("500x600")
        self.musteri_kayit.resizable(False, False)

        labels = [
            "Müşteri Adı", "Müşteri Soyadı", "Müşteri TC",
            "Doğum Tarihi", "Adres", "Telefon No",
            "Meslek", "Ehliyet Sınıfı", "Medeni Hali", "Eğitim Durumu"
        ]
        self.musteri_entries = {}
        for idx, label in enumerate(labels):
            tk.Label(
                self.musteri_kayit,
                text=f"{label}:",
                font=("Helvetica 10 bold"),
                bg="#3c6e71",
                fg="white"
            ).grid(row=idx+1, column=0, padx=20, pady=5, sticky="e")
            entry = tk.Entry(self.musteri_kayit)
            entry.grid(row=idx+1, column=1, pady=5)
            self.musteri_entries[label] = entry

        tk.Button(
            self.musteri_kayit,
            text="Müşteri Kaydı Tamamla",
            command=self.musteri_verilerini_taboya_gonder,
            font=("Helvetica 10 bold"),
            bg="white",
            fg="#3c6e71",
            width=50
        ).grid(row=12, column=0, columnspan=2, pady=10)

    def musteri_verilerini_taboya_gonder(self):
        data = {k: v.get() for k, v in self.musteri_entries.items()}
        try:
            sql = """
                INSERT INTO musteribilgileri
                (ad, soyad, tcNo, dogumTarihi, adres, telefonNo, meslek, ehliyet, medeniHal, egitim)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = tuple(data.values())
            self.cursor.execute(sql, values)
            self.db.commit()
            messagebox.showinfo("Başarılı", "Müşteri kaydı tamamlandı.")
            self.musteri_kayit.destroy()
        except mysql.Error as err:
            messagebox.showerror("Hata", f"Kayıt başarısız: {err}")

    def araba_bilgileri_ekrani(self):
        self.araba_kayit = tk.Toplevel(self.pencere)
        self.araba_kayit.title("Araba Kayıt")
        self.araba_kayit.configure(bg="#3c6e71")
        self.araba_kayit.geometry("500x600")
        self.araba_kayit.resizable(False, False)

        labels = [
            "Marka", "Model", "Üretim Yılı", "Yakıt Türü", "Vites",
            "Motor Gücü", "Kasa Tipi", "Motor Hacmi", "Çekiş Türü",
            "Kapı Sayısı", "Renk", "Motor No", "Şasi No",
            "Günlük Kiralama Ücreti"
        ]
        self.araba_entries = {}
        for idx, label in enumerate(labels):
            tk.Label(
                self.araba_kayit,
                text=f"{label}:",
                font=("Helvetica 10 bold"),
                bg="#3c6e71",
                fg="white"
            ).grid(row=idx+1, column=0, padx=20, pady=5, sticky="e")
            entry = tk.Entry(self.araba_kayit)
            entry.grid(row=idx+1, column=1, pady=5)
            self.araba_entries[label] = entry

        tk.Button(
            self.araba_kayit,
            text="Araba Kaydı Tamamla",
            command=self.araba_verilerini_taboya_gonder,
            font=("Helvetica 10 bold"),
            bg="white",
            fg="#3c6e71",
            width=50
        ).grid(row=16, column=0, columnspan=2, pady=10)

    def araba_verilerini_taboya_gonder(self):
        data = {k: v.get() for k, v in self.araba_entries.items()}
        try:
            sql = """
                INSERT INTO arababilgileri
                (marka, model, uretimYili, yakitTuru, vites, motorGucu, kasaTipi, motorHacmi, cekisTuru, kapiSayisi, renk, motorNo, sasiNo, gunlukKiralamaUcreti)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = tuple(data.values())
            self.cursor.execute(sql, values)
            self.db.commit()
            messagebox.showinfo("Başarılı", "Araba kaydı tamamlandı.")
            self.araba_kayit.destroy()
        except mysql.Error as err:
            messagebox.showerror("Hata", f"Kayıt başarısız: {err}")

    def arac_kiralama_ekrani(self):
        self.kiralama_ekrani = tk.Toplevel(self.pencere)
        self.kiralama_ekrani.title("Araç Kiralama")
        self.kiralama_ekrani.configure(bg="#3c6e71")
        self.kiralama_ekrani.geometry("400x300")
        self.kiralama_ekrani.resizable(False, False)

        tk.Label(
            self.kiralama_ekrani,
            text="Müşteri Seçin:",
            font=("Helvetica 10 bold"),
            bg="#3c6e71",
            fg="white"
        ).grid(row=0, column=0, padx=20, pady=10)
        self.musteri_secim = ttk.Combobox(self.kiralama_ekrani, values=self.get_musteri_listesi(), width=25)
        self.musteri_secim.grid(row=0, column=1, pady=10)

        tk.Label(
            self.kiralama_ekrani,
            text="Araba Seçin:",
            font=("Helvetica 10 bold"),
            bg="#3c6e71",
            fg="white"
        ).grid(row=1, column=0, padx=20, pady=10)
        self.araba_secim = ttk.Combobox(self.kiralama_ekrani, values=self.get_araba_listesi(), width=25)
        self.araba_secim.grid(row=1, column=1, pady=10)

        tk.Label(
            self.kiralama_ekrani,
            text="Kiralama Süresi (gün):",
            font=("Helvetica 10 bold"),
            bg="#3c6e71",
            fg="white"
        ).grid(row=2, column=0, padx=20, pady=10)
        self.kiralama_suresi = tk.Entry(self.kiralama_ekrani)
        self.kiralama_suresi.grid(row=2, column=1, pady=10)

        tk.Button(
            self.kiralama_ekrani,
            text="Kiralamayı Tamamla",
            command=self.kiralama_islemi,
            font=("Helvetica 10 bold"),
            bg="white",
            fg="#3c6e71",
            width=30
        ).grid(row=3, column=0, columnspan=2, pady=20)

    def kiralama_islemi(self):
        musteri_id = self.get_musteri_id(self.musteri_secim.get())
        araba_id = self.get_araba_id(self.araba_secim.get())
        sure = int(self.kiralama_suresi.get())
        ucret = self.get_araba_ucreti(araba_id) * sure
        try:
            sql = """
                INSERT INTO kiralamabilgileri (musteri_id, araba_id, kiralamaSuresi, ucret)
                VALUES (%s, %s, %s, %s)
            """
            self.cursor.execute(sql, (musteri_id, araba_id, sure, ucret))
            self.db.commit()
            messagebox.showinfo("Başarılı", "Araç kiralama tamamlandı.")
            self.kiralama_ekrani.destroy()
        except mysql.Error as err:
            messagebox.showerror("Hata", f"İşlem başarısız: {err}")

    def get_musteri_listesi(self) -> List[str]:
        self.cursor.execute("SELECT id, CONCAT(ad, ' ', soyad) FROM musteribilgileri")
        return [f"{row[0]} - {row[1]}" for row in self.cursor.fetchall()]

    def get_araba_listesi(self) -> List[str]:
        self.cursor.execute("SELECT id, marka FROM arababilgileri WHERE kiradaMi=0 AND kullanimDisi=0")
        return [f"{row[0]} - {row[1]}" for row in self.cursor.fetchall()]

    def get_musteri_id(self, selection: str) -> int:
        return int(selection.split(" - ")[0])

    def get_araba_id(self, selection: str) -> int:
        return int(selection.split(" - ")[0])

    def get_araba_ucreti(self, araba_id: int) -> float:
        self.cursor.execute("SELECT gunlukKiralamaUcreti FROM arababilgileri WHERE id=%s", (araba_id,))
        return self.cursor.fetchone()[0]

    def kirada_olan_araclar_ekrani(self):
        """Kirada olan araçları listeler"""
        pencere = tk.Toplevel(self.pencere)
        pencere.title("Kirada Olan Araçlar")
        pencere.configure(bg="#3c6e71")
        pencere.geometry("800x400")
        pencere.resizable(False, False)

        columns = ("ID", "Marka", "Model", "Kiralama Süresi", "Müşteri")
        tree = ttk.Treeview(pencere, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        tree.pack(fill=tk.BOTH, expand=True)

        sql = """
            SELECT ar.id, ar.marka, ar.model, kir.kiralamaSuresi, CONCAT(m.ad, ' ', m.soyad)
            FROM arababilgileri ar
            JOIN kiralamabilgileri kir ON ar.id = kir.araba_id
            JOIN musteribilgileri m ON kir.musteri_id = m.id
            WHERE ar.kiradaMi = TRUE
        """
        self.cursor.execute(sql)
        for row in self.cursor.fetchall():
            tree.insert("", "end", values=row)

    def kayitli_musterileri_goruntule(self):
        """Kayıtlı müşterileri listeler"""
        pencere = tk.Toplevel(self.pencere)
        pencere.title("Kayıtlı Müşteriler")
        pencere.configure(bg="#3c6e71")
        pencere.geometry("800x400")
        pencere.resizable(False, False)

        columns = ("ID", "Ad", "Soyad", "Telefon No", "Adres")
        tree = ttk.Treeview(pencere, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        tree.pack(fill=tk.BOTH, expand=True)

        self.cursor.execute("SELECT id, ad, soyad, telefonNo, adres FROM musteribilgileri")
        for row in self.cursor.fetchall():
            tree.insert("", "end", values=row)

    def kayitli_arabalari_goruntule(self):
        """Kayıtlı arabaları listeler"""
        pencere = tk.Toplevel(self.pencere)
        pencere.title("Kayıtlı Arabalar")
        pencere.configure(bg="#3c6e71")
        pencere.geometry("800x400")
        pencere.resizable(False, False)

        columns = ("ID", "Marka", "Model", "Üretim Yılı", "Durum")
        tree = ttk.Treeview(pencere, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150)
        tree.pack(fill=tk.BOTH, expand=True)

        self.cursor.execute("SELECT id, marka, model, uretimYili, kiradaMi FROM arababilgileri")
        for row in self.cursor.fetchall():
            durum = "Kirada" if row[4] else "Müsait"
            tree.insert("", "end", values=(row[0], row[1], row[2], row[3], durum))

    def help_page(self):
        """Yardım sayfasını gösterir"""
        mesaj = ("Bu araç kiralama otomasyon programı ile müşterileri ve araçları kaydedebilir, "
                "araç kiralama işlemleri yapabilir ve mevcut kayıtları görüntüleyebilirsiniz.")
        messagebox.showinfo("Nasıl Çalışır", mesaj)

    def about_page(self):
        """Hakkında sayfasını gösterir"""
        mesaj = "Versiyon 1.0\nGeliştirici: Hamza ORTATEPE"
        messagebox.showinfo("Hakkında", mesaj)

if __name__ == "__main__":
    otomasyon = AracOtomasyonu()