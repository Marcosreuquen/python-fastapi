#!/bin/bash

# Función para buscar los archivos .sh en la carpeta y sus subcarpetas
search_scripts() {
    find ./scripts -type f -name "*.sh" -print0 2>/dev/null | while read -d $'\0' script; do
        echo "${script#./scripts/}"
    done
}
# Función para ejecutar el script deseado
run_script() {
    script_path=$(find ./scripts -name "$1*.sh" -o -path "*/$1*.sh" | head -1)
    if [[ -z $script_path ]]; then
        echo "No se encontró el script $1"
        exit 1
    fi
    bash "$script_path" "${@:2}"
}

# Si no se especifica ningún argumento, mostrar la lista de scripts disponibles
if [[ $# -eq 0 ]]; then
    echo "Los siguientes scripts están disponibles:"
    search_scripts
    exit 0
fi

# Ejecutar el script deseado
run_script "$1" "${@:2}"
