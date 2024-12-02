from PyQt6.QtWidgets import *
from gui import *
import csv

class Logic(QMainWindow, Ui_MainWindow):
    def __init__(self)->None:
        super().__init__()
        self.setupUi(self)
        self.submit_button.clicked.connect(lambda: self.submit() )
        self.submit_button = QRadioButton("Submit Vote")

    def clear(self)->None:
        """
        Function is used to clear text and uncheck the radio buttons
        :return: None
        """
        self.ID_line.clear()
        self.Outcome_label.clear()
        #Haven't been able to uncheck all of them yet!
        self.buttonGroup.setExclusive(False)
        self.Can1_radBut.setChecked(False)
        self.Cand2_radBut.setChecked(False)
        self.Cand3_radBut.setChecked(False)
        self.buttonGroup.setExclusive(True)

    def read(self, ID, Canidate)->None:
        """
        Function runs throught data.csv to see if the Voter ID is there, and if data.csv doens't exist, it will be created
        :param ID: Voter ID that will be used to see if it is unique and haven't voted yet
        :param Canidate: The candidate that a voter will be voting for
        :return: None
        """
        bad = False
        try:
            with open("data.csv", "r", newline='') as csv_file:
                csv_reader = csv.reader(csv_file)
                for row in csv_reader:
                    if ID in row:
                        raise ValueError
                        bad = True
                        self.clear()
                if bad == False:
                    self.Wr(ID, Canidate)

        except FileNotFoundError:
            with open("data.csv", "a", newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(["Voter ID", "Candidate"])
                csv_writer.writerow([ID, Canidate])

    def Wr(self, ID, Candidate) -> None:
        """
        Function writes the data in csv file
        :param ID: Voter ID that will be used to write row
        :param Candidate: The candidate that a voter will be voting for
        :return: None
        """
        with open("data.csv", "a", newline='') as csv_file:
            Row = ID, Candidate
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(Row)

    def submit(self) -> None:
        """
        Function is checking which candidate was selected, and is using exception handling to not crash the program
        :return: None
        """
        user_ID = self.ID_line.text().strip()
        checked = False
        try:
            if self.Can1_radBut.isChecked():
                candidate = 'Bianca'
                checked = True
            elif self.Cand2_radBut.isChecked():
                candidate = 'Edward'
                checked = True
            elif self.Cand3_radBut.isChecked():
                checked= True
                candidate = 'Felicia'
            if user_ID=='':
                raise UnboundLocalError
            self.read(user_ID, candidate)
            self.clear()
            self.Outcome_label.setText(f"Voted {candidate}")
            self.Outcome_label.setStyleSheet("color: green;")

        except ValueError:
            self.Outcome_label.setText("Already Voted")
            self.Outcome_label.setStyleSheet("color: red;")

        except UnboundLocalError:
            if user_ID == '' and checked == False:
                self.Outcome_label.setText("Enter Voter ID and select a Candidate")
                self.Outcome_label.setStyleSheet("color: red;")
            elif user_ID == '':
                self.Outcome_label.clear()
                self.Outcome_label.setText("Enter Voter ID")
                self.Outcome_label.setStyleSheet("color: red;")
            elif checked == False:
                self.Outcome_label.setText("Select a Candidate")
                self.Outcome_label.setStyleSheet("color: red;")
