# radar-analysis-app

### Instruktioner för analysis-app
Förutsatt att du har python och pip installerat

1. Öppna kommandofönster och navigera till mappen analysis_app
```
...\kandidatarbete-eenx15-20-03\analysis_app>
```
2. Aktivera virtual environment
```
...\analysis_app>venv\scripts\activate
```
3. Kör appen
```
(venv) ...\analysis_app>python src\app.py
```
4. Något i stil med följande kommer att skrivas ut:
```
Running on http://127.0.0.1:8050/
Debugger PIN: 804-687-657
 * Serving Flask app "config" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
Running on http://127.0.0.1:8050/
Debugger PIN: 117-473-131
```
5. Kopiera länken (http://...) och klistra in den i valfri webbläsare. Man får vara försiktig när man trycker `ctrl-c` för det kommandot, förutom att kopiera, avslutar appen från kommandofönstret.
