def get_filename(filepath):

    path_components = filepath.split('/')
    print(path_components)
    filename_with_ext = path_components[len(path_components)-1]
    print(path_components[len(path_components)-1])
    filename_without_ext = filename_with_ext[:-4]
    return filename_without_ext


name = get_filename('/home/sangoshthi/tushar/Django/Sangoshti/uploads/audio_files/Q&A/Content_intro.wav')
print(name)
