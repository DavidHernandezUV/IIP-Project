import os
import shutil
import tkinter as tk
from tkinter import filedialog
import nibabel as nib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.algorithms.algorithmsCollection import algorithmsCollection
import copy as copy
import numpy as np
# GLOBAL VARIABLES
z_layer = 1
image = None
segmentation = None
image_to_pair_registration = None
image_to_histogram_matching = None
max_depth = 0
slider = None
algorithm_selected = ""
denoise_selected = ""
standarization_selected = ""
type_of_transform = ""
file_listbox = None
hist_condition = 0

#metrics
gray_matter_volume = 0
white_matter_volume = 0
liquid_volume = 0

BG_COLOR = "white"
HIST_SIZE = (3, 3)
SEG_SIZE = (4, 4)


def select_image_to_registration():
    global image_to_pair_registration

    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "T1.nii.gz")])
    if file_path:
        # Mover el archivo seleccionado a la carpeta "data"
        nifti_image = nib.load(file_path)
        image_to_pair_registration = nifti_image.get_fdata()
        print("Archivo guardado en la carpeta 'data'")


def select_file():
    global image
    global segmentation
    global max_depth
    global slider
    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.nii.gz")])
    if file_path:
        # Mover el archivo seleccionado a la carpeta "data"
        shutil.copy(file_path, "data")
        nifti_image = nib.load(file_path)
        image = nifti_image.get_fdata()
        segmentation = copy.deepcopy(image)
        max_depth = image.shape[2]
        print("Archivo guardado en la carpeta 'data'")
        # Actualizar el rango del slider
        slider.config(to=max_depth)
        slider.set(1)  # Restablecer el valor del slider a 1
        # Agregar el archivo a la lista de archivos
        file_listbox.insert(tk.END, os.path.basename(file_path))
    draw_image(segmentation)
    drawHistogram()


def select_algorithm(choice):
    global algorithm_selected
    algorithm_selected = choice
    draw_params()
    print("clicked:", algorithm_selected)

def select_type_of_transform(choice):
    global type_of_transform
    global image
    type_of_transform = choice
    draw_params()
    print("clicked:", type_of_transform)

def select_denoise(choice):
    global denoise_selected
    denoise_selected = choice
    print("clicked:", denoise_selected)


def select_standarization(choice):
    global standarization_selected
    standarization_selected = choice
    print("Clicked:", standarization_selected)


def select_image_to_matching():
    global image_to_histogram_matching

    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.nii.gz")])
    if file_path:
        # Mover el archivo seleccionado a la carpeta "data"
        nifti_image = nib.load(file_path)
        image_to_histogram_matching = nifti_image.get_fdata()
        print("Archivo guardado en la carpeta 'data'")


def draw_params():
    # Limpiar el frame_segmentation
    for widget in frame_params.winfo_children():
        widget.destroy()

    input_tol = None
    input_tau = None
    input_groups = None
    input_x = None
    input_y = None
    input_z = None
    if algorithm_selected == "Thresholding":
        label_tol = tk.Label(master=frame_params,
                             text="Tolerancia:", bg=BG_COLOR)
        label_tol.grid(row=0, column=0, padx=5, pady=5)
        input_tol = tk.Entry(master=frame_params)
        input_tol.grid(row=0, column=1, padx=5, pady=5)

        label_tau = tk.Label(master=frame_params,
                             text="Valor Tau:", bg=BG_COLOR)
        label_tau.grid(row=1, column=0, padx=5, pady=5)
        input_tau = tk.Entry(master=frame_params)
        input_tau.grid(row=1, column=1, padx=5, pady=5)

    if algorithm_selected == "K-means":
        label_groups = tk.Label(master=frame_params,
                                text="Grupos:", bg=BG_COLOR)
        label_groups.grid(row=0, column=0, padx=5, pady=5)
        input_groups = tk.Entry(master=frame_params)
        input_groups.grid(row=0, column=1, padx=5, pady=5)

    if algorithm_selected == "Region Growing":
        label_x = tk.Label(master=frame_params,
                           text="x:", bg=BG_COLOR)
        label_x.grid(row=0, column=0, padx=5, pady=5)
        input_x = tk.Entry(master=frame_params)
        input_x.grid(row=0, column=1, padx=5, pady=5)

        label_y = tk.Label(master=frame_params,
                           text="y:", bg=BG_COLOR)
        label_y.grid(row=1, column=0, padx=5, pady=5)
        input_y = tk.Entry(master=frame_params)
        input_y.grid(row=1, column=1, padx=5, pady=5)

        label_z = tk.Label(master=frame_params,
                           text="z:", bg=BG_COLOR)
        label_z.grid(row=2, column=0, padx=5, pady=5)
        input_z = tk.Entry(master=frame_params)
        input_z.grid(row=2, column=1, padx=5, pady=5)

        label_tol = tk.Label(master=frame_params,
                             text="tolerancia:", bg=BG_COLOR)
        label_tol.grid(row=0, column=2, padx=5, pady=5)
        input_tol = tk.Entry(master=frame_params)
        input_tol.grid(row=0, column=3, padx=5, pady=5)

    button_capture = tk.Button(master=frame_params, text="Segmentar",
                               command=lambda x=input_x, y=input_y, z=input_z, tol=input_tol, tau=input_tau, groups=input_groups: segmentate(x, y, z, tol, tau, groups))
    button_capture.grid(row=4, column=1, columnspan=2, padx=5, pady=5)


def denoise():
    global image
    global segmentation
    if denoise_selected == "Mean filter":
        image = algorithmsCollection.mean_filter(image)
    if denoise_selected == "Median filter":
        image = algorithmsCollection.median_filter(image)
    if denoise_selected == "Median Filter Borders":
        image = algorithmsCollection.meddian_filter_border(image)
    segmentation = copy.deepcopy(image)
    draw_image(segmentation)


def segmentate(input_x, input_y, input_z, input_tol, input_tau, input_groups):
    global image
    global segmentation
    if algorithm_selected == "Thresholding":
        tol_value = int(input_tol.get())
        tau_value = int(input_tau.get())
        segmentation = algorithmsCollection.thresholding(
            tol_value, tau_value, image)
    if algorithm_selected == "K-means":
        groups = int(input_groups.get())
        segmentation = algorithmsCollection.k_means(image, groups)
    if algorithm_selected == "Gaussian Mixture Model":
        segmentation = algorithmsCollection.gaussian_mixture_model(image)
    if algorithm_selected == "Region Growing":
        x = int(input_x.get())
        y = int(input_y.get())
        z = int(input_z.get())
        tol_value = int(input_tol.get())

        segmentation = algorithmsCollection.region_growing(
            x, y, z, tol_value, image)

    draw_image(segmentation)

def metrics():
    global segmentation
    final_img = nib.Nifti1Image(segmentation.astype(int), np.eye(4))
    final_img.header.set_data_dtype(np.float32)
    
    values = algorithmsCollection.metrics(final_img)
    print(values)
    # Simular la obtención de los nuevos valores dinámicamente
    nuevo_valor_gris = values[1.0]
    nuevo_valor_blanca = values[2.0]
    nuevo_valor_liquido = values[3.0]

    # Actualizar las variables de control con los nuevos valores
    materia_gris_var.set(nuevo_valor_gris)
    materia_blanca_var.set(nuevo_valor_blanca)
    liquido_var.set(nuevo_valor_liquido)

def registration():
    global image_to_pair_registration
    global image
    global type_of_transform
    global segmentation
    segmentation = algorithmsCollection.registration(image,image_to_pair_registration,type_of_transform)
    draw_image(segmentation)
    
def standarization():
    global image
    global segmentation
    global image_to_histogram_matching
    if standarization_selected == "Z-score":
        image = algorithmsCollection.z_score(image)
    if standarization_selected == "White Stripe":
        image = algorithmsCollection.white_stripe(image)
    if standarization_selected == "Rescaling":
        image = algorithmsCollection.rescaling(image)
    if standarization_selected == "Histogram Matching":
        image = algorithmsCollection.histogram_matching(image, image_to_histogram_matching, 50)

    segmentation = copy.deepcopy(image)
    draw_image(segmentation)
    drawHistogram()


def draw_image(segmentation):
    global canvas

    plt.close()
    if segmentation is None:
        print("Error al cargar la segmentation")
        return
    segmentation_section = segmentation[:, :, z_layer-1]

    canvas.get_tk_widget().destroy()

    fig, ax = plt.subplots(figsize=SEG_SIZE)
    canvas = FigureCanvasTkAgg(fig, master=frame_center)

    ax.imshow(segmentation_section, cmap="gray")
    canvas.draw()
    canvas.get_tk_widget().pack(expand=True)


def slider_event(value):
    global segmentation
    global z_layer
    z_layer = int(value)
    draw_image(segmentation)


def listbox_select_event(event):
    global image
    global segmentation
    selected_index = file_listbox.curselection()
    if selected_index:
        index = int(selected_index[0])
        selected_file = file_listbox.get(index)
        file_path = os.path.join("data", selected_file)
        nifti_image = nib.load(file_path)
        image = nifti_image.get_fdata()
        segmentation = copy.deepcopy(image)
        max_depth = image.shape[2]
        print(max_depth)
        slider.config(to=max_depth)
        slider.set(1)
        draw_image(segmentation)
        drawHistogram()


def change_conditional_value(new_value):
    global hist_condition
    hist_condition = new_value
    drawHistogram()


def drawHistogram():
    global image
    global hist
    global hist_condition
    hist.get_tk_widget().destroy()
    if image is None:
        print("Error al cargar la imagen")
        return
    hist.get_tk_widget().destroy()

    fig2, ax2 = plt.subplots(figsize=HIST_SIZE)
    fig2.subplots_adjust(left=0.35, bottom=0.25, right=0.75, top=0.75)
    hist = FigureCanvasTkAgg(fig2, master=frame_histogram)


    ax2.hist(image[image > hist_condition].flatten(), 100)

    hist.draw()

    hist.get_tk_widget().pack(expand=True, fill="both")

    # Ajustar los márgenes del histograma


root = tk.Tk()
root.title("Interfaz de Subida de Datos")
root.geometry("1200x800")
root.resizable(False, False)  # Bloquear redimensionamiento

# Estilo del borde
border_style = tk.SUNKEN

menubar = tk.Menu(root)
root.config(menu=menubar)

# Función para centrar y organizar verticalmente los componentes dentro del frame


def center_components(frame):
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_rowconfigure(1, weight=1)
    frame.grid_rowconfigure(2, weight=1)
    frame.grid_rowconfigure(3, weight=1)
    frame.grid_rowconfigure(4, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_columnconfigure(2, weight=1)
    frame.grid_columnconfigure(3, weight=1)

# FRAME LEFT
frame_left = tk.Frame(master=root, width=400, height=810, bg=BG_COLOR)
frame_left.pack(side="left", expand=300, fill=tk.BOTH)

# Files box
file_listbox = tk.Listbox(master=frame_left, width=45)
file_listbox.grid(padx=5,row=0,column=0)
file_listbox.bind("<<ListboxSelect>>", listbox_select_event)
# Menu "Archivos"
file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="Abrir", command=select_file)
file_menu.add_separator()
file_menu.add_command(label="Salir", command=root.quit)

menubar.add_cascade(label="Archivo", menu=file_menu)
# Crear las variables de control para los valores de los labels
materia_gris_var = tk.StringVar()
materia_blanca_var = tk.StringVar()
liquido_var = tk.StringVar()
#Metrics
frame_metrics = tk.LabelFrame(
    master=frame_left, text="Métricas", bg=BG_COLOR)
frame_metrics.grid(row=1, column=0, columnspan=4, sticky="we", padx=10)
button_metrics = tk.Button(master=frame_metrics, text="Aplicar",
                                command=lambda: metrics())
button_metrics.grid(padx=5, row=0, sticky="W")
tk.Label(master=frame_metrics,
         text="Volúmen Materia Gris: ", bg=BG_COLOR).grid(pady=5, row=1,sticky="W")
tk.Label(master=frame_metrics,
         text="Volúmen Materia Blanca: ", bg=BG_COLOR).grid(pady=5, row=2,sticky="W")
tk.Label(master=frame_metrics,
         text="Volúmen Líquido Cerebro Espinal: ", bg=BG_COLOR).grid(pady=5, row=3,sticky="W")
# Crear los labels dinámicos utilizando las variables de control
tk.Label(master=frame_metrics, textvariable=materia_gris_var, bg="white").grid(pady=5, row=1, column=1, sticky="W")
tk.Label(master=frame_metrics, textvariable=materia_blanca_var, bg="white").grid(pady=5, row=2, column=1, sticky="W")
tk.Label(master=frame_metrics, textvariable=liquido_var, bg="white").grid(pady=5, row=3, column=1, sticky="W")



center_components(frame_left)

# FRAME CENTER
frame_center = tk.Frame(master=root, width=600, height=800)
frame_center.pack(side="left", expand=600, fill=tk.BOTH, padx=20)
# PLOT
fig, ax = plt.subplots(figsize=SEG_SIZE)

canvas = FigureCanvasTkAgg(fig, master=frame_center)
canvas.get_tk_widget().pack(expand=True)

# SLIDER
frame_z_slider = tk.LabelFrame(
    master=frame_center, text="Capa Z")
frame_z_slider.pack(side="bottom", padx=10, pady=20)
slider = tk.Scale(master=frame_z_slider, from_=1, to=max_depth, resolution=1,
                  orient=tk.HORIZONTAL, command=slider_event)
slider.pack(pady=5)

# FRAME RIGHT
frame_right = tk.Frame(master=root, width=400, height=810, bg=BG_COLOR)
frame_right.pack(side="right", expand=400, fill=tk.BOTH)


# Registration
frame_registration = tk.LabelFrame(
    master=frame_right, text="Registro", bg=BG_COLOR)
frame_registration.grid(row=0, column=1, columnspan=4, sticky="we", padx=10)
type_of_transform_var = tk.StringVar()
type_of_transform_var.set("-")  # Valor inicial
type_of_transform_options = ["Rigid", "Similarity",
                          "QuickRigid", "SyN"]
button_add_t1 = tk.Button(master=frame_registration, text="Agregar T1",
                          command=lambda: select_image_to_registration())
button_add_t1.grid(padx=5, row=1, column=1, sticky="E", pady=10)
tk.Label(master=frame_registration,
         text="Transformación: ", bg=BG_COLOR).grid(pady=5, row=1, column=2)
type_of_transform_menu = tk.OptionMenu(
    frame_registration, type_of_transform_var, *type_of_transform_options, command=select_type_of_transform)
type_of_transform_menu.grid(pady=5, row=1, column=3)

button_registration = tk.Button(master=frame_registration, text="Aplicar",
                                command=lambda: registration())
button_registration.grid(padx=5, row=1, column=4, sticky="E", pady=10)


# PREPROCESSING (Denoising)
frame_denoising = tk.LabelFrame(
    master=frame_right, text="Remoción de ruido", bg=BG_COLOR)
frame_denoising.grid(row=1, column=1, columnspan=4, sticky="we", padx=10)

preprocessing_var = tk.StringVar()
preprocessing_var.set("-")
preprocessing_options = ["Mean filter",
                         "Median filter", "Median Filter Borders"]

tk.Label(master=frame_denoising, text="Denoising: ",
         bg=BG_COLOR).grid(pady=5, row=1, column=1)
preprocessing_menu = tk.OptionMenu(
    frame_denoising, preprocessing_var, *preprocessing_options, command=select_denoise)
preprocessing_menu.grid(pady=5, row=1, column=2)
button_denoising = tk.Button(master=frame_denoising, text="Aplicar",
                             command=lambda: denoise())
button_denoising.grid(padx=5, row=1, column=3, sticky="E")

# PROCESSING (Segmentation)
algorithm_var = tk.StringVar()
algorithm_var.set("-")  # Valor inicial
algorithm_options = ["Thresholding", "K-means",
                     "Region Growing", "Gaussian Mixture Model"]

frame_segmentation = tk.LabelFrame(
    master=frame_right, text="Segmentación", bg=BG_COLOR)
frame_segmentation.grid(row=2, column=1, columnspan=4, sticky="we", padx=10)

tk.Label(master=frame_segmentation,
         text="Segmentación: ", bg=BG_COLOR).grid(pady=5, row=1, column=1)
algorithm_menu = tk.OptionMenu(
    frame_segmentation, algorithm_var, *algorithm_options, command=select_algorithm)
algorithm_menu.grid(pady=5, row=1, column=2)

frame_params = tk.LabelFrame(
    master=frame_segmentation, text="Parámetros", bg=BG_COLOR)
frame_params.grid(pady=5, row=2, column=1, columnspan=2, sticky="we", padx=10)

# STANDARIZATION
standarization_var = tk.StringVar()
standarization_var.set("-")  # Valor inicial
standarization_options = ["Z-score", "White Stripe",
                          "Rescaling", "Histogram Matching"]

frame_standarization = tk.LabelFrame(
    master=frame_right, text="Estandarización", bg=BG_COLOR)
frame_standarization.grid(row=3, column=1, columnspan=4, sticky="we", padx=10)

tk.Label(master=frame_standarization,
         text="Estandarización: ", bg=BG_COLOR).grid(pady=5, row=1, column=1)
standarization_menu = tk.OptionMenu(
    frame_standarization, standarization_var, *standarization_options, command=select_standarization)
standarization_menu.grid(pady=5, row=1, column=2)
button_standarization = tk.Button(master=frame_standarization, text="Aplicar",
                                  command=lambda: standarization())
button_standarization.grid(padx=5, row=1, column=3, sticky="E")
button_add_image = tk.Button(master=frame_standarization,
                             text="Agregar", command=lambda: select_image_to_matching())
button_add_image.grid(padx=5, row=1, column=4, sticky="E", pady=10)
# HISTOGRAM
frame_histogram = tk.LabelFrame(
    master=frame_right, text="Histograma", bg=BG_COLOR,)
frame_histogram.grid(row=4, column=1, columnspan=4,
                     sticky="we", padx=10)

fig2, ax2 = plt.subplots(figsize=HIST_SIZE)
ax2.set_xlabel("Intensidad")
ax2.set_ylabel("Frecuencia")
# Ajustar los márgenes del histograma
fig2.subplots_adjust(left=0.25, bottom=0.25, right=0.75, top=0.75)
hist = FigureCanvasTkAgg(fig2, master=frame_histogram)
hist.get_tk_widget().pack(expand=True, fill="both")

frame_conditional_value = tk.LabelFrame(
    master=frame_histogram, text="Filtrar BG", bg=BG_COLOR)
frame_conditional_value.pack(side="bottom", padx=10, pady=20)
input_conditional_value = tk.Entry(master=frame_conditional_value)
input_conditional_value.grid(row=0, column=1, padx=5, pady=5)
button_conditional_value = tk.Button(master=frame_conditional_value,
                                     text="Aplicar", command=lambda: change_conditional_value(float(input_conditional_value.get())))
button_conditional_value.grid(padx=5, row=0, column=2, sticky="E", pady=10)

# Centrar y organizar verticalmente los componentes dentro de frame_right
center_components(frame_right)

# Crear la carpeta "data" si no existe
if not os.path.exists("data"):
    os.makedirs("data")

root.mainloop()
