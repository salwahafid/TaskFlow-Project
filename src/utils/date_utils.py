from datetime import date, datetime

def jours_restants(date_echeance: date) -> int:

    aujourd_hui = date.today()
    difference = date_echeance - aujourd_hui
    return difference.days

def est_en_retard(date_echeance: date) -> bool:

    return jours_restants(date_echeance) < 0

def formater_date(d: date) -> str:

    return d.strftime("%d/%m/%Y")
if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)