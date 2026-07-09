from flask import Flask, render_template, request
from ldap3 import Server, Connection, ALL, SIMPLE
import os

app = Flask(__name__)

LDAP_HOST = os.getenv('LDAP_HOST', 'ldap-server')
LDAP_BASE_DN = os.getenv('LDAP_BASE_DN', 'dc=login-ldap,dc=ra3,dc=localhost')

@app.route('/', methods=['GET', 'POST'])
def login():
    mensaje = None
    caso_true_false = None

    if request.method == 'POST':
        usuario = request.form.get('username')
        password = request.form.get('password')

        if usuario == "admin":
            user_dn = f"cn=admin,{LDAP_BASE_DN}"
        else:
            user_dn = f"cn={usuario},ou=usuarios,{LDAP_BASE_DN}"
        
        try:
            server = Server(LDAP_HOST, get_info=ALL)
            conn = Connection(server, user=user_dn, password=password, authentication=SIMPLE)
            
            if conn.bind():
                mensaje = "Usuario encontrado (caso True)"
                caso_true_false = True
                conn.unbind()
            else:
                mensaje = "Usuario no encontrado (caso False)"
                caso_true_false = False
        except Exception as e:
            mensaje = f"Error de conexión: {str(e)}"
            caso_true_false = False
            print(f"Error LDAP: {e}")  

    return render_template('login.html', mensaje=mensaje, caso_true_false=caso_true_false)

if __name__ == '__main__':
    # use_reloader=False evita bloqueos de red tanto en Windows (WSL2) como en Linux nativo
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
