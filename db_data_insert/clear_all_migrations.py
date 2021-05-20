import os


def clear_all_migrations(project_dir = "./"):
    exception_files = {"__init__.py"}
    for root, dirs, files in os.walk(project_dir):
        if "migrations" in root:
            files = list(set(files) - exception_files)
            for file in files:
                os.remove(os.path.join(root, file))


if __name__ == "__main__":
    clear_all_migrations("./HIS_void")
