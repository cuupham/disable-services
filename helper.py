from pathlib import Path
import subprocess


def is_path_exists(path: str) -> bool:
    return Path(path).exists()

def get_services_from_file(file_path: str) -> list[str]:
    with open(file_path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def is_service_available(service_name: str) -> bool:
    try:
        result = subprocess.run(['sc', 'query', service_name], capture_output=True, text=True)
        return result.returncode == 0 and 'STATE' in result.stdout
    except Exception:
        return False

def disable_service(service_name: str) -> tuple[bool, str]:
    try:
        result = subprocess.run(
            ['sc', 'config', service_name, 'start=', 'disabled'],
            capture_output=True,
            text=True
        )

        message = (result.stdout + result.stderr).strip()
        message = ' '.join(message.split())

        if result.returncode != 0 or "FAILED" in result.stdout.upper():
            return False, message or f"Return code: {result.returncode}"

        return True, message or "Success"

    except Exception as e:
        return False, ' '.join(str(e).split())

def disable_all(services: list[str]) -> list[tuple[str, bool, str]]:
    results = []
    for service in services:
        if is_service_available(service):
            status, message = disable_service(service)
            results.append((service, status, message))
        else:
            results.append((service, False, "Service not found"))
    return results