import os
import subprocess
import argparse
import json


def run_command(command):
    """Run a system command and handle errors if any."""
    try:
        result = subprocess.run(command, shell=True, check=True)
        if result.returncode != 0:
            print(f"Command failed: {command}")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        exit(1)


def update_and_upgrade(skip_upgrade=False):
    """Update and optionally upgrade the system's package list."""
    print("Updating apt package list...")
    run_command("sudo apt-get update")
    if not skip_upgrade:
        print("Upgrading apt packages...")
        run_command("sudo apt-get upgrade -y")
    else:
        print("Skipping apt upgrade...")


def install_apt_components(components):
    """Install components using apt-get."""
    print("Installing apt components...")
    component_list = " ".join(components)
    run_command(f"sudo apt-get install -y {component_list}")


def install_pip_components(components):
    """Install components using pip."""
    print("Installing pip components...")
    component_list = " ".join(components)
    run_command(f"pip3 install {component_list}")


def update_submodules():
    """Update git submodules."""
    print("Updating git submodules...")
    run_command("git submodule update --init --recursive")


def read_json_file(json_path):
    """Read the build requirements from a JSON file."""
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Error: The file {json_path} does not exist.")
    else:
        with open(json_path, "r") as f:
            return json.load(f)


def read_requirements_txt(txt_path):
    """Read the pip requirements from a requirements.txt file."""
    if not os.path.exists(txt_path):
        raise FileNotFoundError(f"Error: The file {txt_path} does not exist.")
    else:
        with open(txt_path, "r") as f:
            return [line.strip() for line in f if line.strip()]


if __name__ == "__main__":
    # Argument parser to handle skip_upgrade option
    parser = argparse.ArgumentParser(description="Install necessary development tools.")
    parser.add_argument(
        "--skip-upgrade",
        action="store_true",
        help="Skip the apt upgrade step",
    )
    parser.add_argument(
        "--json",
        default="scripts/build_requirements.json",
        help="Path to the JSON file with apt build requirements",
    )
    parser.add_argument(
        "--requirements",
        default="scripts/python_requirements.txt",
        help="Path to the pip requirements.txt file",
    )
    args = parser.parse_args()

    # Read from JSON and requirements.txt
    try:
        build_requirements = read_json_file(args.json)
        apt_components = build_requirements.get("apt", [])
    except FileNotFoundError as e:
        print(e)
        exit(1)

    try:
        pip_components = read_requirements_txt(args.requirements)
    except FileNotFoundError as e:
        print(e)
        exit(1)

    # Execute functions
    update_and_upgrade(skip_upgrade=args.skip_upgrade)
    install_apt_components(apt_components)
    install_pip_components(pip_components)
    update_submodules()
