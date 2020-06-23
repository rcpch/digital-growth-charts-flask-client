from pathlib import Path
from os import path, remove
from flask import request

def chunk_file(file, file_path):
    ## thanks to Chris Griffith, Code Calamity for this code - upload files, chunk if large
    
    current_chunk = int(request.form['dzchunkindex'])

    # If the file already exists it's ok if we are appending to it,
    # but not if it's new file that would overwrite the existing one
    if path.exists(file_path) and current_chunk == 0:
        # 400 and 500s will tell dropzone that an error occurred and show an error
        return {
            "response":'File already exists', 
            "response_code": 400
        }

    try:
        with open(file_path, 'ab') as f:
            f.seek(int(request.form['dzchunkbyteoffset']))
            f.write(file.stream.read())

    except OSError:
        # log.exception will include the traceback so we can see what's wrong 
        print('Could not write to file')
        return {
            "response": "Not sure why, but we couldn't write the file to disk",
            "response_code": 500
        }

    total_chunks = int(request.form['dztotalchunkcount'])

    if current_chunk + 1 == total_chunks:
        # This was the last chunk, the file should be complete and the size we expect
        if path.getsize(file_path) != int(request.form['dztotalfilesize']):
            assert(f"File {file.filename} was completed, "
                    f"but has a size mismatch."
                    f"Was {os.path.getsize(save_path)} but we"
                    f" expected {request.form['dztotalfilesize']} ")
            return {
                "response": "Size mismatch", 
                "response_code": 500
            }
        else:
            print(f'File {file.filename} has been uploaded successfully')
            return {
                "response": 'success',
                "response_code": 200
                }
    else:
        print(f'Chunk {current_chunk + 1} of {total_chunks} '
                f'for file {file.filename} complete')

        return {
                "response": "Chunk upload successful", 
                "response_code": 200
        }