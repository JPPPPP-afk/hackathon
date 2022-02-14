import filetype
import os

# Write text to the end of a file
# If append is true, add to file end
# If append is false, cover original content
# If file does not exist / not txt file, raise IOError
def write_txt_file(*, output_file_name, text, append):
    if exists_file(output_file_name) and check_file_type(output_file_name, 'txt'):
        if append:
            with open (output_file_name, 'a') as f:
                f.write(text)
                f.close()
        else:
            with open (output_file_name, 'w') as f:
                f.write(text)
                f.close()
    else:
        raise IOError('write_txt_file: error file input: {}'.format(output_file_name))

# Check file type according to the first 16 bit of the file
def check_file_type(filename, target_type):
    kind = filetype.guess(filename)

    # txt file cannot be identified
    if kind is None:
        if target_type == 'txt':
            try:
                with open(filename) as f:
                    f.close()
                    return True
            except Exception:
                return False

        return False
    
    return kind.extension == target_type


# Try to read a txt file and return its content in a list of string
# If file does not exist / not txt file, raise IOError
def read_txt_file(filename):
    if exists_file(filename) and check_file_type(filename, 'txt'):
        f = open(filename)
        file_content = []

        for line in f:
            file_content.append(line)

        return file_content
    else:
        raise IOError("read_txt_file: error file input: {}".format(filename)) # .format(e) ?


# Check if a file exists
def exists_file(file):
    return os.path.exists(file) and os.path.isfile(file)

# Check if a directory exists
def exists_dir(dir):
    return os.path.exists(dir) and os.path.isdir(dir)