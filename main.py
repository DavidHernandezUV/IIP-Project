import os
import shutil
import tkinter as tk
from tkinter import filedialog
import nibabel as nib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from src.algorithms.algorithmsCollection import algorithmsCollection
# GLOBAL VARIABLES
z_layer = 1
image = None
max_depth = 0
slider = None
algorithm_selected = ""
denoise_selected = ""
file_listbox = None

BG_COLOR = "white"
HIST_SIZE = (2, 2)
SEG_SIZE = (4, 4)


def select_file():
    global image
    global max_depth
    global slider
    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.nii.gz")])
    if file_path:
        # Mover el archivo seleccionado a la carpeta "data"
        shutil.copy(file_path, "data")
        nifti_image = nib.load(file_path)
        image = nifti_image.get_fdata()
        max_depth = image.shape[2]
        print("Archivo guardado en la carpeta 'data'")
        # Actualizar el rango del slider
        slider.config(to=max_depth)
        slider.set(1)  # Restablecer el valor del slider a 1
        # Agregar el archivo a la lista de archivos
        file_listbox.insert(tk.END, os.path.basename(file_path))
    draw_image()
    drawHistogram()


def select_algorithm(choice):
    global algorithm_selected
    global image
    algorithm_selected = choice
    if (choice == "Thresholding"):
        segmentation = algorithmsCollection.thresholding(100, 30, image)
        image = segmentation
        draw_image()
    print("clicked:", algorithm_selected)


def select_denoise(choice):
    global denoise_selected
    denoise_selected = choice
    print("clicked:", denoise_selected)


def draw_image():
    global image
    global canvas

    plt.close()
    if image is None:
        print("Error al cargar la imagen")
        return
    image_section = image[:, :, z_layer-1]

    canvas.get_tk_widget().destroy()

    fig, ax = plt.subplots(figsize=SEG_SIZE)
    canvas = FigureCanvasTkAgg(fig, master=frame_center)

    ax.imshow(image_section, cmap="gray")
    canvas.draw()
    canvas.get_tk_widget().pack(expand=True)


def slider_event(value):
    global z_layer
    z_layer = int(value)
    draw_image()


def listbox_select_event(event):
    selected_index = file_listbox.curselection()
    if selected_index:
        index = int(selected_index[0])
        selected_file = file_listbox.get(index)
        file_path = os.path.join("data", selected_file)
        nifti_image = nib.load(file_path)
        global image
        image = nifti_image.get_fdata()
        max_depth = image.shape[2]
        print(max_depth)
        slider.config(to=max_depth)
        slider.set(1)
        draw_image()
        drawHistogram()


def drawHistogram():
    global image
    global hist

    if image is None:
        print("Error al cargar la imagen")
        return
    hist.get_tk_widget().destroy()

    fig2, ax2 = plt.subplots(figsize=HIST_SIZE)
    fig2.subplots_adjust(left=0.35, bottom=0.25, right=0.75, top=0.75)
    hist = FigureCanvasTkAgg(fig2, master=frame_right)

    ax2.hist(image[image > 10].flatten(), 200)
    hist.draw()

    hist.get_tk_widget().grid(row=4, column=2, columnspan=4)

    # Ajustar los márgenes del histograma


root = tk.Tk()
root.title("Interfaz de Subida de Datos")
root.geometry("1200x800")
root.resizable(False, False)  # Bloquear redimensionamiento

menubar = tk.Menu(root)
root.config(menu=menubar)

# FRAME LEFT
frame_left = tk.Frame(master=root, width=300, height=810, bg=BG_COLOR)
frame_left.pack(side="left")

# Files box label
label_listbox = tk.Label(master=frame_left, text="Datos", bg=BG_COLOR)
label_listbox.place(rely=0.002, relx=0.02)
# Files box
file_listbox = tk.Listbox(master=frame_left, width=45)
file_listbox.place(rely=0.03, relx=0.02)
file_listbox.bind("<<ListboxSelect>>", listbox_select_event)
# Menu "Archivos"
file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="Abrir", command=select_file)
file_menu.add_separator()
file_menu.add_command(label="Salir", command=root.quit)

menubar.add_cascade(label="Archivo", menu=file_menu)

# FRAME CENTER
frame_center = tk.Frame(master=root, width=600, height=800)
frame_center.pack(side="left", expand=600, fill=tk.BOTH, padx=20)
# PLOT
fig, ax = plt.subplots(figsize=SEG_SIZE)

canvas = FigureCanvasTkAgg(fig, master=frame_center)
canvas.get_tk_widget().pack(expand=True)


# FRAME RIGHT
frame_right = tk.Frame(master=root, width=400, height=810, bg=BG_COLOR)
frame_right.pack(side="right", expand=400, fill=tk.BOTH)

# SLIDER
tk.Label(master=frame_right, text="Capa Z: ",
         bg=BG_COLOR).grid(pady=5, row=0, column=1)
slider = tk.Scale(master=frame_right, from_=1,
                  to=max_depth, resolution=1, orient=tk.HORIZONTAL, bg=BG_COLOR, command=slider_event)
slider.grid(pady=5, row=0, column=2)

# PREPROCESSING (Denoising)
preprocessing_var = tk.StringVar()
preprocessing_var.set("Main filter")
preprocessing_options = ["Main filter",
                         "Median filter", "Median Filter Borders"]

tk.Label(master=frame_right, text="Denoising: ",
         bg=BG_COLOR).grid(pady=5, row=1, column=1)
preprocessing_menu = tk.OptionMenu(
    frame_right, preprocessing_var, *preprocessing_options, command=select_denoise)
preprocessing_menu.grid(pady=5, row=1, column=2)


# PROCESSING (Segmentation)
algorithm_var = tk.StringVar()
algorithm_var.set("K-means")  # Valor inicial
algorithm_options = ["Thresholding", "K-means",
                     "Region Growing", "Gaussian Mixture Model"]

tk.Label(master=frame_right, text="Segmentación: ",
         bg=BG_COLOR).grid(pady=5, row=2, column=1)
algorithm_menu = tk.OptionMenu(
    frame_right, algorithm_var, *algorithm_options, command=select_algorithm)
algorithm_menu.grid(pady=5, row=2, column=2)

# HISTOGRAM
tk.Label(master=frame_right, text="Histograma: ",
         bg=BG_COLOR).grid(pady=5, row=3, column=2, columnspan=4)
fig2, ax2 = plt.subplots(figsize=HIST_SIZE)
ax2.set_xlabel("Intensidad")
ax2.set_ylabel("Frecuencia")
# Ajustar los márgenes del histograma
fig2.subplots_adjust(left=0.25, bottom=0.25, right=0.75, top=0.75)
hist = FigureCanvasTkAgg(fig2, master=frame_right)
hist.get_tk_widget().grid(row=4, column=2, columnspan=4)

# Crear la carpeta "data" si no existe
if not os.path.exists("data"):
    os.makedirs("data")

root.mainloop()
