from wsgi import app

def main():
    app.run(host="0.0.0.0", port=80)

if __name__ == '__main__':
    main()
