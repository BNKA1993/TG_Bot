picture_directory = 'pictures'
picture_files = os.listdir(picture_directory)
picture_paths = [os.path.join(picture_directory, filename) for filename in picture_files]
# список картинок для пользователя, которые отправляются рандомно
