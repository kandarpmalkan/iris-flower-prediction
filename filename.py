
import os
from pathlib import Path


def generate_folder_structure(folder_path):
    root = Path(folder_path).expanduser().resolve()

    # Validate the input folder
    if not root.exists():
        print("Error: The folder does not exist.")
        return

    if not root.is_dir():
        print("Error: The given path is not a folder.")
        return

    # Save the output outside the scanned folder
    output_file = root.parent / f"{root.name}_structure.txt"

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(f"FOLDER STRUCTURE: {root.name}\n")
        file.write(f"Root path: {root}\n")
        file.write("=" * 80 + "\n\n")

        def walk_directory(current_path, prefix=""):
            try:
                items = sorted(
                    current_path.iterdir(),
                    key=lambda item: (
                        not item.is_dir(),
                        item.name.lower()
                    )
                )
            except PermissionError:
                file.write(prefix + "└── [Permission denied]\n")
                return

            for index, item in enumerate(items):
                is_last = index == len(items) - 1

                connector = "└── " if is_last else "├── "
                file.write(prefix + connector + item.name)

                if item.is_dir():
                    file.write("/\n")
                    extension = "    " if is_last else "│   "
                    walk_directory(item, prefix + extension)
                else:
                    file.write("\n")

        file.write(root.name + "/\n")
        walk_directory(root)

    print(f"Folder structure saved successfully!\n")
    print(f"Output file: {output_file}")


if __name__ == "__main__":
    folder = input("Enter the folder path: ").strip().strip('"')
    generate_folder_structure(folder)
