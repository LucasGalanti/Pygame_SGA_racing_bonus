from PIL import Image
import os


RGB_color_change_dict = {
    "light_shirt": [(234, 50, 60), (0,122,197)],
    "dark_shirt": [(196, 36, 48), (0,88,143)],
    "light_pants": [(0, 152, 220), (95, 92, 91)],
    "dark_pants": [(0, 105, 170), (56, 51 , 49)],
    "darker_shirt": [(137,30,43), (0, 35, 57)]
}


# Define the folder path where the images are located
folder_path = 'C:/Users/L4069846/OneDrive - Saint-Gobain/Documents - Inteligência de Vendas/Outros Projetos/Card_Game_Convencao_2023/Jogo/assets/char_selection/'

# Iterate through all the PNG images in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".png"):
        # Open the image
        image_path = os.path.join(folder_path, filename)
        image = Image.open(image_path).convert("RGBA")

        # Get the pixel data
        pixels = image.load()

        # Iterate through each pixel in the image
        for x in range(image.width):
            for y in range(image.height):
                # Check if the pixel color matches any of the RGB values in the dictionary
                for key, values in RGB_color_change_dict.items():
                    # Only change the color of non-transparent pixels
                    if pixels[x, y][:3] == values[0] and pixels[x, y][3] > 0:
                        # Change the pixel color to the second RGB value in the dictionary
                        # Preserve the alpha channel
                        pixels[x, y] = values[1] + (pixels[x, y][3],)

        # Save the modified image
        image.save(image_path)


