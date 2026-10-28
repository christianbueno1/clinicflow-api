def validar_cedula_ecuador(cedula: str) -> bool:
    """
    Valida una cédula de identidad ecuatoriana de 10 dígitos
    siguiendo las normas del Registro Civil (Módulo 10).
    """
    # 1. Verificar que tenga exactamente 10 dígitos y sean numéricos
    if not isinstance(cedula, str) or not cedula.isdigit() or len(cedula) != 10:
        return False

    # 2. Verificar código de provincia (01 a 24, o 30 para el exterior)
    provincia = int(cedula[0:2])
    if not ((1 <= provincia <= 24) or provincia == 30):
        return False

    # 3. El tercer dígito debe ser menor a 6 (0 al 5) para personas naturales
    tercer_digito = int(cedula[2])
    if tercer_digito >= 6:
        return False

    # 4. Algoritmo Módulo 10 para el dígito verificador
    coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2]
    suma = 0

    for i in range(9):
        valor = int(cedula[i]) * coeficientes[i]
        if valor > 9:
            valor -= 9
        suma += valor

    # Calcular la decena superior inmediata
    decena_superior = ((suma + 9) // 10) * 10
    digito_verificador = decena_superior - suma

    if digito_verificador == 10:
        digito_verificador = 0

    # 5. Comparar con el décimo dígito proporcionado
    return digito_verificador == int(cedula[9])


if __name__ == "__main__":
    # Ejemplos de prueba
    test_cedulas = [
        "0928193821",
        "1710035544",
        "0999999999",
        "1234567890",
        "1303246399",
        "0924782121",
        "0955352620",
        "0901539189",
    ]
    for c in test_cedulas:
        print(f"Cédula {c}: {'Válida' if validar_cedula_ecuador(c) else 'Inválida'}")
