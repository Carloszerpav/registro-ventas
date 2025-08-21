from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1>¡Hola! Flask está funcionando correctamente</h1>'

if __name__ == '__main__':
    print("🚀 Iniciando prueba de Flask...")
    print("📱 Abre tu navegador en: http://localhost:5001")
    app.run(debug=True, port=5001)
