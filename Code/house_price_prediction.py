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
        "ankara":["akyurt","alt??nda??","??ankaya","??ubuk","etimesgut","g??lba????","kahramankazan","ke??i??ren","mamak","polatl??","pursaklar","sincan","yenimahalle"],
        "antalya":["akseki","aksu","alanya","d????emealt??","finike","gazipa??a","ka??","kemer","kepez","konyaalt??","korkuteli","manavgat","muratpa??a","serik"],
        "gaziantep":["islahiye","nizip","nurda????","o??uzeli","yavuzeli","??ahinbey","??ehitkamil"],
        "istanbul":['arnavutk??y','ata??ehir','avc??lar','ba??c??lar','bah??elievler','bak??rk??y','ba??ak??ehir','beylikd??z??','bayrampa??a','beyo??lu','be??ikta??','b??y??k??ekmece','??ekmek??y','esenler','esenyurt','ey??psultan','fatih','gaziosmanpa??a','g??ng??ren','kad??k??y','kartal','ka????thane','k??????k??ekmece','maltepe','pendik','sancaktepe','sar??yer','silivri','sultanbeyli','sultangazi','??ile','??i??li','tuzla','??mraniye','??sk??dar','zeytinburnu'],
        "izmir":['alia??a','bal??ova','bayrakl??','bergama','bornova','buca','??e??me','??i??li','dikili','fo??a','gaziemir','g??zelbah??e','karaba??lar','karaburun','kar????yaka','kemalpa??a','kiraz','konak','k??n??k','menderes','menemen','narl??dere','??demi??','seferihisar','sel??uk','tire','torbal??','urla'],
        "konya":['ak??ehir','bey??ehir','cihanbeyli','??umra','ere??li','ilg??n','kad??nhan??','karap??nar','karatay','kulu','meram','saray??n??','sel??uklu','seydi??ehir'],
        "mersin":['akdeniz','anamur','bozyaz??','erdemli','g??lnar','mezitli','mut','silifke','tarsus','toroslar','yeni??ehir'],
        "mu??la":['bodrum','dalaman','dat??a','fethiye','k??yce??iz','marmaris','mente??e','milas','ortaca','seydikemer','ula','yata??an'],
        "??anl??urfa":['ak??akale','birecik','ceylanp??nar','eyy??biye','halfeti','haliliye','hilvan','karak??pr??','siverek','suru??','viran??ehir'],
        "trabzon":['ak??aabat','arakl??','arsin','be??ikd??z??','dernekpazar??','??ar????ba????','??aykara','ma??ka','of','ortahisar','s??rmene','??alpazar??','vakf??kebir','yomra'],
        "van":['edremit','erci??','ipekyolu','tu??ba']}

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
        self.il_labels = {'ankara': 0, 'antalya': 1, 'bursa': 2, 'gaziantep': 3, 'istanbul': 4, 'izmir': 5, 'konya': 6, 'mersin': 7, 'mu??la': 8, 'trabzon': 9, 'van': 10, '??anl??urfa': 11}
        self.ilce_labels = {'akdeniz': 0, 'akseki': 1, 'aksu': 2, 'akyurt': 3, 'ak??aabat': 4, 'ak??akale': 5, 'ak??ehir': 6, 'alanya': 7, 'alia??a': 8, 'alt??nda??': 9, 'anamur': 10, 'arakl??': 11, 'arnavutk??y': 12, 'arsin': 13, 'ata??ehir': 14, 'avc??lar': 15, 'bah??elievler': 16, 'bak??rk??y': 17, 'bal??ova': 18, 'bayrakl??': 19, 'bayrampa??a': 20, 'ba??c??lar': 21, 'ba??ak??ehir': 22, 'bergama': 23, 'beylikd??z??': 24, 'beyo??lu': 25, 'bey??ehir': 26, 'be??ikd??z??': 27, 'be??ikta??': 28, 'birecik': 29, 'bodrum': 30, 'bornova': 31, 'bozyaz??': 32, 'buca': 33, 'b??y??k??ekmece': 34, 'ceylanp??nar': 35, 'cihanbeyli': 36, 'dalaman': 37, 'dat??a': 38, 'dernekpazar??': 39, 'dikili': 40, 'd????emealt??': 41, 'edremit': 42, 'erci??': 43, 'erdemli': 44, 'ere??li': 45, 'esenler': 46, 'esenyurt': 47, 'etimesgut': 48, 'eyy??biye': 49, 'ey??psultan': 50, 'fatih': 51, 'fethiye': 52, 'finike': 53, 'fo??a': 54, 'gaziemir': 55, 'gaziosmanpa??a': 56, 'gazipa??a': 57, 'gemlik': 58, 'g??lba????': 59, 'g??lnar': 60, 'g??ng??ren': 61, 'g??rsu': 62, 'g??zelbah??e': 63, 'halfeti': 64, 'haliliye': 65, 'hilvan': 66, 'ilg??n': 67, 'ineg??l': 68, 'ipekyolu': 69, 'islahiye': 70, 'iznik': 71, 'kad??k??y': 72, 'kad??nhan??': 73, 'kahramankazan': 74, 'karaba??lar': 75, 'karaburun': 76, 'karacabey': 77, 'karak??pr??': 78, 'karap??nar': 79, 'karatay': 80, 'kartal': 81, 'kar????yaka': 82, 'ka????thane': 83, 'ka??': 84, 'kemalpa??a': 85, 'kemer': 86, 'kepez': 87, 'kestel': 88, 'ke??i??ren': 89, 'kiraz': 90, 'konak': 91, 'konyaalt??': 92, 'korkuteli': 93, 'kulu': 94, 'k??yce??iz': 95, 'k??????k??ekmece': 96, 'k??n??k': 97, 'maltepe': 98, 'mamak': 99, 'manavgat': 100, 'marmaris': 101, 'ma??ka': 102, 'menderes': 103, 'menemen': 104, 'mente??e': 105, 'meram': 106, 'mezitli': 107, 'milas': 108, 'mudanya': 109, 'muratpa??a': 110, 'mustafakemalpa??a': 111, 'mut': 112, 'narl??dere': 113, 'nil??fer': 114, 'nizip': 115, 'nurda????': 116, 'of': 117, 'orhangazi': 118, 'ortaca': 119, 'ortahisar': 120, 'osmangazi': 121, 'o??uzeli': 122, 'pendik': 123, 'polatl??': 124, 'pursaklar': 125, 'sancaktepe': 126, 'saray??n??': 127, 'sar??yer': 128, 'seferihisar': 129, 'sel??uk': 130, 'sel??uklu': 131, 'serik': 132, 'seydikemer': 133, 'seydi??ehir': 134, 'silifke': 135, 'silivri': 136, 'sincan': 137, 'siverek': 138, 'sultanbeyli': 139, 'sultangazi': 140, 'suru??': 141, 's??rmene': 142, 'tarsus': 143, 'tire': 144, 'torbal??': 145, 'toroslar': 146, 'tuzla': 147, 'tu??ba': 148, 'ula': 149, 'urla': 150, 'vakf??kebir': 151, 'viran??ehir': 152, 'yata??an': 153, 'yavuzeli': 154, 'yenimahalle': 155, 'yeni??ehir': 156, 'yomra': 157, 'y??ld??r??m': 158, 'zeytinburnu': 159, '??ankaya': 160, '??ar????ba????': 161, '??aykara': 162, '??ekmek??y': 163, '??e??me': 164, '??i??li': 165, '??ubuk': 166, '??umra': 167, '??demi??': 168, '??mraniye': 169, '??sk??dar': 170, '??ahinbey': 171, '??alpazar??': 172, '??ehitkamil': 173, '??ile': 174, '??i??li': 175}
        self.emlak_tipi_labels = {'daire': 0, 'residence': 1, 'yazl??k': 2}
        self.bulundugu_kat_labels = {'1': 0, '10': 1, '11': 2, '12': 3, '13': 4, '14': 5, '15': 6, '16': 7, '17': 8, '18': 9, '2': 10, '20': 11, '21': 12, '22': 13, '23': 14, '24': 15, '3': 16, '30 ve ??zeri': 17, '4': 18, '5': 19, '6': 20, '7': 21, '8': 22, '9': 23, 'bah??e kat??': 24, 'bodrum kat': 25, 'giri?? kat??': 26, 'kot 1': 27, 'kot 2': 28, 'kot 3': 29, 'kot 4': 30, 'm??stakil': 31, 'villa tipi': 32, 'y??ksek giri??': 33, 'zemin kat': 34, '??at?? kat??': 35}
        self.isitma_labels = {'do??algaz': 0, 'do??algaz sobas??': 1, 'g??ne?? enerjisi': 2, 'is?? pompas??': 3, 'jeotermal': 4, 'kat kaloriferi': 5, 'klima': 6, 'merkezi': 7, 'soba': 8, 'vrv': 9, 'yerden is??tma': 10, 'yok': 11, '????mine': 12}
        self.balkon_labels = {'var': 0, 'yok': 1}
        self.esyali_labels = {'evet': 0, 'hay??r': 1}
        self.kullanim_durumu_labels = {'bo??': 0, 'kirac??l??': 1, 'm??lk sahibi': 2}
        self.site_icerisinde_labels = {'evet': 0, 'hay??r': 1}
        self.krediye_uygun_labels = {'evet': 0, 'hay??r': 1}
        self.kimden_labels = {'bankadan': 0, 'emlak ofisinden': 1, 'in??aat firmas??ndan': 2, 'sahibinden': 3}
        self.takas_labels = {'evet': 0, 'hay??r': 1}

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
        self.variable1.label.setText("??l")
        il_values = ["ankara","antalya","gaziantep","istanbul","izmir","konya","mersin","mu??la","??anl??urfa","trabzon","van"]
        for i in il_values:
            self.variable1.combobox.addItem(i)

        self.variable2 = Variables_Combo()
        self.variable2.label.setText("??l??e")
        self.variable2.combobox.setEnabled(False)

        self.variable3 = Variables_Combo()
        self.variable3.label.setText("Emlak Tipi")
        self.variable3.combobox.addItem("daire")
        self.variable3.combobox.addItem("yazl??k")
        self.variable3.combobox.addItem("residence")

        self.variable4 = Variables_Line_Edit()
        self.variable4.label.setText("m2 Br??t")

        self.variable5 = Variables_Line_Edit()
        self.variable5.label.setText("m2 Net")

        self.variable6 = Variables_Combo()
        self.variable6.label.setText("Oda")
        oda_values = ["1+0","1+1","2+0","2+1","3+1","3+2","4+1","4+2","5+1","5+2","6+1","6+2","7+1"]
        for i in oda_values:
            self.variable6.combobox.addItem(i)

        self.variable7 = Variables_Line_Edit()
        self.variable7.label.setText("Bina Ya????")

        self.variable8 = Variables_Combo()
        self.variable8.label.setText("Bulundu??u kat")
        kat_values = ["kot 4","kot 3","kot 2","kot 1","zemin kat","giri?? kat??","y??ksek giri??","bah??e kat??","m??stakil","??at?? kat??","villa tipi","bodrum kat","1","2","3","4","5",
        "6","7","8","9","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30 ve ??zeri"]
        for i in kat_values:
            self.variable8.combobox.addItem(i)

        self.variable9 = Variables_Line_Edit()
        self.variable9.label.setText("Bina Kat Say??s??")

        self.variable10 = Variables_Combo()
        self.variable10.label.setText("Is??tma")
        ??s??tma_values = ["do??algaz","merkezi","klima","yerden is??tma","soba","do??algaz sobas??","kat kaloriferi","g??ne?? enerjisi","jeotermal","is?? pompas??","????mine","vrv","yok"]
        for i in ??s??tma_values:
            self.variable10.combobox.addItem(i)

        self.variable11 = Variables_Line_Edit()
        self.variable11.label.setText("Banyo Say??s??")

        self.variable12 = Variables_Combo()
        self.variable12.label.setText("Balkon")
        self.variable12.combobox.addItem("var")
        self.variable12.combobox.addItem("yok")

        self.variable13 = Variables_Combo()
        self.variable13.label.setText("E??yal??")
        self.variable13.combobox.addItem("evet")
        self.variable13.combobox.addItem("hay??r")

        self.variable14 = Variables_Combo()
        self.variable14.label.setText("Kullanim Durumu")
        self.variable14.combobox.addItem("bo??")
        self.variable14.combobox.addItem("m??lk sahibi")
        self.variable14.combobox.addItem("kirac??l??")

        self.variable15 = Variables_Combo()
        self.variable15.label.setText("Site ????erisinde")
        self.variable15.combobox.addItem("evet")
        self.variable15.combobox.addItem("hay??r")

        self.variable16 = Variables_Combo()
        self.variable16.label.setText("Krediye Uygun")
        self.variable16.combobox.addItem("evet")
        self.variable16.combobox.addItem("hay??r")

        self.variable17 = Variables_Combo()
        self.variable17.label.setText("Kimden")
        self.variable17.combobox.addItem("emlak ofisinden")
        self.variable17.combobox.addItem("sahibinden")
        self.variable17.combobox.addItem("in??aat firmas??ndan")
        self.variable17.combobox.addItem("bankadan")

        self.variable18 = Variables_Combo()
        self.variable18.label.setText("Takas")
        self.variable18.combobox.addItem("evet")
        self.variable18.combobox.addItem("hay??r")

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