def export_current_code(file_name):
    # Obtener el c�digo fuente del m�dulo actual
    current_code = inspect.getsource(inspect.currentframe().f_code)

    # Obtener el directorio actual
    current_directory = os.getcwd()

    # Unir el directorio actual con el nombre del archivo
    file_path = os.path.join(current_directory, file_name)

    # Escribir el c�digo en el archivo especificado
    with open(file_path, 'w') as file:
        file.write(current_code)
