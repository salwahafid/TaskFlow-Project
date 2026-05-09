from utils.validation import valider_email
from utils.constantes import A_FAIRE

def main():
    email = "test@gmail.com"

    if valider_email(email):
        print("Email valide")
    else:
        print("Email invalide")

    print("Statut par défaut :", A_FAIRE)


if __name__ == "__main__":
    main()