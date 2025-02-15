import zipfile
import os
import pandas as pd
import glob


def unzip_file(zip_path, destination):
    """Descomprime un archivo ZIP en la ruta especificada."""
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(destination)


def ensure_directory_exists(directory_path):
    """Crea un directorio si no existe."""
    os.makedirs(directory_path, exist_ok=True)


def build_dataset(source_folder, output_csv):
    """Crea un dataset consolidado a partir de archivos de texto organizados en subdirectorios según su categoría."""
    dataset = []
    sentiment_classes = ['negative', 'neutral', 'positive']  # Categorías predefinidas

    for sentiment in sentiment_classes:
        text_files = glob.glob(os.path.join(source_folder, sentiment, '*'))
        for file_path in text_files:
            with open(file_path, 'r', encoding='utf-8') as file:
                text_content = file.read().strip()
                dataset.append([text_content, sentiment])

    # Convertir la lista en un DataFrame y exportarlo a CSV
    df = pd.DataFrame(dataset, columns=['phrase', 'target'])  # Cambio de 'sentiment' a 'target'
    df.to_csv(output_csv, index=False)

    return df

"""
    La información requerida para este laboratio esta almacenada en el
    archivo "files/input.zip" ubicado en la carpeta raíz.
    Descomprima este archivo.

    Como resultado se creara la carpeta "input" en la raiz del
    repositorio, la cual contiene la siguiente estructura de archivos:


    ```
    train/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    test/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    ```

    A partir de esta informacion escriba el código que permita generar
    dos archivos llamados "train_dataset.csv" y "test_dataset.csv". Estos
    archivos deben estar ubicados en la carpeta "output" ubicada en la raiz
    del repositorio.

    Estos archivos deben tener la siguiente estructura:

    * phrase: Texto de la frase. hay una frase por cada archivo de texto.
    * sentiment: Sentimiento de la frase. Puede ser "positive", "negative"
      o "neutral". Este corresponde al nombre del directorio donde se
      encuentra ubicado el archivo.

    Cada archivo tendria una estructura similar a la siguiente:

    ```
    |    | phrase                                                                                                                                                                 | target   |
    |---:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------|
    |  0 | Cardona slowed her vehicle , turned around and returned to the intersection , where she called 911                                                                     | neutral  |
    |  1 | Market data and analytics are derived from primary and secondary research                                                                                              | neutral  |
    |  2 | Exel is headquartered in Mantyharju in Finland                                                                                                                         | neutral  |
    |  3 | Both operating profit and net sales for the three-month period increased , respectively from EUR16 .0 m and EUR139m , as compared to the corresponding quarter in 2006 | positive |
    |  4 | Tampere Science Parks is a Finnish company that owns , leases and builds office properties and it specialises in facilities for technology-oriented businesses         | neutral  |
    ```


"""

def pregunta_01():
    """
    Realiza la extracción, procesamiento y generación de los archivos de dataset.
    """

    # Ruta del archivo ZIP de entrada
    zip_file_path = 'files/input.zip'
    extraction_path = 'files'

    # Extraer el contenido del ZIP
    unzip_file(zip_file_path, extraction_path)

    # Crear la carpeta de salida si no existe
    output_folder = 'files/output'
    ensure_directory_exists(output_folder)

    # Procesar y generar los datasets
    train_dataset = build_dataset(os.path.join(extraction_path, 'input/train'),
                                  os.path.join(output_folder, 'train_dataset.csv'))
    test_dataset = build_dataset(os.path.join(extraction_path, 'input/test'),
                                 os.path.join(output_folder, 'test_dataset.csv'))

    return train_dataset, test_dataset
