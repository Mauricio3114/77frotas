from app import create_app

print("1 - Importou create_app")

app = create_app()

print("2 - App criada")

if __name__ == "__main__":
    print("3 - Entrou no main")
    app.run(debug=True)
    print("4 - Terminou app.run")