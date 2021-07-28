from backend import create_app, APP_ROOT

app = create_app(f'{APP_ROOT}/backend/config/testing.py')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
