import os

folder_path = 'C:/Users/L4069846/OneDrive - Saint-Gobain/Documents - Inteligência de Vendas/Outros Projetos/Card_Game_Convencao_2023/Jogo/assets/char_selection/'

for filename in os.listdir(folder_path):
    #if filename == 'Character1M_1_silver_medal_get_2.png':
    if filename.endswith('.png'):
        base_name, extension = os.path.splitext(filename)
        parts = base_name.split('_')
        if len(parts) > 1 and parts[-1].isdigit():
            parts[-1] = parts[-1].zfill(2)
            new_name = '_'.join(parts) + extension
            old_path = os.path.join(folder_path, filename)
            new_path = os.path.join(folder_path, new_name)
            os.rename(old_path, new_path)
