import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np
from tkinter import ttk

def verificar_tamano_valido():
    try:
        n = int(entry_tamano.get())
    except ValueError:
        # Si no se ingresó un número válido como tamaño, muestra un mensaje de error
        messagebox.showerror("Error", "Ingrese un tamaño de board válido.")
        return False
    return True

def generar_entradas():
    if verificar_tamano_valido():
        global estado_botones
        for boton in estado_botones:
            boton.destroy()  # Elimina los botones anteriores
        n = int(entry_tamano.get())  # Obtiene el tamaño del tablero ingresado por el usuario
        estado_botones = []  # Lista para almacenar los nuevos botones de estado
        for i in range(n * n):
            label = tk.Label(ventana, text="Estado de b" + str(i + 1) + ":")
            label.pack()
            boton = ttk.Button(ventana, text="0", command=lambda i=i: cambiar_estado(i))
            boton.pack()
            estado_botones.append(boton)

def cambiar_estado(i):
    estado_actual = estado_botones[i]["text"]
    nuevo_estado = "1" if estado_actual == "0" else "0"
    estado_botones[i]["text"] = nuevo_estado

def ejecutar_codigo_con_gui():
    if verificar_tamano_valido():
        n = int(entry_tamano.get())
        toro = int(var_toro.get())

        lista_con_n_listas = []
        lista_1 = []

        for i in range(n * n):
            lista_1.append(i + 1)
            if (i + 1) % n == 0:
                lista_con_n_listas.append(lista_1)
                lista_1 = []

        matriz = []
        list_cn_lists_d_btn = []

        # Esta sección se encarga de crear la matriz n*n x n*n
        for i_1 in range(n * n):
            list_cn_lists_d_btn.append(["b" + str(i_1 + 1)])
            lista_1 = []
            y_i_1 = 0
            x_i_1 = 0
            for i_2 in range(n):
                if (i_1 + 1) in lista_con_n_listas[i_2]:
                    y_i_1 = i_2 + 1
                    x_i_1 = (lista_con_n_listas[i_2]).index(i_1 + 1) + 1
            for i_2 in range(n * n):
                y_i_2 = 0
                x_i_2 = 0
                for i_3 in range(n):
                    if (i_2 + 1) in lista_con_n_listas[i_3]:
                        y_i_2 = i_3 + 1
                        x_i_2 = (lista_con_n_listas[i_3]).index(i_2 + 1) + 1
                if toro == 1:  # Para el modo toro
                    if i_1 == i_2:
                        lista_1.append(1)
                    elif x_i_1 == x_i_2 and (((y_i_2 == y_i_1 + 1) or (y_i_2 == y_i_1 - 1)) or ((y_i_2 == y_i_1 + 1 - n) or (y_i_2 == y_i_1 - 1 + n))):
                        lista_1.append(1)
                    elif y_i_1 == y_i_2 and (((x_i_2 == x_i_1 + 1) or (x_i_2 == x_i_1 - 1)) or ((x_i_2 == x_i_1 + 1 - n) or (x_i_2 == x_i_1 - 1 + n))):
                        lista_1.append(1)
                    else:
                        lista_1.append(0)
                else:  # Para el modo normal
                    if i_1 == i_2:
                        lista_1.append(1)
                    elif x_i_1 == x_i_2 and ((y_i_2 == y_i_1 + 1) or (y_i_2 == y_i_1 - 1)):
                        lista_1.append(1)
                    elif y_i_1 == y_i_2 and ((x_i_2 == x_i_1 + 1) or (x_i_2 == x_i_1 - 1)):
                        lista_1.append(1)
                    else:
                        lista_1.append(0)
            matriz.append(lista_1)

        # Crear el diccionario a partir de los estados de los botones
        diccionario = {}
        for i in range(n * n):
            estado = estado_botones[i]["text"]
            diccionario["b" + str(i + 1)] = int(estado)

        # Eliminación de unos
        for i_1 in range(n * n):
            a = 0
            while a < n * n:
                if 1 == (matriz[a])[i_1] and (1 not in (matriz[a])[:i_1]):
                    for i_2 in range(n * n):
                        if 1 == (matriz[i_2])[i_1] and (i_2 != a):
                            for i_3 in range(len(list_cn_lists_d_btn[a])):
                                bn = (list_cn_lists_d_btn[a])[i_3]
                                if bn in list_cn_lists_d_btn[i_2]:
                                    list_cn_lists_d_btn[i_2].remove(bn)
                                else:
                                    list_cn_lists_d_btn[i_2].append(bn)
                            for i_3 in range(n * n):
                                (matriz[i_2])[i_3] = ((matriz[i_2])[i_3] - (matriz[a])[i_3]) * -((matriz[a])[i_3] - (matriz[i_2])[i_3])
                    a = n * n
                a = a + 1

        # Cambio de filas
        for i_1 in range(n * n):
            a = 0
            while a < n * n:
                if 1 == (matriz[a])[i_1] and (1 not in (matriz[a])[:i_1]):
                    fila_buffer = matriz[i_1]
                    matriz[i_1] = matriz[a]
                    matriz[a] = fila_buffer

                    i, j = list_cn_lists_d_btn.index(list_cn_lists_d_btn[i_1]), list_cn_lists_d_btn.index(list_cn_lists_d_btn[a])
                    list_cn_lists_d_btn[i], list_cn_lists_d_btn[j] = list_cn_lists_d_btn[j], list_cn_lists_d_btn[i]

                    a = n * n
                a = a + 1

        # Crear una nueva ventana para mostrar los resultados
        resultados_ventana = tk.Toplevel(ventana)
        resultados_ventana.title("Resultados")

        resultado_text = ""
        for i_1 in range(n * n):
            suma = 0
            for i_2 in range(len(list_cn_lists_d_btn[i_1])):
                suma = suma + diccionario[(list_cn_lists_d_btn[i_1])[i_2]]
            if suma % 2 == 0:
                resultado_text += "b" + str(i_1 + 1) + ": 0\n"
            else:
                resultado_text += "b" + str(i_1 + 1) + ": 1\n"

        resultado_label = tk.Label(resultados_ventana, text=resultado_text, font=("Arial", 16))
        resultado_label.pack()

        # Crear una matriz gráfica para mostrar los resultados
        matriz_resultados = np.zeros((n, n), dtype=int)
        for i in range(n):
            for j in range(n):
                indice = i * n + j
                matriz_resultados[i][j] = diccionario["b" + str(indice + 1)]

        fig, ax = plt.subplots(figsize=(8, 8))
        ax.matshow(matriz_resultados, cmap="binary")
        ax.set_title("Matriz de Resultados")
        plt.show()

ventana = tk.Tk()
ventana.title("Aplicación con GUI")

label_tamano = tk.Label(ventana, text="Tamaño del board:")
label_tamano.pack()
entry_tamano = tk.Entry(ventana)
entry_tamano.pack()

boton_verificar_tamano = tk.Button(ventana, text="Verificar Tamaño", command=verificar_tamano_valido)
boton_verificar_tamano.pack()

var_toro = tk.IntVar()
var_toro.set(0)
toro_checkbox = tk.Checkbutton(ventana, text="Modo toro", variable=var_toro)
toro_checkbox.pack()

boton_generar_entradas = tk.Button(ventana, text="Generar Entradas", command=generar_entradas)
boton_generar_entradas.pack()

boton_ejecutar = tk.Button(ventana, text="Ejecutar Código", command=ejecutar_codigo_con_gui)
boton_ejecutar.pack()

estado_botones = []  # Lista para almacenar los botones de estado

ventana.mainloop()
