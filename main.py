from helper import is_path_exists, get_services_from_file, disable_all
import os


def show_results(results: list[tuple[str, bool, str]]):
    widths = (45, 10, 50)  # service, status, message

    def format_row(service: str, status: str, message: str) -> str:
        return f"{service.ljust(widths[0])} {status.ljust(widths[1])} {message}"

    # Header
    print("Disabled Services Results".center(sum(widths), '-'))
    print(format_row("[SERVICE]", "[STATUS]", "[MESSAGE]"))
    print('-' * (sum(widths)))

    # Data
    for service, status, message in results:
        status_str = "Disabled" if status else "Failed"
        print(format_row(service, status_str, message))

def main():
    file_path = 'disable_safe.txt'

    if not is_path_exists(file_path):
        raise FileNotFoundError(f"File not found: \"{file_path}\"")

    services = get_services_from_file(file_path)
    if not services:
        raise ValueError("No services found in the file.")

    results = disable_all(services)

    show_results(results)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[EXCEPTION] {e}")
    finally:
        os.system('pause')
 