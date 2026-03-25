# Python Automation Tests

Test Automation Suite della sezione Account con `pytest` e `Selenium`.


## Scenari coperti

- registrazione player
- registrazione organizer
- email già esistente
- display name già esistente
- password troppo corta
- login player
- login organizer
- login con credenziali errate
- logout
- persistenza sessione dopo refresh

## Prerequisiti

- TennisMatch up and running
- Python installato

## Installazione

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Esecuzione

```powershell
.\.venv\Scripts\pytest.exe tests\test_account.py -q
```


