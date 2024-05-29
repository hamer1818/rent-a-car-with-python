import tkinter as tk
import mysql.connector as mysql     
from tkinter import ttk            
from tkinter import messagebox
try:
    import tkcalendar as tkc
except:
    pass

class aracOtomasyonu():

    def __init__(self):
        # halihazırda bir veritabanınmız olmadığı için mysql e root kullanıcı adı ile bağlanıyoruz bu sayede mysql de bir veritabanı oluşturabiliriz
        try:
            self.mysqlConn = mysql.connect(
            host = "localhost",
            user = "root",
            password = "")
        except:
            messagebox.showerror("Hata","Mysql bağlantısı kurulamadı\n Lütfen mysql sunucusunu başlatın")
        self.mysqlCursor = self.mysqlConn.cursor()
        self.veriTabaniOlsutur()
        self.musteriTabloOlustur()
        self.arabaTabloOlustur()
        self.kiralamaTabloOlustur()
        self.kullaniciTabloOlustur()
        


        self.pencere = tk.Tk()
        self.pencere.title("Araç Otomasyon Programı - V1.0 - By: Hamza ORTATEPE")
        self.pencere.configure(background="#353535")
        self.pencere.geometry("940x600")
        self.pencere.resizable(False, False)
        # mysql baglantisi yapiliyor
        # self.anaEkran()
        self.girisVeKayitEkran()
        # self.musteriBilgileriniTablodanAl()
        # self.arabaBilgileriniTablodanAl()
        self.pencere.mainloop()

    def girisVeKayitEkran(self):
        "Giriş ve Kayıt ekranı"

        self.girisEkrani = tk.Toplevel(self.pencere)
        self.girisEkrani.title("Giriş ve Kayıt Ekranı")
        self.girisEkrani.configure(background="#3c6e71")
        self.girisEkrani.geometry("500x300")
        self.girisEkrani.resizable(False, False)
        self.girisEkrani.protocol("WM_DELETE_WINDOW",self.pencere.quit)
        # en üst level pencere olsun
        self.girisEkrani.attributes("-topmost", True)

        self.kullaniciAdiLabel = tk.Label(self.girisEkrani, text = "Kullanıcı Adı:",font=("Helvetica 10 bold"),background="#3c6e71",foreground="white")
        self.kullaniciAdiLabel.grid(row=10, column=0,padx=80)
        self.kullaniciAdiEntry = tk.Entry(self.girisEkrani)
        self.kullaniciAdiEntry.grid(row=10, column=1,pady=10)

        self.sifreLabel = tk.Label(self.girisEkrani, text = "Şifre:",font=("Helvetica 10 bold"),background="#3c6e71",foreground="white")
        self.sifreLabel.grid(row=11, column=0)
        self.sifreEntry = tk.Entry(self.girisEkrani,show="*")
        self.sifreEntry.grid(row=11, column=1,pady=10)

        self.girisYapButon = tk.Button(self.girisEkrani, text = "Giriş Yap",command=self.girisYap,font=("Helvetica 10 bold"),background="white",foreground="#3c6e71",width=20)
        self.girisYapButon.grid(row=12, column=0,columnspan=2,pady=5)

        self.kayitOlButon = tk.Button(self.girisEkrani, text = "Kayıt Ol",command=self.kayitOl,font=("Helvetica 10 bold"),background="white",foreground="#3c6e71",width=20)
        self.kayitOlButon.grid(row=13, column=0,columnspan=2,pady=5)
        

        

    def girisYap(self):
        "giriş yapma fonksiyonu"
        
        self.kullaniciAdi = self.kullaniciAdiEntry.get()
        self.sifre = self.sifreEntry.get()
        try:
            self.mysqlCursor.execute("USE arabakiralamadb")
            self.mysqlCursor.execute("SELECT * FROM kullanicibilgileri WHERE kullaniciAdi = %s AND sifre = %s",(self.kullaniciAdi,self.sifre))
            self.kullaniciVerileri = self.mysqlCursor.fetchall()
            if len(self.kullaniciVerileri) > 0:
                self.girisEkrani.destroy()
                self.anaEkran()
                self.musteriBilgileriniTablodanAl()
                self.arabaBilgileriniTablodanAl()
            else:
                messagebox.showerror("Hata","Kullanıcı adı veya şifre hatalı")
        except:
            messagebox.showerror("Hata","Kullanıcı adı veya şifre hatalı")
    
    

    def kayitOl(self):
        "kayıt olma fonksiyonu"
        self.kullaniciAdi = self.kullaniciAdiEntry.get()
        self.sifre = self.sifreEntry.get()
        try:
            self.mysqlCursor.execute("USE arabakiralamadb")
            self.mysqlCursor.execute("INSERT INTO kullanicibilgileri (kullaniciAdi,sifre) VALUES (%s,%s)",(self.kullaniciAdi,self.sifre))
            self.mysqlConn.commit()
            messagebox.showinfo("Başarılı","Kayıt başarılı")
        except:
            messagebox.showerror("Hata","Kayıt başarısız")

  
    def anaEkran(self):
        # menu çubuğu oluşturup verilere daha kolay ulaşılmasını sağladım ve programın çalışma mantığını anlattım
        menu = tk.Menu(self.pencere)
        self.pencere.config(menu=menu)

        # Menü çubuğuna birkaç menü ekle
        file_menu = tk.Menu(menu)
        menu.add_cascade(label="Yardım", menu=file_menu)
        file_menu.add_command(label="Nasıl çalışır", command=lambda: self.helpPager())
        file_menu.add_command(label="Hakkında", command=lambda: self.about())
        file_menu.add_separator()
        file_menu.add_command(label="Çıkış", command=self.pencere.quit)

        # Menü çubuğuna birkaç menü daha ekle
        edit_menu = tk.Menu(menu)
        menu.add_cascade(label="Veritabanı", menu=edit_menu)
        edit_menu.add_command(label="Müşteri Veritabanı", command=lambda: self.kayitliMusterileriGoruntule(self.pencere))
        edit_menu.add_command(label="Araba Veritabanı", command=lambda: self.kayitliArabalariGoruntule(self.pencere))


        # edit_menu.add_command(label="Veritabanlarını temizle!!",command=self.veritabanınıTemizle)

        "ana ekranın amacı ana ekranda butonlar oluşturmak ve butonlara fonksiyonları atamak"
        self.anaEkranBaslik = tk.Label(self.pencere, text = "Araç Kiralama Otomasyonu",font=("Broadway 25 bold underline"),bg="#353535",fg="white")
        self.anaEkranBaslik.grid(row=0, column=0,columnspan=4,pady=20,padx=10)

        self.musteriBilgileri = tk.Button(self.pencere, text = "Müşteri Kayıt",width=25,height=8,command=self.musteriBilgileriEkrani,font="Helvetica 10 bold",bg="white",fg="black",borderwidth=5)
        self.musteriBilgileri.grid(row=10, column=0,pady=150,padx=10)

        self.arabaBilgileri = tk.Button(self.pencere, text = "Araba Kayıt",width=25,height=8,command=self.arabaBilgileriEkran,font="Helvetica 10 bold",bg="white",fg="black",borderwidth=5)
        self.arabaBilgileri.grid(row=10, column=1,padx=10)

        self.aracKiralamaBilgileri = tk.Button(self.pencere, text = "Araç Kiralama",width=25,height=8,command=self.aracKiralamaEkran,font="Helvetica 10 bold",bg="white",fg="black",borderwidth=5)
        self.aracKiralamaBilgileri.grid(row=10, column=2,padx=10)

        self.kiradaOlanAraclariGoruntuler = tk.Button(self.pencere, text = "Kirada Olan Araçları Görüntüle",width=25,height=8,font="Helvetica 10 bold",bg="white",fg="black",borderwidth=5,command=self.kiradaOlanAraclarinListesiEkran)
        self.kiradaOlanAraclariGoruntuler.grid(row=10, column=3,padx=10)

        self.aramaEkraniAc = tk.Button(self.pencere, text = "Arama Ekranı",font="Helvetica 10 bold",bg="white",fg="black",borderwidth=5,command=self.aramaEkrani)
        self.aramaEkraniAc.place(x=830,y=10)

    def musteriBilgileriEkrani(self):
        "Müşteri Bilgileri ekranı amacı Müşteri Bilgilerini kaydetmek"
        self.musterikayit = tk.Toplevel(self.pencere)
        self.musterikayit.title("Müşteri Kayıt")
        self.musterikayit.configure(background="#3c6e71")
        self.musterikayit.geometry("500x600")
        self.musterikayit.resizable(False, False)
        
        self.musteriBilgileriEkraniBaslik = tk.Label(self.musterikayit, text = "Müşteri Bilgileri",font=("Broadway 25 bold underline"),bg="#3c6e71",fg="white",width=15,height=2)
        self.musteriBilgileriEkraniBaslik.grid(row=0, column=0,columnspan=2,padx=50)

        self.musteriAdi = tk.Label(self.musterikayit, text = "Müşteri Adı:",font=("Helvetica 10 bold"),background="#3c6e71",foreground="white")
        self.musteriAdi.grid(row=10, column=0,padx=80)
        self.musteriAdiEntry = tk.Entry(self.musterikayit)
        self.musteriAdiEntry.grid(row=10, column=1,pady=10)

        self.musteriSoyAdi = tk.Label(self.musterikayit, text = "Müşteri Soyadı:",font=("Helvetica 10 bold"),background="#3c6e71",foreground="white")
        self.musteriSoyAdi.grid(row=11, column=0)
        self.musteriSoyAdiEntry = tk.Entry(self.musterikayit)
        self.musteriSoyAdiEntry.grid(row=11, column=1,pady=10)

        self.musteriTC = tk.Label(self.musterikayit, text = "Müşteri TC:",font=("Helvetica 10 bold"),background="#3c6e71",foreground="white")
        self.musteriTC.grid(row=12, column=0)
        self.musteriTCEntry = tk.Entry(self.musterikayit)
        self.musteriTCEntry.grid(row=12, column=1,pady=10)
        self.musteriTCEntry.config(width=11)

        self.musteriDogumTarihi = tk.Label(self.musterikayit, text = "Müşteri Doğum Tarihi:",font=("Helvetica 10 bold"),background="#3c6e71",foreground="white")
        self.musteriDogumTarihi.grid(row=13, column=0)
        try: 
            self.musteriDogumTarihiEntry = tkc.DateEntry(self.musterikayit, width=12, background='darkblue',foreground='white', borderwidth=2, year=2023)
        except:
            self.musteriDogumTarihiEntry = tk.Entry(self.musterikayit)

        self.musteriDogumTarihiEntry.grid(row=13, column=1,pady=10)
        self.musteriDogumTarihiEntry.config(width=10)

        self.musteriAdresi = tk.Label(self.musterikayit, text = "Müşteri Adresi:",font=("Helvetica 10 bold"),background="#3c6e71",foreground="white")
        self.musteriAdresi.grid(row=14, column=0)
        self.musteriAdresiEntry = tk.Entry(self.musterikayit)
        self.musteriAdresiEntry.grid(row=14, column=1,pady=10)

        self.musteriTelefonNo = tk.Label(self.musterikayit, text = "Müşteri Telefon No:",font=("Helvetica 10 bold"),background="#3c6e71",foreground="white")
        self.musteriTelefonNo.grid(row=15, column=0)
        self.musteriTelefonNoEntry = tk.Entry(self.musterikayit)
        self.musteriTelefonNoEntry.grid(row=15, column=1,pady=10)
        self.musteriTelefonNoEntry.config(width=11)

        self.musteriMeslegi = tk.Label(self.musterikayit, text = "Müşteri Mesleği:",font=("Helvetica 10 bold"),background="#3c6e71",foreground="white")
        self.musteriMeslegi.grid(row=16, column=0)
        self.musteriMeslegiEntry = tk.Entry(self.musterikayit)
        self.musteriMeslegiEntry.grid(row=16, column=1,pady=10)

        self.musteriEhliyetSinifi = tk.Label(self.musterikayit, text = "Müşteri Ehliyet Sınıfı:",font=("Helvetica 10 bold"),background="#3c6e71",foreground="white")
        self.musteriEhliyetSinifi.grid(row=17, column=0)
        self.musteriEhliyetSinifiEntry = tk.Entry(self.musterikayit)
        self.musteriEhliyetSinifiEntry.grid(row=17, column=1,pady=10)

        self.musteriMedeniHali = tk.Label(self.musterikayit, text = "Müşteri Medeni Hali:",font=("Helvetica 10 bold"),background="#3c6e71",foreground="white")
        self.musteriMedeniHali.grid(row=18, column=0)
        self.musteriMedeniHaliEntry = tk.Entry(self.musterikayit)
        self.musteriMedeniHaliEntry.grid(row=18, column=1,pady=10)

        self.musteriEgitimDurumu = tk.Label(self.musterikayit, text = "Müşteri Eğitim Durumu:",font=("Helvetica 10 bold"),background="#3c6e71",foreground="white")
        self.musteriEgitimDurumu.grid(row=19, column=0)
        self.musteriEgitimDurumuEntry = tk.Entry(self.musterikayit)
        self.musteriEgitimDurumuEntry.grid(row=19, column=1,pady=10)

        self.musteriKaydiTamamla = tk.Button(self.musterikayit, text = "Müşteri Kaydı Tamamla",command=self.musteriVerileriniTabloyaGonder,font=("Helvetica 10 bold"),background="white",foreground="#3c6e71",width=50)
        self.musteriKaydiTamamla.grid(row=20, column=0,columnspan=2,pady=5)

        self.kayitliMusterilereBak = tk.Button(self.musterikayit, text = "Kayıtlı Müşterilere Bak",command=lambda pencere=self.musterikayit: self.kayitliMusterileriGoruntule(pencere),font=("Helvetica 10 bold"),background="white",foreground="#3c6e71",width=50)
        self.kayitliMusterilereBak.grid(row=21, column=0,columnspan=2,pady=5)
    
    def arabaBilgileriEkran(self):
        "araba bilgileri ekranının amacı araba bilgilerini girip kaydetmek"
        self.aracBilgileri = tk.Toplevel(self.pencere)
        self.aracBilgileri.title("Araç Bilgileri")
        self.aracBilgileri.geometry("370x600")
        self.aracBilgileri.configure(background="#3c6e71")
        self.aracBilgileri.resizable(False, False)
        
        self.aracBilgileriBaslik = tk.Label(self.aracBilgileri, text = "Araç Bilgileri",font=("Broadway 25 bold underline"),bg="#3c6e71",fg="white",width=15,height=2)
        self.aracBilgileriBaslik.grid(row=0, column=0,columnspan=2)
        
        self.aracTuru = tk.Label(self.aracBilgileri, text = "Araç Türü :",font=("Helvetica 10 bold"),background="#3c6e71",foreground="white")
        self.aracTuru.grid(row=10, column=0)
        self.aracTuruEntry = tk.Entry(self.aracBilgileri)
        self.aracTuruEntry.grid(row=10, column=1)

        self.marka = tk.Label(self.aracBilgileri, text = "Marka :",font=("Helvetica 10 bold"),background="#3c6e71",foreground="white")
        self.marka.grid(row=11, column=0)
        self.markaEntry = tk.Entry(self.aracBilgileri)
        self.markaEntry.grid(row=11, column=1)

        self.aracModeli = tk.Label(self.aracBilgileri, text = "Araç Modeli :",font=("Helvetica 10 bold"),background="#3c6e71",foreground="white")
        self.aracModeli.grid(row=12, column=0)
        self.aracModeliEntry = tk.Entry(self.aracBilgileri)
        self.aracModeliEntry.grid(row=12, column=1)

        self.uretimYili = tk.Label(self.aracBilgileri, text = "Üretim Yılı :",font=("Helvetica 10 bold"),background="#3c6e71",foreground="white")
        self.uretimYili.grid(row=13, column=0)
        self.uretimYiliEntry = tk.Entry(self.aracBilgileri)
        self.uretimYiliEntry.grid(row=13, column=1)
        self.uretimYiliEntry.config(width=10)

        self.yakitTuru = tk.Label(self.aracBilgileri, text = "Yakıt Türü :",font=("Helvetica 10 bold"),background="#3c6e71",foreground="white")
        self.yakitTuru.grid(row=14, column=0)
        self.yakitTuruEntry = tk.Entry(self.aracBilgileri)
        self.yakitTuruEntry.grid(row=14, column=1)

        self.vites = tk.Label(self.aracBilgileri, text = "Vites :",font=("Helvetica 10 bold"),background="#3c6e71",foreground="white")
        self.vites.grid(row=15, column=0)
        self.vitesEntry = tk.Entry(self.aracBilgileri)
        self.vitesEntry.grid(row=15, column=1)

        self.motorGucu = tk.Label(self.aracBilgileri, text = "Motor Gücü :",font=("Helvetica 10 bold"),background="#3c6e71",foreground="white")
        self.motorGucu.grid(row=16, column=0)
        self.motorGucuEntry = tk.Entry(self.aracBilgileri)
        self.motorGucuEntry.grid(row=16, column=1)

        self.kasaTipi = tk.Label(self.aracBilgileri, text = "Kasa Tipi :",font=("Helvetica 10 bold"),background="#3c6e71",foreground="white")
        self.kasaTipi.grid(row=17, column=0)
        self.kasaTipiEntry = tk.Entry(self.aracBilgileri)
        self.kasaTipiEntry.grid(row=17, column=1)

        self.motoHacmi = tk.Label(self.aracBilgileri, text = "Motor Hacmi :",font=("Helvetica 10 bold"),background="#3c6e71",foreground="white")
        self.motoHacmi.grid(row=18, column=0)
        self.motoHacmiEntry = tk.Entry(self.aracBilgileri)
        self.motoHacmiEntry.grid(row=18, column=1)

        self.cekisTuru = tk.Label(self.aracBilgileri, text = "Çekiş Türü :",font=("Helvetica 10 bold"),background="#3c6e71",foreground="white")
        self.cekisTuru.grid(row=19, column=0)
        self.cekisTuruEntry = tk.Entry(self.aracBilgileri)
        self.cekisTuruEntry.grid(row=19, column=1)

        self.kapiSayisi = tk.Label(self.aracBilgileri, text = "Kapı Sayısı :",font=("Helvetica 10 bold"),background="#3c6e71",foreground="white")
        self.kapiSayisi.grid(row=20, column=0)
        self.kapiSayisiEntry = tk.Entry(self.aracBilgileri)
        self.kapiSayisiEntry.grid(row=20, column=1)

        self.renk = tk.Label(self.aracBilgileri, text = "Renk :",font=("Helvetica 10 bold"),background="#3c6e71",foreground="white")
        self.renk.grid(row=21, column=0)
        self.renkEntry = tk.Entry(self.aracBilgileri)
        self.renkEntry.grid(row=21, column=1)

        self.motorNo = tk.Label(self.aracBilgileri, text = "Motor No :",font=("Helvetica 10 bold"),background="#3c6e71",foreground="white")
        self.motorNo.grid(row=22, column=0)
        self.motorNoEntry = tk.Entry(self.aracBilgileri)
        self.motorNoEntry.grid(row=22, column=1)

        self.sasiNo = tk.Label(self.aracBilgileri, text = "Şasi No :",font=("Helvetica 10 bold"),background="#3c6e71",foreground="white")
        self.sasiNo.grid(row=23, column=0)
        self.sasiNoEntry = tk.Entry(self.aracBilgileri)
        self.sasiNoEntry.grid(row=23, column=1)

        self.gunlukKiralamaucreti = tk.Label(self.aracBilgileri, text = "Günlük Kiralama ücreti :",font=("Helvetica 10 bold"),background="#3c6e71",foreground="white")
        self.gunlukKiralamaucreti.grid(row=24, column=0)
        self.gunlukKiralamaucretiEntry = tk.Entry(self.aracBilgileri)
        self.gunlukKiralamaucretiEntry.grid(row=24, column=1)

        self.kiradaMi = tk.Label(self.aracBilgileri, text = "Kirada mı :",font=("Helvetica 10 bold"),background="#3c6e71",foreground="white")
        self.kiradaMi.grid(row=25, column=0)
        self.kiradaMiEntry = tk.Entry(self.aracBilgileri)
        self.kiradaMiEntry.grid(row=25, column=1)

        self.kullanimDisiMi = tk.Label(self.aracBilgileri, text = "Kullanım Dışı mı :",font=("Helvetica 10 bold"),background="#3c6e71",foreground="white")
        self.kullanimDisiMi.grid(row=26, column=0)
        self.kullanimDisiMiEntry = tk.Entry(self.aracBilgileri)
        self.kullanimDisiMiEntry.grid(row=26, column=1)

        self.aracBilgileriniTamamla = tk.Button(self.aracBilgileri, text = "Araç Bilgilerini Tamamla",command=self.arabaBilgileriniTabloyaGonder,font=("Helvetica 10 bold"),background="white",foreground="#3c6e71",width=40)
        self.aracBilgileriniTamamla.grid(row=27, column=0, columnspan=2,pady=5)

        self.kayitliArabalaraBak = tk.Button(self.aracBilgileri, text = "Kayıtlı Arabalara Bak",command=lambda pencere=self.aracBilgileri: self.kayitliArabalariGoruntule(pencere),font=("Helvetica 10 bold"),background="white",foreground="#3c6e71",width=40)
        self.kayitliArabalaraBak.grid(row=28, column=0, columnspan=2,pady=5)

    def aracKiralamaEkran(self):
        "araç kiralama ekranının amacı veritabanındaki müşterileri ve araçları seçip kiralama işlemini gerçekleştirmektir."
        self.aracKiralamaEkrani = tk.Toplevel(self.pencere)
        self.aracKiralamaEkrani.title("Araç Kiralama Ekranı")
        self.aracKiralamaEkrani.configure(background="#3c6e71")
        self.aracKiralamaEkrani.geometry("420x450")
        self.aracKiralamaEkrani.resizable(False, False)

        menu = tk.Menu(self.aracKiralamaEkrani)
        kiraYardimMenu = tk.Menu(menu)
        self.aracKiralamaEkrani.config(menu=menu)

        menu.add_cascade(label="Verileri veri tabanına kaydettiğinde gelmiyorsa veritabanı bağlantısı yenile", menu=kiraYardimMenu)
        # kiraYardimMenu.add_command(label="Araç Kiralamadan önce bunu oku", command=self.aracKiralamaYardimSayfasi)

        self.aracKiralamaEkraniBaslik = tk.Label(self.aracKiralamaEkrani, text="Araç Kiralama Ekranı",font=("Broadway 20 bold underline"),bg="#3c6e71",fg="white",height=2)
        self.aracKiralamaEkraniBaslik.grid(row=0, column=0, columnspan=2,pady=10,padx=30)

        self.musteriSecim = tk.Label(self.aracKiralamaEkrani, text = "Müşteri Seçim",font=("Helvetica 10 bold"),background="#3c6e71",foreground="white")
        self.musteriSecim.grid(row=10, column=0,padx=30)
        self.musteriSecimCombobox = ttk.Combobox(self.aracKiralamaEkrani,values=self.musteriBilgileriListe,width=30)
        self.musteriSecimCombobox.grid(row=10,column=1,pady=10)

        self.arabaSecim = tk.Label(self.aracKiralamaEkrani, text="Araba Seçim",font=("Helvetica 10 bold"),background="#3c6e71",foreground="white")
        self.arabaSecim.grid(row=11, column=0)
        self.arabaSecimCombobox = ttk.Combobox(self.aracKiralamaEkrani,values=self.arabaBilgileriListe,width=30)
        self.arabaSecimCombobox.grid(row=11, column=1,pady=10)

        self.KacGunKiralanacak = tk.Label(self.aracKiralamaEkrani, text="Kaç Gün Kiralanacak",font=("Helvetica 10 bold"),background="#3c6e71",foreground="white")
        self.KacGunKiralanacak.grid(row=12, column=0)
        self.KacGunKiralanacakEntry = tk.Entry(self.aracKiralamaEkrani)
        self.KacGunKiralanacakEntry.grid(row=12, column=1,pady=10)

        self.nereyeGidilecek = tk.Label(self.aracKiralamaEkrani, text="Nereye Gidilecek",font=("Helvetica 10 bold"),background="#3c6e71",foreground="white")
        self.nereyeGidilecek.grid(row=13, column=0)
        self.nereyeGidilecekEntry = tk.Entry(self.aracKiralamaEkrani)
        self.nereyeGidilecekEntry.grid(row=13, column=1,pady=10)

        self.islemiTamamla = tk.Button(self.aracKiralamaEkrani, text="İşlemi Tamamla",command=self.aracKiralamaBilgileriniVeriTabaninaGonder,font=("Helvetica 10 bold"),background="white",foreground="#3c6e71",width=40)
        
        self.islemiTamamla.grid(row=14, column=0, columnspan=2,pady=10)

        self.veritabaniBaglantisiniYenile = tk.Button(self.aracKiralamaEkrani, text="Veritabani Bağlantısını Yenile",command=self.verileriTablolardanGetir,font=("Helvetica 10 bold"),background="white",foreground="#3c6e71",width=40)
        
        self.veritabaniBaglantisiniYenile.grid(row=15, column=0, columnspan=2,pady=10)

        musterilerTablosunuAc = tk.Button(self.aracKiralamaEkrani, text="Müşteriler Tablosunu Aç",command=lambda pencere=self.aracKiralamaEkrani:self.kayitliMusterileriGoruntule(pencere),font=("Helvetica 10 bold"),background="white",foreground="#3c6e71",width=40)
        musterilerTablosunuAc.grid(row=16, column=0, columnspan=2,pady=10)
        arabalarTablosunuAc = tk.Button(self.aracKiralamaEkrani, text="Arabalar Tablosunu Aç",command=lambda pencere=self.aracKiralamaEkrani:self.kayitliArabalariGoruntule(pencere),font=("Helvetica 10 bold"),background="white",foreground="#3c6e71",width=40)
        arabalarTablosunuAc.grid(row=17, column=0, columnspan=2,pady=10)

    def kiradaOlanAraclarinListesiEkran(self):
        "kirada olan araçların listesini göstermek için kullanılır."
        self.kiradaOlanAraclarinListesiEkrani = tk.Toplevel(self.pencere)
        self.kiradaOlanAraclarinListesiEkrani.title("Kirada Olan Araçların Listesi")
        self.kiradaOlanAraclarinListesiEkrani.configure(background="#3c6e71")
        self.kiradaOlanAraclarinListesiEkrani.geometry("800x600")
        self.kiradaOlanAraclarinListesiEkrani.resizable(False, False)


        self.kiraFrame = tk.Frame(self.kiradaOlanAraclarinListesiEkrani)
        self.kiraFrame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.kiraFrame.config(width=(self.kiradaOlanAraclarinListesiEkrani.winfo_screenwidth()-100),height=(self.kiradaOlanAraclarinListesiEkrani.winfo_screenheight()))
        self.kiraTree = ttk.Treeview(self.kiraFrame,columns=("A","B","C","D","E"), show="headings",selectmode="browse")
        self.kiraTree.pack()
        self.kiraTree.config(height=25)
        
        self.kiraTree.heading("A",text="adSoyadTc")
        self.kiraTree.heading("B",text="marka")
        self.kiraTree.heading("C",text="kiralamaSuresi")
        self.kiraTree.heading("D",text="nereyeGidecek")
        self.kiraTree.heading("E",text="ucret")

        self.kiraTree.column("A",width=200)
        self.kiraTree.column("B",width=100)
        self.kiraTree.column("C",width=100)
        self.kiraTree.column("D",width=100)
        self.kiraTree.column("E",width=100)
        try:
            self.kiraCursor = self.mysqlConn.cursor()
            self.kiraCursor.execute("SELECT * FROM kiralamabilgileri")
            self.kiraVerileri = self.kiraCursor.fetchall()
        except:
            messagebox.showerror("Hata","Veritabanından kiralama Bilgileri çekilemedi.")

        for i,adSoyadTc,marka,kiralamaSuresi,nereyeGidecek,ucret in self.kiraVerileri:
            self.kiraTree.insert("",tk.END,text=i,values=(adSoyadTc,marka,kiralamaSuresi,nereyeGidecek,ucret))

        self.kiraTreeScrollY = tk.Scrollbar(self.kiraFrame,orient=tk.VERTICAL,command=self.kiraTree.yview)
        self.kiraTreeScrollY.pack(side=tk.RIGHT,fill=tk.Y)
        self.kiraTree.config(yscrollcommand=self.kiraTreeScrollY.set)

    def musteriBilgileriniTablodanAl(self):
        "müşteri bilgilerini veritabanından alıp comboboxa eklemek için kullanılır."
        self.musteriBilgileriListe = []
        try:
            self.musteriCursor = self.mysqlConn.cursor()
            self.musteriCursor.execute("SELECT concat(ad,' ',soyad,' ',tcNo) FROM musteribilgileri")
            self.musteriVerileri = self.musteriCursor.fetchall()
            for musteriVeri in self.musteriVerileri:
                self.musteriBilgileriListe.append(musteriVeri[0])
            # print(self.musteriBilgileriListe)
            self.musteriCursor.close() 
        except:
            messagebox.showerror("Hata","Veritabanından müşteri Bilgileri çekilemedi.")



    def arabaBilgileriniTablodanAl(self):
        "araba bilgilerini veritabanından alıp comboboxa eklemek için kullanılır."
        try:
            self.arabaBilgileriListe = []
            self.arabaCursor = self.mysqlConn.cursor()
            self.arabaCursor.execute("SELECT marka FROM arababilgileri")
            self.arabaVerileri = self.arabaCursor.fetchall()
            for arabaVeri in self.arabaVerileri:
                self.arabaBilgileriListe.append(arabaVeri[0])
            # print(self.arabaBilgileriListe)

            self.arabaCursor.close()
        except:
            messagebox.showerror("Hata","Veritabanından araba Bilgileri çekilemedi.")
    
    def verileriTablolardanGetir(self):
        "veritabanı bağlantısını yenilemek için kullanılır. ve ekranı yeniden oluşturur."
        self.aracKiralamaEkrani.destroy()
        self.musteriBilgileriniTablodanAl()
        self.arabaBilgileriniTablodanAl()
        self.aracKiralamaEkran()
    
    def aracKiralamaBilgileriniVeriTabaninaGonder(self):
        "araç kiralama bilgilerini veritabanına göndermek için kullanılır."
        # mesaj kutusu ile bilgilendirme yapılacak.
        try:
            self.aracKiralamaCursor = self.mysqlConn.cursor()
            self.aracKiralamaCursor.execute(f"INSERT INTO kiralamabilgileri (adSoyadTc,marka,kiralamaSuresi,nereyeGidecek,ucret) VALUES ('{self.musteriSecimCombobox.get()}','{self.arabaSecimCombobox.get()}','{self.KacGunKiralanacakEntry.get()}','{self.nereyeGidilecekEntry.get()}','{int(self.KacGunKiralanacakEntry.get())*100}')")
            self.kayitTamamlandı = messagebox.showinfo("Başarılı","Başarıyla araç kiralandı.")
            self.mysqlConn.commit()
            self.aracKiralamaCursor.close()
        except:
            self.kayitTamamlanamadi = messagebox.showinfo("Başarısız","Araç kiralanamadı.")

    def musteriTabloOlustur(self):
        "müşteri bilgilerini tutan tabloyu oluşturur."
        try:
            self.mysqlCursor.execute(f"use arabaKiralamaDB")
            self.mysqlCursor.execute("CREATE TABLE IF NOT EXISTS musteriBilgileri (id INT AUTO_INCREMENT PRIMARY KEY, ad VARCHAR(255), soyad VARCHAR(255), tcNo VARCHAR(255),dogumTarihi VARCHAR(255), adres VARCHAR(255), telefonNo VARCHAR(255),meslek VARCHAR(255),ehliyet VARCHAR(255),medeniHal VARCHAR(255),egitim VARCHAR(255))")
        except Exception as e:
            print(f"hata var {e}")

    def musteriVerileriniTabloyaGonder(self):
        "müşteri bilgilerini tabloya gönderir."
        try:
            self.musteriCursor = self.mysqlConn.cursor()
            self.musteriCursor.execute(f"INSERT INTO musteriBilgileri (ad, soyad, tcNo, dogumTarihi, adres, telefonNo, meslek, ehliyet, medeniHal, egitim) VALUES ('{self.musteriAdiEntry.get()}', '{self.musteriSoyAdiEntry.get()}', '{self.musteriTCEntry.get()}', '{self.musteriDogumTarihiEntry.get()}', '{self.musteriAdresiEntry.get()}', '{self.musteriTelefonNoEntry.get()}', '{self.musteriMeslegiEntry.get()}', '{self.musteriEhliyetSinifiEntry.get()}', '{self.musteriMedeniHaliEntry.get()}', '{self.musteriEgitimDurumuEntry.get()}')")
            self.musteriKayitTamamlandıMesaj = messagebox.showinfo("Müşteri Kayıt Tamamlandi", "Müşteri Kayıt Tamamlandi")
            self.mysqlConn.commit()
            self.musterikayit.destroy()
            # self.mysqlConn.close()
        except Exception as e:
            print(f"Müşteri Bilgilerini tabloya gönderilirken hata oldu hata durumu: {e}")
            self.musteriKayitTamamlanmadıMesaj = messagebox.showerror("kayıt başarısız","kayıt başarısız oldu")

    def veriTabaniOlsutur(self):
        "veritabanını oluşturur."
        try:

            self.mysqlCursor.execute(f"CREATE DATABASE IF NOT EXISTS arabaKiralamaDB")
            self.mysqlCursor.execute(f"use arabaKiralamaDB")
            print("Veri tabani olusturuldu")
        except Exception as e:
            print(f"hata var {e}")   

    def arabaTabloOlustur(self):
        "araba bilgilerini tutan tabloyu oluşturur."
        try:
            self.mysqlCursor.execute(f"use arabaKiralamaDB")
            self.mysqlCursor.execute("CREATE TABLE IF NOT EXISTS arabaBilgileri (id INT AUTO_INCREMENT PRIMARY KEY, marka VARCHAR(255), model VARCHAR(255),uretimYili INT(4),yakitTuru VARCHAR(255),vites VARCHAR(255),motorGucu INT(5),kasaTipi VARCHAR(255), motorHacmi INT(5),cekisTuru VARCHAR(255),kapiSayisi VARCHAR(255), renk VARCHAR(255),motorNo INT(5),sasiNo VARCHAR(255), gunlukKiralamaUcreti INT(6) DEFAULT '100',kiradaMi VARCHAR(255),kullanimDisi VARCHAR(255))")
        except Exception as e:
            print(f"hata var {e}")
    
    def arabaBilgileriniTabloyaGonder(self):
        "araba bilgilerini tabloya gönderir."
        try:
            self.arabaCursor = self.mysqlConn.cursor()
            self.arabaCursor.execute(f"INSERT INTO arabaBilgileri (marka,model,uretimYili,yakitTuru,vites,motorGucu,kasaTipi,motorHacmi,cekisTuru,kapiSayisi,renk,motorNo,sasiNo,gunlukKiralamaUcreti,kiradaMi,kullanimDisi) VALUES ('{self.markaEntry.get()}', '{self.aracModeliEntry.get()}', '{self.uretimYiliEntry.get()}', '{self.yakitTuruEntry.get()}', '{self.vitesEntry.get()}', '{self.motorGucuEntry.get()}', '{self.kasaTipiEntry.get()}', '{self.motoHacmiEntry.get()}', '{self.cekisTuruEntry.get()}', '{self.kapiSayisiEntry.get()}', '{self.renkEntry.get()}', '{self.motorNoEntry.get()}', '{self.sasiNoEntry.get()}', '{self.gunlukKiralamaucretiEntry.get()}', '{self.kiradaMiEntry.get()}', '{self.kullanimDisiMiEntry.get()}')")
            self.arabaKayitTamamlandıMesaj = messagebox.showinfo("Araba Kayit Tamamlandi", "Araba Kayit Tamamlandi")
            self.mysqlConn.commit()
            self.aracBilgileri.destroy()
            # self.mysqlConn.close()
        except Exception as e:
            print(f"Araba bilgilerini tabloya gönderilirken hata oldu hata durumu: {e}")
            self.arabaKayitTamamlanmadıMesaj = messagebox.showinfo("kayıt başarısız","kayıt başarısız oldu")

    def kiralamaTabloOlustur(self):
        "kiralama bilgilerini tutan tabloyu oluşturur."
        try:
            self.mysqlCursor.execute(f"use arabaKiralamaDB")
            self.mysqlCursor.execute("CREATE TABLE IF NOT EXISTS kiralamabilgileri (id INT AUTO_INCREMENT PRIMARY KEY, adSoyadTc varchar(255), marka varchar(255),kiralamaSuresi INT(4),nereyeGidecek VARCHAR(255),ucret INT(9))")
        except Exception as e:
            print(f"kiralama tablosu oluşturulamadı \nhata durumu: {e}")
    def kullaniciTabloOlustur(self):
        "kullanıcı bilgilerini tutan tabloyu oluşturur."
        try:
            self.mysqlCursor.execute(f"use arabaKiralamaDB")
            self.mysqlCursor.execute("CREATE TABLE IF NOT EXISTS kullaniciBilgileri (id INT AUTO_INCREMENT PRIMARY KEY, kullaniciAdi VARCHAR(255), sifre VARCHAR(255), yetki TINYINT(1) NOT NULL DEFAULT '0')")
        except Exception as e:
            print(f"kullanıcı tablosu oluşturulamadı \nhata durumu: {e}")

    def kayitliMusterileriGoruntule(self,pencere):
        "kayıtlı müşterileri görüntüler."
        self.kayitliMusterilerEkran = tk.Toplevel(pencere)
        self.kayitliMusterilerEkran.title("Kayıtlı Müşteriler")
        self.kayitliMusterilerEkran.geometry("1200x500")
        # pencereli tam ekran yapma
        # self.kayitliMusterilerEkran.state("zoomed")
        self.kayitliMusterilerEkran.resizable(False, False)
        self.kayitliMusterilerEkran.config(bg="white")

        self.kayitliMusterilerFrame = tk.Frame(self.kayitliMusterilerEkran)
        self.kayitliMusterilerFrame.place(relx=0.5, rely=0.5, anchor="center")
        # frame ekran büyüklüğünde olsun
        self.kayitliMusterilerFrame.config(width=(self.kayitliMusterilerEkran.winfo_screenwidth()-100), height=(self.kayitliMusterilerEkran.winfo_screenheight()))

        self.kayitliMusterilerTree = ttk.Treeview(self.kayitliMusterilerFrame, columns=("A", "B", "C", "D", "E", "F", "G", "H", "I", "J"), show="headings",selectmode="browse")
        self.kayitliMusterilerTree.pack()
        self.kayitliMusterilerTree.config(height=20)
        self.kayitliMusterilerTree.heading("A", text="ad")
        self.kayitliMusterilerTree.heading("B", text="soyad")
        self.kayitliMusterilerTree.heading("C", text="tcNo")
        self.kayitliMusterilerTree.heading("D", text="dogumTarihi")
        self.kayitliMusterilerTree.heading("E", text="adres")
        self.kayitliMusterilerTree.heading("F", text="telefonNo")
        self.kayitliMusterilerTree.heading("G", text="meslek")
        self.kayitliMusterilerTree.heading("H", text="ehliyet")
        self.kayitliMusterilerTree.heading("I", text="medeniHal")
        self.kayitliMusterilerTree.heading("J", text="egitim")
        self.kayitliMusterilerTree.column("A", width=120)
        self.kayitliMusterilerTree.column("B", width=120)
        self.kayitliMusterilerTree.column("C", width=120)
        self.kayitliMusterilerTree.column("D", width=120)
        self.kayitliMusterilerTree.column("E", width=120)
        self.kayitliMusterilerTree.column("F", width=120)
        self.kayitliMusterilerTree.column("G", width=120)
        self.kayitliMusterilerTree.column("H", width=120)
        self.kayitliMusterilerTree.column("I", width=120)
        self.kayitliMusterilerTree.column("J", width=120)

        try:
            self.musteriBilgiCursor = self.mysqlConn.cursor()
            self.musteriBilgiCursor.execute("SELECT * FROM musteribilgileri")
            self.musteriBilgi = self.musteriBilgiCursor.fetchall()

            for i,ad,soyad,tcNo,dogumTarihi,adres,telefonNo,meslek,ehliyet,medeniHal,egitim in self.musteriBilgi: 
                self.kayitliMusterilerTree.insert("", "end", text=i,values=(ad,soyad,tcNo,dogumTarihi,adres,telefonNo,meslek,ehliyet,medeniHal,egitim))
        except:
            print("müşteri bilgileri çekilemedi")

        # y ekseninde kaydırma çubuğu oluştur
        self.kayitliMusterilerTreeYScroll = tk.Scrollbar(self.kayitliMusterilerFrame, orient="vertical", command=self.kayitliMusterilerTree.yview)
        self.kayitliMusterilerTreeYScroll.pack(side="right", fill="y")
        self.kayitliMusterilerTree.configure(yscrollcommand=self.kayitliMusterilerTreeYScroll.set)

    def kayitliArabalariGoruntule(self,pencere):

        self.kayitliArabalarEkran = tk.Toplevel(pencere)
        self.kayitliArabalarEkran.title("Kayıtlı Arabalar")
        self.kayitliArabalarEkran.geometry("1200x500")
        self.kayitliArabalarEkran.resizable(False, False)
        self.kayitliArabalarEkran.config(bg="white")

        self.kayitliArabalarFrame = tk.Frame(self.kayitliArabalarEkran)
        self.kayitliArabalarFrame.place(relx=0.5, rely=0.5, anchor="center")
        self.kayitliArabalarFrame.config(width=(self.kayitliArabalarEkran.winfo_screenwidth()-100), height=(self.kayitliArabalarEkran.winfo_screenheight()))

        self.kayitliArabalarTree = ttk.Treeview(self.kayitliArabalarFrame, columns=("A", "B", "C", "D", "E", "F", "G", "H", "I", "J","K","L","M","N","O","P"), show="headings",selectmode="browse")
        self.kayitliArabalarTree.pack()
        self.kayitliArabalarTree.config(height=20)
        self.kayitliArabalarTree.heading("A", text="marka")
        self.kayitliArabalarTree.heading("B", text="model")
        self.kayitliArabalarTree.heading("C", text="uretimYili")
        self.kayitliArabalarTree.heading("D", text="yakitTuru")
        self.kayitliArabalarTree.heading("E", text="vites")
        self.kayitliArabalarTree.heading("F", text="motorGucu")
        self.kayitliArabalarTree.heading("G", text="kasaTipi")
        self.kayitliArabalarTree.heading("H", text="motorHacmi")
        self.kayitliArabalarTree.heading("I", text="cekisTuru")
        self.kayitliArabalarTree.heading("J", text="kapiSayisi")
        self.kayitliArabalarTree.heading("K", text="renk")
        self.kayitliArabalarTree.heading("L", text="motornNo")
        self.kayitliArabalarTree.heading("M", text="sasiNo")
        self.kayitliArabalarTree.heading("N", text="gunlukKiralamaUcreti")
        self.kayitliArabalarTree.heading("O", text="kiradaMi")
        self.kayitliArabalarTree.heading("P", text="kullanimDisi")

        self.kayitliArabalarTree.column("A", width=75)
        self.kayitliArabalarTree.column("B", width=75)
        self.kayitliArabalarTree.column("C", width=75)
        self.kayitliArabalarTree.column("D", width=75)
        self.kayitliArabalarTree.column("E", width=75)
        self.kayitliArabalarTree.column("F", width=75)
        self.kayitliArabalarTree.column("G", width=75)
        self.kayitliArabalarTree.column("H", width=75)
        self.kayitliArabalarTree.column("I", width=75)
        self.kayitliArabalarTree.column("J", width=75)
        self.kayitliArabalarTree.column("K", width=75)
        self.kayitliArabalarTree.column("L", width=75)
        self.kayitliArabalarTree.column("M", width=75)
        self.kayitliArabalarTree.column("N", width=75)
        self.kayitliArabalarTree.column("O", width=75)
        self.kayitliArabalarTree.column("P", width=75)

        try:
            self.arabaBilgiCursor = self.mysqlConn.cursor()
            self.arabaBilgiCursor.execute("SELECT * FROM arababilgileri")
            self.arabaBilgi = self.arabaBilgiCursor.fetchall()

            for i,marka,model,uretimYili,yakitTuru,vites,motorGucu,kasaTipi,motorHacmi,cekisTuru,kapiSayisi,renk,motornNo,sasiNo,gunlukKiralamaUcreti,kiradaMi,kullanimDisi in self.arabaBilgi:
                self.kayitliArabalarTree.insert("", "end", text=i,values=(marka,model,uretimYili,yakitTuru,vites,motorGucu,kasaTipi,motorHacmi,cekisTuru,kapiSayisi,renk,motornNo,sasiNo,gunlukKiralamaUcreti,kiradaMi,kullanimDisi))
        except:
            messagebox.showerror("Hata", "Veritabanı bağlantısı kurulamadı")
        # y ekseninde kaydırma çubuğu oluştur
        self.kayitliArabalarTreeYScroll = tk.Scrollbar(self.kayitliArabalarFrame, orient="vertical", command=self.kayitliArabalarTree.yview)
        self.kayitliArabalarTreeYScroll.pack(side="right", fill="y")
        self.kayitliArabalarTree.configure(yscrollcommand=self.kayitliArabalarTreeYScroll.set)

    def helpPager(self):
        "Yardım sayfası"
        self.helpPage = tk.Toplevel(self.pencere)
        self.helpPage.title("Nasıl çalışır")
        self.helpPage.geometry("800x500")
        self.helpPage.resizable(False, False)
        # self.helpPage.iconbitmap("icon.ico")
        self.helpPage.config(bg="#284b63")

        self.helpPageLabel = tk.Label(self.helpPage, text="Yardım", font=("Arial", 20), bg="#284b63")
        self.helpPageLabel.pack(pady=10)

        self.helpPageText = tk.Text(self.helpPage, width=50, height=20, bg="white", font=("Arial", 12))
        self.helpPageText.pack()
        self.helpPageText.insert("1.0", "1-) Programı ilk çalıştırıldığında root kullanıcı adı ile mysql veritabanına bağlanır.\r\n")
        self.helpPageText.insert("2.0", "2-) Veritabanı bağlantısı yapıldıktan sonra arabaKiralamaDB isimli veritabanı oluşturur.\r\n")
        self.helpPageText.insert("3.0", "3-) Daha sonra 'arababilgileri' , 'müsteribilgileri' ve 'kiralamabilgileri' adlı üç adet tablo oluşturur.\r\n")
        self.helpPageText.insert("4.0", "4-) Ana ekrandan yapacağınız müşteri kayıt işlemi sonrasında veriler musteribilgileri adlı tabloya kaydedilir.\r")
        self.helpPageText.insert("5.0", "5-) Ana ekrandan yapacağınız araba kayıt işlemi sonrasında veriler arababilgileri adlı tabloya kaydedilir.\r\n")
        self.helpPageText.insert("6.0", "6-) Ana ekrandan yapacağınız kiralama işlemi sonrasında veriler kiralamabilgileri adlı tabloya kaydedilir.\r\n")
        # self.helpPageText.insert("7.0", ")
        self.helpPageText.config(state="disabled")

    def about(self):
        "Hakkında sayfası"
        self.aboutPage = tk.Toplevel(self.pencere)
        self.aboutPage.title("Hakkında")
        self.aboutPage.geometry("800x500")
        self.aboutPage.resizable(False, False)
        # self.aboutPage.iconbitmap("icon.ico")
        self.aboutPage.config(bg="#284b63")

        self.aboutPageLabel = tk.Label(self.aboutPage, text="Hakkında", font=("Arial", 20), bg="#284b63")
        self.aboutPageLabel.pack(pady=10)

        self.aboutPageText = tk.Text(self.aboutPage, width=50, height=20, bg="white", font=("Arial", 12))
        self.aboutPageText.pack()
        self.aboutPageText.insert("1.0", "Adı : Hamza\r\n")
        self.aboutPageText.insert("2.0", "Soyadı : ORTATEPE\r\n")
        self.aboutPageText.insert("3.0", "Araç kiralama sistemi\r\n")
        self.aboutPageText.insert("4.0", "\r")
    def müşterileriGöster(self):
        "Müşterileri göster"
        
    def aramaEkrani(self):
        self.aramaEkraniPencere = tk.Toplevel(self.pencere)
        self.aramaEkraniPencere.title("Arama")
        self.aramaEkraniPencere.geometry("800x500")
        self.aramaEkraniPencere.resizable(False, False)
        self.aramaEkraniPencere.config(bg="#284b63")

        self.aramaEkraniLabel = tk.Label(self.aramaEkraniPencere, text="Müşteri Arama (Tc Girin)", font=("Broadway 25 bold underline"),bg="#284b63",fg="white")
        self.aramaEkraniLabel.pack(pady=10)

        self.aramaEkraniEntry = tk.Entry(self.aramaEkraniPencere, width=50, font=("Arial", 12))
        self.aramaEkraniEntry.pack(pady=10)

        self.aramaEkraniButton = tk.Button(self.aramaEkraniPencere, text="Ara", font=("Arial", 12), command=self.musteriAra)
        self.aramaEkraniButton.pack(pady=10)

        self.aramaEkraniLabel = tk.Label(self.aramaEkraniPencere, text="", font=("Arial", 12), bg="#284b63")
        self.aramaEkraniLabel.pack(pady=10)

        self.aramaEkraniBilgi = tk.Label(self.aramaEkraniPencere, text="sırasıyla gelen bilgiler:\nid,ad,soyad,tcNo,dogumTarihi,adres,telefonNo,meslek,ehliyet,medeniHal,egitim", font=("Arial", 10), bg="#284b63")
        self.aramaEkraniBilgi.pack(pady=10)
    def musteriAra(self):
        self.aramaCursor = self.mysqlConn.cursor()
        self.aramaCursor.execute(F"USE arabaKiralamaDB")
        self.aramaCursor.execute(F"SELECT * FROM musteribilgileri WHERE tcNo = '{self.aramaEkraniEntry.get()}' ")
        self.aramaVeriler = self.aramaCursor.fetchall()
        self.aramaEkraniLabel.config(text=self.aramaVeriler)
   
otomasyon = aracOtomasyonu()
