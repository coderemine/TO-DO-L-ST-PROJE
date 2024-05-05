from tkinter import *
import tkinter as tk
from tkinter import messagebox
import json

class Uygulama:

    def __init__(self):
        # Tkinter penceresini oluşturdum
        self.pencere = tk.Tk()
        self.pencere.title("To-Do List App")
        self.pencere.config(bg="purple") # Pencere arkaplan rengini ayarladım
        self.yapilacaklar = []  # Görev listesi için boş bir liste oluşturdum
        self.tamamlananlar = []  # Tamamlanan görev listesi için boş bir liste oluşturdum

        # Dosyadan görevleri yüklemek için yönlendirdiğim fonksiyon
        self.dosya_ara()

        # Başlık çerçevesini oluşturdum
        self.basliklar_cerceve = tk.Frame(self.pencere)
        self.basliklar_cerceve.pack(pady=12)

        # Listeler çerçevesini oluşturdum
        self.listeler_cerceve = tk.Frame(self.pencere)
        self.listeler_cerceve.pack(pady=12)

        # Görev Listesi başlığını oluşturdum
        self.gorev_yazi = tk.Label(self.basliklar_cerceve, text="Görev Listesi", font=("Times", 14))
        self.gorev_yazi.pack(side=tk.LEFT, padx=110, pady=5)

        # Tamamlanmış Görevler Listesi başlığını oluşturdum
        self.tamamlanmis_yazi = tk.Label(self.basliklar_cerceve, text="Tamamlanmış Görevler Listesi", font=("Times", 14))
        self.tamamlanmis_yazi.pack(side=tk.LEFT, padx=50, pady=5)

        # Yapılacak Görev ve tamamlanan görevler olarak 2 ayrı listbox'ını oluşturdum
        self.gorev_listbox = tk.Listbox(self.listeler_cerceve, selectmode=tk.SINGLE, width=50)
        self.gorev_listbox.pack(side=tk.LEFT, pady=10)

        self.tamamlanmis_listbox = tk.Listbox(self.listeler_cerceve, selectmode=tk.SINGLE, width=50)
        self.tamamlanmis_listbox.pack(side=tk.RIGHT, pady=10)

        # listbox'ları scrollbar ile bağladım
        self.gorev_scrollbar = tk.Scrollbar(self.listeler_cerceve, orient=tk.VERTICAL)
        self.gorev_scrollbar.pack(side=tk.LEFT, fill=tk.Y)
        self.gorev_listbox.config(yscrollcommand=self.gorev_scrollbar.set)
        self.gorev_scrollbar.config(command=self.gorev_listbox.yview)


        self.tamamlanmis_scrollbar = tk.Scrollbar(self.listeler_cerceve, orient=tk.VERTICAL)
        self.tamamlanmis_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tamamlanmis_listbox.config(yscrollcommand=self.tamamlanmis_scrollbar.set)
        self.tamamlanmis_scrollbar.config(command=self.tamamlanmis_listbox.yview)

        # Silme, ekleme ,tamamlama butonlarını oluşturdum , çalışma işlevine ait fonksiyonlarına yönlendirdim
        self.sil_buton = tk.Button(self.pencere, text="Sil", cursor="hand2", activebackground="Red", command=self.gorev_sil, bg="yellow")
        self.sil_buton.pack(side=tk.BOTTOM, padx=5, pady=10)

        self.tamamla_buton = tk.Button(self.pencere, text="Tamamla", cursor="hand2", activebackground="Green", command=self.gorev_tamamla, bg="green")
        self.tamamla_buton.pack(side=tk.BOTTOM, padx=5, pady=10)

        self.ekle_buton = tk.Button(self.pencere, text="Ekle", cursor="hand2", command=self.gorev_ekle_ekrani, bg="red")
        self.ekle_buton.pack(side=tk.BOTTOM, padx=5, pady=10)

        # Ekrana yaz fonksiyonunu çağırdım
        self.ekrana_yaz()

    def gorev_ekle_ekrani(self):
        # Görev ekle penceresini oluşturdum
        ekle_pencere = tk.Toplevel(self.pencere)
        ekle_pencere.title("Görev Ekle")

        # Başlıkları oluşturup onları paketledim
        yazi1 = tk.Label(ekle_pencere, text="Görevinizi giriniz")
        yazi1.pack()

        girdi1 = tk.Entry(ekle_pencere)
        girdi1.pack()

        yazi2 = tk.Label(ekle_pencere, text="Görevin önem sırasını giriniz")
        yazi2.pack()

        girdi2 = tk.Entry(ekle_pencere)
        girdi2.pack()

        # Ekle butonu oluşturup gerekli fonksiyona bağladım
        ekle_buton = tk.Button(ekle_pencere, text="Ekle", cursor="hand2", command=lambda: self.gorev_ekle(ekle_pencere, girdi1.get(), girdi2.get()))
        ekle_buton.pack()

    def gorev_ekle(self, pencere, girdi1, girdi2):
        # Girilen girdilerin nasıl olması gerektiği konusunda geri bildirimler verdim ,ve listeye girilen görev ve önem sıralarını atadım
        if girdi1 == "":
            messagebox.showerror("Dikkat", "Boş görev girişi olamaz!")
            pencere.destroy()
        elif not girdi2.isdigit():
            messagebox.showerror("Dikkat", "Önem sırasına sayı girilmelidir!")
            pencere.destroy()
        elif girdi2 == "":
            messagebox.showerror("Dikkat", "Boş önem sırası olamaz!")
            pencere.destroy()
        else:
            messagebox.showinfo("Tebrikler", "Görev başarıyla eklendi:)")
            pencere.destroy()
            ana = {"Görev": girdi1, "Önem Sırası": int(girdi2)}
            self.yapilacaklar.append(ana)
            self.sirala()
            self.ekrana_yaz()
            self.dosyaya_kaydet()

    def sirala(self):
        # Sıralama fonksiyonu yaptım
        for i in range(len(self.yapilacaklar)):
            for j in range(0, len(self.yapilacaklar) - i - 1):
                if self.yapilacaklar[j]["Önem Sırası"] > self.yapilacaklar[j + 1]["Önem Sırası"]:
                    temp = self.yapilacaklar[j]
                    self.yapilacaklar[j] = self.yapilacaklar[j + 1]
                    self.yapilacaklar[j + 1] = temp

    def gorev_sil(self):
        # Görev sil fonksiyonu yaptım
        index = self.gorev_listbox.curselection()
        index2 = self.tamamlanmis_listbox.curselection()
        if index:
            del self.yapilacaklar[index[0]]
            messagebox.showinfo("!", "Görev Silindi.")
            self.dosyaya_kaydet()
            self.ekrana_yaz()
        elif index2:
            del self.tamamlananlar[index2[0]]
            messagebox.showinfo("Tebrikler", "Tamamlanmış görev silindi.")
            self.dosyaya_kaydet()
            self.ekrana_yaz()

    def gorev_tamamla(self):
        # Görev tamamlama fonksiyonu yaptım
        index = self.gorev_listbox.curselection()
        if index:
            tamamlanan = self.yapilacaklar[index[0]]
            self.tamamlananlar.append(tamamlanan)
            del self.yapilacaklar[index[0]]
            messagebox.showinfo("Tebrikler", "Görev tamamlandı.")
            self.ekrana_yaz()
            self.dosyaya_kaydet()

    def ekrana_yaz(self):
        # Listbox'lara görevleri yazan fonksiyon yaptım
        self.gorev_listbox.delete(0, tk.END)
        self.tamamlanmis_listbox.delete(0, tk.END)

        for gorev in self.yapilacaklar:
            self.gorev_listbox.insert(tk.END, f"Görev: {gorev['Görev']}, Önem Sırası: {gorev['Önem Sırası']}")

        for tgorev in self.tamamlananlar:
            self.tamamlanmis_listbox.insert(tk.END, f"Görev: {tgorev['Görev']}, Önem Sırası: {tgorev['Önem Sırası']}")

    def dosyaya_kaydet(self):
        # Görevleri dosyaya kaydeden fonksiyon yaptım
        dosya = open("gorevler.json", "w")
        dosya2 = open("tgorevler.json", "w")
        json.dump(self.yapilacaklar, dosya)
        json.dump(self.tamamlananlar, dosya2)

    def dosya_ara(self):
        # Dosyadan görevleri okuyan fonksiyon yaptım
        try:
            dosya = open("gorevler.json", "r")
            self.yapilacaklar = json.load(dosya)
        except FileNotFoundError:
            messagebox.showwarning("Dikkat", "Görev bulunamadı. Yeni dosya oluşturuldu.")
            self.yapilacaklar = []

        try:
            dosya2 = open("tgorevler.json", "r")
            self.tamamlananlar= json.load(dosya2)
        except FileNotFoundError:
            messagebox.showwarning("Dikkat", "Tamamlanmış görev bulunamadı. Yeni dosya oluşturuldu.")
            self.tamamlananlar = []

# Uygulamayı başlatan durum
uygulama = Uygulama()
uygulama.pencere.mainloop()