import winreg
import sys
import os

def main():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"SOFTWARE\POV-Ray\v3.7\Windows")
        doc_path, _ = winreg.QueryValueEx(key, "DocPath")
    except FileNotFoundError:
        print("Could not find the POV-Rays document path")
        doc_path = input("Where is the POV-Ray document directory located? ")

    install_path = os.getcwd()
    venv_path = os.path.join(install_path, "../venv")
    pip_path = os.path.join(venv_path, "Scripts/pip.exe")
    python_path = os.path.abspath(os.path.join(install_path, "../venv/Scripts/python.exe")).replace("/", "\\")
    py_render_path = os.path.abspath(os.path.join(install_path, "../render/render.py")).replace("/", "\\")
    bat_render_path = os.path.abspath(os.path.join(install_path, "../render/render.bat")).replace("/", "\\")
    pvtools_path = os.path.join(doc_path, "ini/pvtools.ini")

    os.system("py -m pip install --user virtualenv")
    os.system(f"py -m venv {venv_path}")
    os.system(f"{pip_path} install moviepy numpy opencv-python keyboard datetime")

    with open(bat_render_path, "w") as render:
        render.write("@ECHO OFF\n")
        render.write(f"{python_path} {py_render_path} %1")

    with open(pvtools_path, "r") as pvtools:
        pvtools_lines = pvtools.readlines()

    with open(os.path.join(doc_path, "ini/pvtools.backup.ini"), "w") as pvtools_backup:
        pvtools_backup.writelines(pvtools_lines)

    indexed_items = {}
    for x in range(int(1e6)):
        if len(indices := line_start_indexes(pvtools_lines, f"Item{x}")) > 0:
            indexed_items[x] = indices
        else:
            break

    zero_indices = indexed_items[0]
    
    for _, (index, lines) in enumerate(indexed_items.items()):
        for line in lines:
            pvtools_lines[line] = pvtools_lines[line].replace(f"Item{index}", f"Item{index + 1}")

    zero_lines = [
        "Render video",
        f"{bat_render_path} \"%d\"",
        "Render the last animation to a video file"
    ]
    for index, zero in enumerate(zero_indices):
        pvtools_lines.insert(zero + index, f"Item0={zero_lines[index]}\n")

    with open(pvtools_path, "w") as f:
        f.writelines(pvtools_lines)

    print("\nInstallation finished!\n")

def line_start_indexes(lines, keyword):
    indices = []
    for line in range(len(lines)):
        if lines[line].startswith(keyword):
            indices.append(line)
    return indices

if __name__ == '__main__':
    main()
