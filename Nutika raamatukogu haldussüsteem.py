import csv # CSV failidega töötamine (tabelid)
import os # failide olemasolu kontrollimine
from datetime import datetime # praeguse kuupäeva ja aja saamine

# Failide nimed, kus andmed salvestatakse
RAAMATUD_FAIL = "raamatud.csv"
KASUTAJAD_FAIL = "kasutajad.csv"
LAENUTUSED_FAIL = "laenutused.csv"

# ------------------ KLASSID ------------------

class Raamat:
     # Raamatu klass
    def __init__(self, raamatu_id, pealkiri, autor, saadaval="jah"):
        self.raamatu_id = raamatu_id
        self.pealkiri = pealkiri
        self.autor = autor
        self.saadaval = saadaval


class Kasutaja:
    # Kasutaja klass
    def __init__(self, kasutaja_id, nimi):
        self.kasutaja_id = kasutaja_id
        self.nimi = nimi


class Laenutus:
    # Laenutuse klass (raamatu laenamine)
    def __init__(self, kasutaja_id, raamatu_id, laenutuse_kuup, tagastus_kuup=""):
        self.kasutaja_id = kasutaja_id
        self.raamatu_id = raamatu_id
        self.laenutuse_kuup = laenutuse_kuup
        self.tagastus_kuup = tagastus_kuup
        
# ------------------ FAILIDE LOOMINE ------------------

def loo_failid():
    # Kui raamatute fail puudub, loome selle
    if not os.path.exists(RAAMATUD_FAIL):
        with open(RAAMATUD_FAIL, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "pealkiri", "autor", "saadaval"])
            
# Kui kasutajate fail puudub, loome selle
    if not os.path.exists(KASUTAJAD_FAIL):
        with open(KASUTAJAD_FAIL, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "nimi"])
# Kui laenutuste fail puudub, loome selle
    if not os.path.exists(LAENUTUSED_FAIL):
        with open(LAENUTUSED_FAIL, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["kasutaja_id", "raamatu_id", "laenutuse_kuup", "tagastus_kuup"])

# ------------------ RAAMATUD ------------------

def lisa_raamat():
    # Uue raamatu lisamine
    raamatu_id = input("Sisesta raamatu ID: ")
    pealkiri = input("Sisesta pealkiri: ")
    autor = input("Sisesta autor: ")

    # Salvestame raamatu faili
    with open(RAAMATUD_FAIL, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([raamatu_id, pealkiri, autor, "jah"])

    print("Raamat lisatud!")


def kuva_raamatud():
    # Kuvab kõik raamatud
    with open(RAAMATUD_FAIL, "r") as f:
        reader = csv.reader(f)
        next(reader)
        print("\nRaamatud:")
        for rida in reader:
            print(rida)

# ------------------ KASUTAJAD ------------------

def lisa_kasutaja():
    # Uue kasutaja lisamine
    kasutaja_id = input("Sisesta kasutaja ID: ")
    nimi = input("Sisesta nimi: ")

    with open(KASUTAJAD_FAIL, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([kasutaja_id, nimi])

    print("Kasutaja lisatud!")

# ------------------ LAENUTAMINE ------------------

def laenuta_raamat():
    # Raamatu laenutamine
    kasutaja_id = input("Sisesta kasutaja ID: ")
    raamatu_id = input("Sisesta raamatu ID: ")

    raamatud = [] # kõigi raamatute loend
    leitud = False # kas raamat leiti ja oli saadaval
 
# kontrollime, kas raamat on saadaval
    with open(RAAMATUD_FAIL, "r") as f:
        reader = csv.reader(f)
        next(reader)
        for rida in reader:
            if rida[0] == raamatu_id and rida[3] == "jah":
                rida[3] = "ei"
                leitud = True
            raamatud.append(rida)

    if not leitud:
        print("Raamat ei ole saadaval!")
        return
        
# salvestame uuendatud raamatud
    with open(RAAMATUD_FAIL, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "pealkiri", "autor", "saadaval"])
        writer.writerows(raamatud)

    # lisame laenutuse kirje
    with open(LAENUTUSED_FAIL, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([kasutaja_id, raamatu_id, datetime.now(), ""])

    print("Raamat laenutatud!")


def tagasta_raamat():
    # Raamatu tagastamine
    raamatu_id = input("Sisesta tagastatava raamatu ID: ")

    raamatud = []

    # muudame raamatu uuesti saadavaks
    with open(RAAMATUD_FAIL, "r") as f:
        reader = csv.reader(f)
        next(reader)
        for rida in reader:
            if rida[0] == raamatu_id:
                rida[3] = "jah"
            raamatud.append(rida)

    # salvestame muudatused
    with open(RAAMATUD_FAIL, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "pealkiri", "autor", "saadaval"])
        writer.writerows(raamatud)

    laenutused = []

    # leiame laenutuse ja lisame tagastuse kuupäeva
    with open(LAENUTUSED_FAIL, "r") as f:
        reader = csv.reader(f)
        next(reader)
        for rida in reader:
            if rida[1] == raamatu_id and rida[3] == "":
                rida[3] = datetime.now()
            laenutused.append(rida)

    # salvestame laenutused uuesti
    with open(LAENUTUSED_FAIL, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["kasutaja_id", "raamatu_id", "laenutuse_kuup", "tagastus_kuup"])
        writer.writerows(laenutused)

    print("Raamat tagastatud!")

# ------------------ MENÜÜ ------------------

def menuu():
    # programmi peamenüü
    while True:
        print("\n--- RAAMATUKOGU SÜSTEEM ---")
        print("1. Lisa raamat")
        print("2. Kuva raamatud")
        print("3. Lisa kasutaja")
        print("4. Laenuta raamat")
        print("5. Tagasta raamat")
        print("0. Välju")

        valik = input("Vali: ")

        # kasutaja valiku töötlemine
        if valik == "1":
            lisa_raamat()
        elif valik == "2":
            kuva_raamatud()
        elif valik == "3":
            lisa_kasutaja()
        elif valik == "4":
            laenuta_raamat()
        elif valik == "5":
            tagasta_raamat()
        elif valik == "0":
            break
        else:
            print("Vale valik!")

# ------------------ PROGRAMMI KÄIVITUS ------------------

if __name__ == "__main__":
    loo_failid()
    menuu()
