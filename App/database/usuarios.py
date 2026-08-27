"""
Funciones relacionadas al usuario: crear cuenta, iniciar sesión,
actualizar racha y sumar puntos de experiencia (XP).
"""

import bcrypt
from datetime import date, timedelta
from database.conexion import obtener_conexion


def crear_usuario(nombre, apellidoP, apellidoM, nombreUsuario, edad, contrasena):
    """
    Registra un nuevo usuario en la base de datos.
    La contraseña se guarda hasheada, nunca en texto plano.

    Devuelve (True, "mensaje") si se creó correctamente,
    o (False, "mensaje de error") si algo falló (ej. usuario duplicado).
    """
    contrasena_hash = bcrypt.hashpw(contrasena.encode("utf-8"), bcrypt.gensalt())

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute("""
            INSERT INTO usuario (nombre, apellidoP, apellidoM, nombreUsuario, edad, contrasena_hash)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nombre, apellidoP, apellidoM, nombreUsuario, edad, contrasena_hash.decode("utf-8")))

        conexion.commit()
        return True, "Cuenta creada correctamente."

    except Exception as error:
        # UNIQUE constraint failed -> el nombre de usuario ya existe
        if "UNIQUE constraint failed" in str(error):
            return False, "Ese nombre de usuario ya está en uso."
        return False, f"Ocurrió un error al crear la cuenta: {error}"

    finally:
        conexion.close()


def verificar_login(nombreUsuario, contrasena):
    """
    Verifica las credenciales de un usuario.

    Devuelve el registro del usuario (sqlite3.Row) si las credenciales
    son correctas, o None si el usuario no existe o la contraseña es incorrecta.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM usuario WHERE nombreUsuario = ?", (nombreUsuario,))
    usuario = cursor.fetchone()
    conexion.close()

    if usuario is None:
        return None

    contrasena_correcta = bcrypt.checkpw(
        contrasena.encode("utf-8"),
        usuario["contrasena_hash"].encode("utf-8")
    )

    return usuario if contrasena_correcta else None


def actualizar_nombre_usuario(usuario_id, nuevo_nombreUsuario):
    """
    Permite cambiar el nombre de usuario (sigue siendo único).
    Devuelve (True, "mensaje") o (False, "mensaje de error").
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            "UPDATE usuario SET nombreUsuario = ? WHERE id = ?",
            (nuevo_nombreUsuario, usuario_id)
        )
        conexion.commit()
        return True, "Nombre de usuario actualizado."

    except Exception as error:
        if "UNIQUE constraint failed" in str(error):
            return False, "Ese nombre de usuario ya está en uso."
        return False, f"Ocurrió un error: {error}"

    finally:
        conexion.close()


def actualizar_racha_y_xp(usuario_id, xp_ganado=10):
    """
    Actualiza la racha de práctica y suma XP al usuario.
    Se debe llamar una vez por cada sesión de práctica (no por cada intento individual).

    Lógica de la racha:
    - Si ya practicó hoy: no cambia la racha (evita inflarla practicando varias veces el mismo día).
    - Si practicó ayer: +1 a la racha actual.
    - Si no practicó ayer (o es su primera vez): la racha se reinicia a 1.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT racha_actual, racha_maxima, ultima_practica FROM usuario WHERE id = ?",
        (usuario_id,)
    )
    fila = cursor.fetchone()

    if fila is None:
        conexion.close()
        return

    hoy = date.today()
    ultima_practica = (
        date.fromisoformat(fila["ultima_practica"]) if fila["ultima_practica"] else None
    )

    if ultima_practica == hoy:
        nueva_racha = fila["racha_actual"]
    elif ultima_practica == hoy - timedelta(days=1):
        nueva_racha = fila["racha_actual"] + 1
    else:
        nueva_racha = 1

    nueva_racha_maxima = max(nueva_racha, fila["racha_maxima"])

    cursor.execute("""
        UPDATE usuario
        SET racha_actual = ?, racha_maxima = ?, ultima_practica = ?, puntos_xp = puntos_xp + ?
        WHERE id = ?
    """, (nueva_racha, nueva_racha_maxima, hoy.isoformat(), xp_ganado, usuario_id))

    conexion.commit()
    conexion.close()