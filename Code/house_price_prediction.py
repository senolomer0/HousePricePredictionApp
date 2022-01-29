from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5.QtWidgets import QFrame
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QCursor
import sys
from datetime import datetime
import webbrowser
import joblib
from catboost import CatBoostRegressor
from warnings import filterwarnings
filterwarnings("ignore")

class Variables_Line_Edit(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color:white")
        self.init()

    def init(self):
        self.label = QtWidgets.QLabel()
        self.label.setFont(QtGui.QFont("sans-serif",12))
        spacer = QtWidgets.QSpacerItem(10,0)
        
        self.input = QtWidgets.QLineEdit()
        self.input.setFixedSize(150,25)
        self.input.setStyleSheet("QLineEdit""{""background-color:white;border:1px solid gray;border-radius:5px;padding-left:5px""}""QLineEdit::focus""{""border:2px solid #114171""}")

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addItem(spacer)
        self.layout.addWidget(self.input)
        self.setLayout(self.layout)

class Variables_Combo(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color:white")
        self.init()

    def init(self):
        self.label = QtWidgets.QLabel()
        self.label.setFont(QtGui.QFont("sans-serif",12))
        spacer = QtWidgets.QSpacerItem(10,0)

        self.combobox = QtWidgets.QComboBox()
        self.combobox.setFixedSize(150,25)
        self.combobox.setStyleSheet("background-color:white; color:#455D84; border-radius:5px; border:1px solid #455D84;")
        self.combobox.setStyleSheet("QComboBox""{""background-color:white;border:1px solid gray;border-radius:5px;padding-left:5px""}""QComboBox::focus""{""border:2px solid #114171""}""QComboBox::drop-down""{""border:0px""}")
        self.combobox.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.combobox.addItem("- - - - -")
        self.combobox.setFont(QtGui.QFont("sans-serif",10))
        
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addItem(spacer)
        self.layout.addWidget(self.combobox)
        self.setLayout(self.layout)

class Main_Page(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(700, 700)
        self.setFixedSize(1200,800)
        self.setStyleSheet("background-color:white;")
        self.setWindowIcon(QtGui.QIcon("Price Prediction Photos/app_icon.png"))

        self.current_value_il = "- - - - -"

        self.setWindowTitle("House Price Prediction")
        self.widgets()

    def run_func(self):
        now = datetime.now()
        time = now.strftime("%H:%M:%S")
        self.current_time.setText(time)

        ilceler = {"- - - - -":[],
        "ankara":["akyurt","altındağ","çankaya","çubuk","etimesgut","gölbaşı","kahramankazan","keçiören","mamak","polatlı","pursaklar","sincan","yenimahalle"],
        "antalya":["akseki","aksu","alanya","döşemealtı","finike","gazipaşa","kaş","kemer","kepez","konyaaltı","korkuteli","manavgat","muratpaşa","serik"],
        "gaziantep":["islahiye","nizip","nurdağı","oğuzeli","yavuzeli","şahinbey","şehitkamil"],
        "istanbul":['arnavutköy','ataşehir','avcılar','bağcılar','bahçelievler','bakırköy','başakşehir','beylikdüzü','bayrampaşa','beyoğlu','beşiktaş','büyükçekmece','çekmeköy','esenler','esenyurt','eyüpsultan','fatih','gaziosmanpaşa','güngören','kadıköy','kartal','kağıthane','küçükçekmece','maltepe','pendik','sancaktepe','sarıyer','silivri','sultanbeyli','sultangazi','şile','şişli','tuzla','ümraniye','üsküdar','zeytinburnu'],
        "izmir":['aliağa','balçova','bayraklı','bergama','bornova','buca','çeşme','çiğli','dikili','foça','gaziemir','güzelbahçe','karabağlar','karaburun','karşıyaka','kemalpaşa','kiraz','konak','kınık','menderes','menemen','narlıdere','ödemiş','seferihisar','selçuk','tire','torbalı','urla'],
        "konya":['akşehir','beyşehir','cihanbeyli','çumra','ereğli','ilgın','kadınhanı','karapınar','karatay','kulu','meram','sarayönü','selçuklu','seydişehir'],
        "mersin":['akdeniz','anamur','bozyazı','erdemli','gülnar','mezitli','mut','silifke','tarsus','toroslar','yenişehir'],
        "muğla":['bodrum','dalaman','datça','fethiye','köyceğiz','marmaris','menteşe','milas','ortaca','seydikemer','ula','yatağan'],
        "şanlıurfa":['akçakale','birecik','ceylanpınar','eyyübiye','halfeti','haliliye','hilvan','karaköprü','siverek','suruç','viranşehir'],
        "trabzon":['akçaabat','araklı','arsin','beşikdüzü','dernekpazarı','çarşıbaşı','çaykara','maçka','of','ortahisar','sürmene','şalpazarı','vakfıkebir','yomra'],
        "van":['edremit','erciş','ipekyolu','tuşba']}

        if (self.variable1.combobox.currentText() != self.current_value_il):
            self.current_value_il = self.variable1.combobox.currentText()
            self.variable2.combobox.setEnabled(True)
            self.variable2.combobox.clear()
            self.variable2.combobox.addItem("- - - - -")
            for i in ilceler[self.variable1.combobox.currentText()]:
                self.variable2.combobox.addItem(i)

        elif (self.variable1.combobox.currentText() == "- - - - -"):
            self.variable2.combobox.setEnabled(False)

        try:
            int(self.variable4.input.text())
            self.variable4.input.setStyleSheet("QLineEdit""{""background-color:white;border:1px solid gray;border-radius:5px;padding-left:5px""}""QLineEdit::focus""{""border:2px solid #114171""}")
        except:
            if len(self.variable4.input.text()) > 0:
                self.variable4.input.setStyleSheet("QLineEdit""{""background-color:white;border:1px solid red;border-radius:5px;padding-left:5px""}""QLineEdit::focus""{""border:2px solid red""}")
        try:
            int(self.variable5.input.text())
            self.variable5.input.setStyleSheet("QLineEdit""{""background-color:white;border:1px solid gray;border-radius:5px;padding-left:5px""}""QLineEdit::focus""{""border:2px solid #114171""}")
        except:
            if len(self.variable5.input.text()) > 0:
                self.variable5.input.setStyleSheet("QLineEdit""{""background-color:white;border:1px solid red;border-radius:5px;padding-left:5px""}""QLineEdit::focus""{""border:2px solid red""}")
        try:
            int(self.variable7.input.text())
            self.variable7.input.setStyleSheet("QLineEdit""{""background-color:white;border:1px solid gray;border-radius:5px;padding-left:5px""}""QLineEdit::focus""{""border:2px solid #114171""}")
        except:
            if len(self.variable7.input.text()) > 0:
                self.variable7.input.setStyleSheet("QLineEdit""{""background-color:white;border:1px solid red;border-radius:5px;padding-left:5px""}""QLineEdit::focus""{""border:2px solid red""}")
        try:
            int(self.variable9.input.text())
            self.variable9.input.setStyleSheet("QLineEdit""{""background-color:white;border:1px solid gray;border-radius:5px;padding-left:5px""}""QLineEdit::focus""{""border:2px solid #114171""}")
        except:
            if len(self.variable9.input.text()) > 0:
                self.variable9.input.setStyleSheet("QLineEdit""{""background-color:white;border:1px solid red;border-radius:5px;padding-left:5px""}""QLineEdit::focus""{""border:2px solid red""}")
        try:
            int(self.variable11.input.text())
            self.variable11.input.setStyleSheet("QLineEdit""{""background-color:white;border:1px solid gray;border-radius:5px;padding-left:5px""}""QLineEdit::focus""{""border:2px solid #114171""}")
        except:
            if len(self.variable11.input.text()) > 0:
                self.variable11.input.setStyleSheet("QLineEdit""{""background-color:white;border:1px solid red;border-radius:5px;padding-left:5px""}""QLineEdit::focus""{""border:2px solid red""}")

        if (((self.variable1.combobox.currentText() != "- - - - -") and (self.variable2.combobox.currentText() != "- - - - -") and (self.variable3.combobox.currentText() != "- - - - -")
        and (self.variable6.combobox.currentText() != "- - - - -") and (self.variable8.combobox.currentText() != "- - - - -") and (self.variable10.combobox.currentText() != "- - - - -")
        and (self.variable12.combobox.currentText() != "- - - - -") and (self.variable13.combobox.currentText() != "- - - - -") and (self.variable14.combobox.currentText() != "- - - - -")
        and (self.variable15.combobox.currentText() != "- - - - -") and (self.variable16.combobox.currentText() != "- - - - -") and (self.variable17.combobox.currentText() != "- - - - -")
        and (self.variable18.combobox.currentText() != "- - - - -")) and 
        ((len(self.variable4.input.text()) != 0) and (len(self.variable5.input.text())!= 0) and (len(self.variable7.input.text())!= 0) and (len(self.variable9.input.text())!= 0)
        and (len(self.variable11.input.text())!= 0))):
            try:
                int(self.variable4.input.text())
                int(self.variable5.input.text())
                int(self.variable7.input.text())
                int(self.variable9.input.text())
                int(self.variable11.input.text())
                self.calculate_button.setEnabled(True)
                self.calculate_button.setStyleSheet("background-color:white;border-radius:5px;color:#114171;border:2px solid #114171") 
            except:
                self.calculate_button.setEnabled(False)
                self.calculate_button.setStyleSheet("background-color:white;border-radius:5px;color:gra;border:2px solid gray") 

        else:
            self.calculate_button.setEnabled(False)
            self.calculate_button.setStyleSheet("background-color:white;border-radius:5px;color:gra;border:2px solid gray") 

    def labels(self):
        self.il_labels = {'ankara': 0, 'antalya': 1, 'bursa': 2, 'gaziantep': 3, 'istanbul': 4, 'izmir': 5, 'konya': 6, 'mersin': 7, 'muğla': 8, 'trabzon': 9, 'van': 10, 'şanlıurfa': 11}
        self.ilce_labels = {'akdeniz': 0, 'akseki': 1, 'aksu': 2, 'akyurt': 3, 'akçaabat': 4, 'akçakale': 5, 'akşehir': 6, 'alanya': 7, 'aliağa': 8, 'altındağ': 9, 'anamur': 10, 'araklı': 11, 'arnavutköy': 12, 'arsin': 13, 'ataşehir': 14, 'avcılar': 15, 'bahçelievler': 16, 'bakırköy': 17, 'balçova': 18, 'bayraklı': 19, 'bayrampaşa': 20, 'bağcılar': 21, 'başakşehir': 22, 'bergama': 23, 'beylikdüzü': 24, 'beyoğlu': 25, 'beyşehir': 26, 'beşikdüzü': 27, 'beşiktaş': 28, 'birecik': 29, 'bodrum': 30, 'bornova': 31, 'bozyazı': 32, 'buca': 33, 'büyükçekmece': 34, 'ceylanpınar': 35, 'cihanbeyli': 36, 'dalaman': 37, 'datça': 38, 'dernekpazarı': 39, 'dikili': 40, 'döşemealtı': 41, 'edremit': 42, 'erciş': 43, 'erdemli': 44, 'ereğli': 45, 'esenler': 46, 'esenyurt': 47, 'etimesgut': 48, 'eyyübiye': 49, 'eyüpsultan': 50, 'fatih': 51, 'fethiye': 52, 'finike': 53, 'foça': 54, 'gaziemir': 55, 'gaziosmanpaşa': 56, 'gazipaşa': 57, 'gemlik': 58, 'gölbaşı': 59, 'gülnar': 60, 'güngören': 61, 'gürsu': 62, 'güzelbahçe': 63, 'halfeti': 64, 'haliliye': 65, 'hilvan': 66, 'ilgın': 67, 'inegöl': 68, 'ipekyolu': 69, 'islahiye': 70, 'iznik': 71, 'kadıköy': 72, 'kadınhanı': 73, 'kahramankazan': 74, 'karabağlar': 75, 'karaburun': 76, 'karacabey': 77, 'karaköprü': 78, 'karapınar': 79, 'karatay': 80, 'kartal': 81, 'karşıyaka': 82, 'kağıthane': 83, 'kaş': 84, 'kemalpaşa': 85, 'kemer': 86, 'kepez': 87, 'kestel': 88, 'keçiören': 89, 'kiraz': 90, 'konak': 91, 'konyaaltı': 92, 'korkuteli': 93, 'kulu': 94, 'köyceğiz': 95, 'küçükçekmece': 96, 'kınık': 97, 'maltepe': 98, 'mamak': 99, 'manavgat': 100, 'marmaris': 101, 'maçka': 102, 'menderes': 103, 'menemen': 104, 'menteşe': 105, 'meram': 106, 'mezitli': 107, 'milas': 108, 'mudanya': 109, 'muratpaşa': 110, 'mustafakemalpaşa': 111, 'mut': 112, 'narlıdere': 113, 'nilüfer': 114, 'nizip': 115, 'nurdağı': 116, 'of': 117, 'orhangazi': 118, 'ortaca': 119, 'ortahisar': 120, 'osmangazi': 121, 'oğuzeli': 122, 'pendik': 123, 'polatlı': 124, 'pursaklar': 125, 'sancaktepe': 126, 'sarayönü': 127, 'sarıyer': 128, 'seferihisar': 129, 'selçuk': 130, 'selçuklu': 131, 'serik': 132, 'seydikemer': 133, 'seydişehir': 134, 'silifke': 135, 'silivri': 136, 'sincan': 137, 'siverek': 138, 'sultanbeyli': 139, 'sultangazi': 140, 'suruç': 141, 'sürmene': 142, 'tarsus': 143, 'tire': 144, 'torbalı': 145, 'toroslar': 146, 'tuzla': 147, 'tuşba': 148, 'ula': 149, 'urla': 150, 'vakfıkebir': 151, 'viranşehir': 152, 'yatağan': 153, 'yavuzeli': 154, 'yenimahalle': 155, 'yenişehir': 156, 'yomra': 157, 'yıldırım': 158, 'zeytinburnu': 159, 'çankaya': 160, 'çarşıbaşı': 161, 'çaykara': 162, 'çekmeköy': 163, 'çeşme': 164, 'çiğli': 165, 'çubuk': 166, 'çumra': 167, 'ödemiş': 168, 'ümraniye': 169, 'üsküdar': 170, 'şahinbey': 171, 'şalpazarı': 172, 'şehitkamil': 173, 'şile': 174, 'şişli': 175}
        self.emlak_tipi_labels = {'daire': 0, 'residence': 1, 'yazlık': 2}
        self.bulundugu_kat_labels = {'1': 0, '10': 1, '11': 2, '12': 3, '13': 4, '14': 5, '15': 6, '16': 7, '17': 8, '18': 9, '2': 10, '20': 11, '21': 12, '22': 13, '23': 14, '24': 15, '3': 16, '30 ve üzeri': 17, '4': 18, '5': 19, '6': 20, '7': 21, '8': 22, '9': 23, 'bahçe katı': 24, 'bodrum kat': 25, 'giriş katı': 26, 'kot 1': 27, 'kot 2': 28, 'kot 3': 29, 'kot 4': 30, 'müstakil': 31, 'villa tipi': 32, 'yüksek giriş': 33, 'zemin kat': 34, 'çatı katı': 35}
        self.isitma_labels = {'doğalgaz': 0, 'doğalgaz sobası': 1, 'güneş enerjisi': 2, 'isı pompası': 3, 'jeotermal': 4, 'kat kaloriferi': 5, 'klima': 6, 'merkezi': 7, 'soba': 8, 'vrv': 9, 'yerden isıtma': 10, 'yok': 11, 'şömine': 12}
        self.balkon_labels = {'var': 0, 'yok': 1}
        self.esyali_labels = {'evet': 0, 'hayır': 1}
        self.kullanim_durumu_labels = {'boş': 0, 'kiracılı': 1, 'mülk sahibi': 2}
        self.site_icerisinde_labels = {'evet': 0, 'hayır': 1}
        self.krediye_uygun_labels = {'evet': 0, 'hayır': 1}
        self.kimden_labels = {'bankadan': 0, 'emlak ofisinden': 1, 'inşaat firmasından': 2, 'sahibinden': 3}
        self.takas_labels = {'evet': 0, 'hayır': 1}

    def predict(self):
        room, living_room = self.variable6.combobox.currentText().split("+")

        liste = []
        self.labels()

        liste.append(self.il_labels[self.variable1.combobox.currentText()])
        liste.append(self.ilce_labels[self.variable2.combobox.currentText()])
        liste.append(self.emlak_tipi_labels[self.variable3.combobox.currentText()])
        liste.append(int(self.variable4.input.text()))
        liste.append(int(self.variable5.input.text()))
        liste.append(int(room))
        liste.append(int(self.variable7.input.text()))
        liste.append(self.bulundugu_kat_labels[self.variable8.combobox.currentText()])
        liste.append(int(self.variable9.input.text()))
        liste.append(self.isitma_labels[self.variable10.combobox.currentText()])
        liste.append(int(self.variable11.input.text()))
        liste.append(self.balkon_labels[self.variable12.combobox.currentText()])
        liste.append(self.esyali_labels[self.variable13.combobox.currentText()])
        liste.append(self.kullanim_durumu_labels[self.variable14.combobox.currentText()])
        liste.append(self.site_icerisinde_labels[self.variable15.combobox.currentText()])
        liste.append(self.krediye_uygun_labels[self.variable16.combobox.currentText()])
        liste.append(self.kimden_labels[self.variable17.combobox.currentText()])
        liste.append(self.takas_labels[self.variable18.combobox.currentText()])
        liste.append(int(living_room))
        liste.append(int(self.variable11.input.text()) / int(room))
        
        j_model = joblib.load("model")
        y = f"{int(j_model.predict([liste])[0]):,.2f}"
        z = y.replace(",", "!").replace(".", ",").replace("!", ".")

        self.predicted_value.setText("Predicted Value : "+str(z)+" TL")

    def widgets(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.run_func)
        self.timer.start(500)

        self.app_logo=QtWidgets.QPushButton()
        self.app_logo.setStyleSheet("background-image : url(Price Prediction Photos/app_icon.png);background-repeat: no-repeat;border: 0px;")
        self.app_logo.setMinimumSize(70,70)
        self.app_logo.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.app_logo.clicked.connect(lambda:webbrowser.open("https://github.com/senolomer0"))

        self.header = QtWidgets.QLabel("House Price Prediction")
        self.header.setFont(QtGui.QFont("times-new-roman",30))

        self.current_time = QtWidgets.QLabel("00:00:00")
        self.current_time.setFont(QtGui.QFont("sans-serif",14))

        self.variable1 = Variables_Combo()
        self.variable1.label.setText("İl")
        il_values = ["ankara","antalya","gaziantep","istanbul","izmir","konya","mersin","muğla","şanlıurfa","trabzon","van"]
        for i in il_values:
            self.variable1.combobox.addItem(i)

        self.variable2 = Variables_Combo()
        self.variable2.label.setText("İlçe")
        self.variable2.combobox.setEnabled(False)

        self.variable3 = Variables_Combo()
        self.variable3.label.setText("Emlak Tipi")
        self.variable3.combobox.addItem("daire")
        self.variable3.combobox.addItem("yazlık")
        self.variable3.combobox.addItem("residence")

        self.variable4 = Variables_Line_Edit()
        self.variable4.label.setText("m2 Brüt")

        self.variable5 = Variables_Line_Edit()
        self.variable5.label.setText("m2 Net")

        self.variable6 = Variables_Combo()
        self.variable6.label.setText("Oda")
        oda_values = ["1+0","1+1","2+0","2+1","3+1","3+2","4+1","4+2","5+1","5+2","6+1","6+2","7+1"]
        for i in oda_values:
            self.variable6.combobox.addItem(i)

        self.variable7 = Variables_Line_Edit()
        self.variable7.label.setText("Bina Yaşı")

        self.variable8 = Variables_Combo()
        self.variable8.label.setText("Bulunduğu kat")
        kat_values = ["kot 4","kot 3","kot 2","kot 1","zemin kat","giriş katı","yüksek giriş","bahçe katı","müstakil","çatı katı","villa tipi","bodrum kat","1","2","3","4","5",
        "6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30 ve üzeri"]
        for i in kat_values:
            self.variable8.combobox.addItem(i)

        self.variable9 = Variables_Line_Edit()
        self.variable9.label.setText("Bina Kat Sayısı")

        self.variable10 = Variables_Combo()
        self.variable10.label.setText("Isıtma")
        ısıtma_values = ["doğalgaz","merkezi","klima","yerden isıtma","soba","doğalgaz sobası","kat kaloriferi","güneş enerjisi","jeotermal","isı pompası","şömine","vrv","yok"]
        for i in ısıtma_values:
            self.variable10.combobox.addItem(i)

        self.variable11 = Variables_Line_Edit()
        self.variable11.label.setText("Banyo Sayısı")

        self.variable12 = Variables_Combo()
        self.variable12.label.setText("Balkon")
        self.variable12.combobox.addItem("var")
        self.variable12.combobox.addItem("yok")

        self.variable13 = Variables_Combo()
        self.variable13.label.setText("Eşyalı")
        self.variable13.combobox.addItem("evet")
        self.variable13.combobox.addItem("hayır")

        self.variable14 = Variables_Combo()
        self.variable14.label.setText("Kullanim Durumu")
        self.variable14.combobox.addItem("boş")
        self.variable14.combobox.addItem("mülk sahibi")
        self.variable14.combobox.addItem("kiracılı")

        self.variable15 = Variables_Combo()
        self.variable15.label.setText("Site İçerisinde")
        self.variable15.combobox.addItem("evet")
        self.variable15.combobox.addItem("hayır")

        self.variable16 = Variables_Combo()
        self.variable16.label.setText("Krediye Uygun")
        self.variable16.combobox.addItem("evet")
        self.variable16.combobox.addItem("hayır")

        self.variable17 = Variables_Combo()
        self.variable17.label.setText("Kimden")
        self.variable17.combobox.addItem("emlak ofisinden")
        self.variable17.combobox.addItem("sahibinden")
        self.variable17.combobox.addItem("inşaat firmasından")
        self.variable17.combobox.addItem("bankadan")

        self.variable18 = Variables_Combo()
        self.variable18.label.setText("Takas")
        self.variable18.combobox.addItem("evet")
        self.variable18.combobox.addItem("hayır")

        self.line = QFrame()
        self.line.setFixedSize(600,2)
        self.line.setStyleSheet('border:2px solid black;')

        self.line2 = QFrame()
        self.line2.setFixedSize(600,2)
        self.line2.setStyleSheet('border:2px solid black;')

        self.calculate_button = QtWidgets.QPushButton("Calculate")
        self.calculate_button.clicked.connect(self.predict)
        self.calculate_button.setStyleSheet("background-color:white;border-radius:5px;color:gray;border:2px solid gray")
        self.calculate_button.setFont(QtGui.QFont("sans-serif",13))
        self.calculate_button.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.calculate_button.setMinimumSize(250,40)
        self.calculate_button.setEnabled(False)

        self.predicted_value = QtWidgets.QLabel()
        self.predicted_value.setFont(QtGui.QFont("times-new-roman",20))

        self.app_layouts()

    def app_layouts(self):
        spacer = QtWidgets.QSpacerItem(0,30)
        spacer2 = QtWidgets.QSpacerItem(0,30)
        spacer3 = QtWidgets.QSpacerItem(0,30)
        spacer4 = QtWidgets.QSpacerItem(0,30)

        logo_layout = QtWidgets.QVBoxLayout()
        logo_layout.addWidget(self.app_logo)
        logo_layout.addStretch()

        grid_layout = QtWidgets.QGridLayout()
        grid_layout.addWidget(self.variable1, 0, 0)
        grid_layout.addWidget(self.variable2, 0, 1)
        grid_layout.addWidget(self.variable3, 0, 2)
        grid_layout.addWidget(self.variable4, 1, 0)
        grid_layout.addWidget(self.variable5, 1, 1)
        grid_layout.addWidget(self.variable6, 1, 2)
        grid_layout.addWidget(self.variable7, 2, 0)
        grid_layout.addWidget(self.variable8, 2, 1)
        grid_layout.addWidget(self.variable9, 2, 2)
        grid_layout.addWidget(self.variable10, 3, 0)
        grid_layout.addWidget(self.variable11, 3, 1)
        grid_layout.addWidget(self.variable12, 3, 2)
        grid_layout.addWidget(self.variable13, 4, 0)
        grid_layout.addWidget(self.variable14, 4, 1)
        grid_layout.addWidget(self.variable15, 4, 2)
        grid_layout.addWidget(self.variable16, 5, 0)
        grid_layout.addWidget(self.variable17, 5, 1)
        grid_layout.addWidget(self.variable18, 5, 2)

        centre_layout = QtWidgets.QVBoxLayout()
        centre_layout.addWidget(self.header,alignment=QtCore.Qt.AlignCenter)  
        centre_layout.addItem(spacer4)
        centre_layout.addWidget(self.line,alignment=QtCore.Qt.AlignCenter)     
        centre_layout.addLayout(grid_layout) 
        centre_layout.addItem(spacer)
        centre_layout.addWidget(self.calculate_button,alignment=QtCore.Qt.AlignCenter)     
        centre_layout.addItem(spacer2)
        centre_layout.addWidget(self.line2,alignment=QtCore.Qt.AlignCenter) 
        centre_layout.addItem(spacer3)
        centre_layout.addWidget(self.predicted_value,alignment=QtCore.Qt.AlignCenter)
        centre_layout.addStretch()

        time_layout = QtWidgets.QVBoxLayout()
        time_layout.addWidget(self.current_time,alignment=QtCore.Qt.AlignTop)
        time_layout.addStretch()

        main_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(logo_layout)
        main_layout.addStretch()
        main_layout.addLayout(centre_layout)
        main_layout.addStretch()
        main_layout.addLayout(time_layout)        

        self.setLayout(main_layout)
        self.show()

app = QtWidgets.QApplication(sys.argv)
application = Main_Page()
sys.exit(app.exec_())