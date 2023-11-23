def export_current_code(file_name):
    # Obtener el código fuente del módulo actual
    current_code = inspect.getsource(inspect.currentframe().f_code)

    # Obtener el directorio actual
    current_directory = os.getcwd()

    # Unir el directorio actual con el nombre del archivo
    file_path = os.path.join(current_directory, file_name)

    # Escribir el código en el archivo especificado
    with open(file_path, 'w') as file:
        file.write(current_code)
