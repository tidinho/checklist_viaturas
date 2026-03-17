from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def extrair_metadados(caminho_imagem):
    imagem = Image.open(caminho_imagem)
    exif_data = imagem._getexif()
    dados = {}

    if exif_data:
        for tag, valor in exif_data.items():
            nome_tag = TAGS.get(tag, tag)
            dados[nome_tag] = valor

    # GPS
    gps_info = {}
    if "GPSInfo" in dados:
        for key in dados["GPSInfo"].keys():
            gps_info[GPSTAGS.get(key, key)] = dados["GPSInfo"][key]

        # Converter para decimal
        def _convert_to_degrees(value):
            d, m, s = value
            return d + m/60 + s/3600

        if 'GPSLatitude' in gps_info and 'GPSLatitudeRef' in gps_info:
            lat = _convert_to_degrees(gps_info['GPSLatitude'])
            if gps_info['GPSLatitudeRef'] != 'N':
                lat = -lat
            gps_info['Latitude'] = lat

        if 'GPSLongitude' in gps_info and 'GPSLongitudeRef' in gps_info:
            lon = _convert_to_degrees(gps_info['GPSLongitude'])
            if gps_info['GPSLongitudeRef'] != 'E':
                lon = -lon
            gps_info['Longitude'] = lon

    return {
        "dispositivo": dados.get("Model"),
        "data": dados.get("DateTime"),
        "gps": gps_info
    }