from datetime import date

def get_today():
    today = date.today()
    # dd/mm/YY
    return(today.strftime("%d/%m/%Y"))

if __name__ == "__main__":
    pass