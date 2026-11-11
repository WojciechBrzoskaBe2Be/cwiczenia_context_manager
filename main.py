class Logger:

    def __enter__(self):
        print("Start sekcji logowania")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Koniec sekcji logowania")
        return False


class FileWriter:

    def __init__(self, filepath: str, tlumienie_wyjatkow: bool = False):
        self.filepath = filepath
        self.file_handle = None
        self.tlumienie_wyjatkow = tlumienie_wyjatkow

    def __enter__(self):
        """
        zadaniem  __enter__ jest inicjalizacja zasobów oraz zwrócenie uchwytu do powstałgo obektu tu
        jest to uchwyt do obiektu którym jest plik.
        Otwieramy plik do zapisu ('w') z kodowaniem UTF-8 i zwracamy jego uchwyt
       """
        self.file_handle = open(self.filepath, "w", encoding="utf-8")
        return self.file_handle

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Zawsze zamykamy plik, nawet jeśli w bloku with wystąpił błąd
        if self.file_handle:
            self.file_handle.close()
        #czy bład będzie tłumiony?
        if self.tlumienie_wyjatkow:
            return True
        if exc_type:
            raise ValueError(f"Blok context manager: {exc_val} linia:{exc_tb.tb_lineno} ")
        # Zwrócenie False pozwala powyjątkom (jeśli wystąpiły) przejść dalej
        return False


class SafeDivision:

    def __enter__(self):
        return self

    def divide(self, a, b):
        return a / b

    def __exit__(self, exc_type, exc_val, exc_tb):
        # czy wystąpił błąd dzielenia przez zero?
        if exc_type is ZeroDivisionError:
            print(f"{46 * '*'}\n*Pamiętaj cholero nie dziel nigdy przez zero!*\n{46 * '*'}")
            return True  # Zwracamy True :czyli błąd nie spowoduje zakończenia działania programu
        # Inne wyjątki nie są tłumione
        return False


if __name__ == "__main__":
    #scenariusz błedu w bloku with ma być wywołany
    podziel_przez_0 = True
    # wskaż czy tlumic_bledy w klasie FileWriter
    bledy_beda_tlumione = True

    # Użycie w bloku with
    with Logger():
        print("Trwa przetwarzanie danych portfela AIFMD i sprawdzanie limitów...")

    plik_docelowy = "raport_testowy.txt"

    # Użycie klasy FileWriter w bloku with
    with FileWriter(filepath=plik_docelowy, tlumienie_wyjatkow=bledy_beda_tlumione) as f:
        f.write("Raport zgodności AIFMD - Test zapisu\n")
        if podziel_przez_0:
            1 / 0

        f.write("Status: OK\n")
        f.write("Wszystkie limity portfela zostały zweryfikowane pomyślnie.\n")

    print(f"Tekst został pomyślnie zapisany do pliku: {plik_docelowy}")

    #stlumienie błędu dzielenia przez 0
    with SafeDivision() as op:
        op.divide(1, 0)
