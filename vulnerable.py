def upload_file(file, upload_dir):
  filename = file.filename

  file_path = os.path.join(upload_dir, filename)

  file.save(file_path)
