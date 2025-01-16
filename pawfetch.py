#!/usr/bin/env python3
import os
import platform
import psutil
import subprocess
import configparser
from datetime import timedelta

CONFIG_PATH = os.path.expanduser("~/.config/pawfetch/config.paw")

def load_config():
    config = configparser.ConfigParser()
    config['settings'] = {
        'title_color': '#f5c2e7',
        'info_color': '#f5c2e7',
        'info_sub_color': '#cdd6f4',
        'ascii_color1': '#74c7ec',
        'ascii_color2': '#f5c2e7',
        'ascii_color3': '#cdd6f4',
        'hostname_format': '{user}@{hostname}'
    }
    if not os.path.exists(CONFIG_PATH):
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        with open(CONFIG_PATH, 'w') as config_file:
            config.write(config_file)
    else:
        config.read(CONFIG_PATH)
    return config

def get_cpu_info():
    cpu_info = subprocess.check_output("lscpu | grep 'Model name:'", shell=True).decode().strip()
    cpu_name = cpu_info.split(":")[1].strip().lower().split(" @")[0].replace(" cpu", "")
    if "amd" in cpu_name:
        return cpu_name.replace("amd", "").strip()
    else:
        return cpu_name.replace("intel(r) core(tm)", "").replace("cpu @", "").strip()

def get_ram_info():
    mem = psutil.virtual_memory()
    total_memory = mem.total / (1024 ** 3)
    used_memory = (mem.total - mem.available) / (1024 ** 3)
    return f"{used_memory:.0f} gb / {total_memory:.0f} gb"

def get_gpu_info():
    try:
        gpu_info = subprocess.check_output("lspci | grep -i 'vga\\|3d\\|display'", shell=True).decode().lower()
        if "nvidia" in gpu_info:
            return gpu_info.split("[")[1].split("]")[0].strip()
        elif "amd" in gpu_info:
            return gpu_info.split(":")[-1].strip().replace("amd", "")
        else:
            return gpu_info.split(":")[-1].strip()
    except subprocess.CalledProcessError:
        return "gpu isn't supported :3"

def get_distro():
    try:
        distro_info = subprocess.check_output("cat /etc/os-release | grep -E '^PRETTY_NAME='", shell=True).decode()
        return distro_info.split("=")[1].strip().strip('"').lower().replace(" linux", "")
    except subprocess.CalledProcessError:
        return "unsupported distro :3"

def get_kernel():
    return platform.release().lower()

def get_packages():
    try:
        pacman_count = int(subprocess.check_output("pacman -Qq | wc -l", shell=True).decode().strip())
    except subprocess.CalledProcessError:
        pacman_count = 0

    try:
        flatpak_count = int(subprocess.check_output("flatpak list --columns=application | wc -l", shell=True).decode().strip())
    except subprocess.CalledProcessError:
        flatpak_count = 0

    total_count = pacman_count + flatpak_count
    return f"{total_count}"

def get_uptime():
    uptime_seconds = psutil.boot_time()
    uptime_duration = timedelta(seconds=int(psutil.time.time() - uptime_seconds))
    days = uptime_duration.days
    hours, remainder = divmod(uptime_duration.seconds, 3600)
    minutes = remainder // 60

    if days > 0:
        return f"{days}d {hours}h {minutes}m"
    elif hours > 0:
        return f"{hours}h {minutes}m"
    else:
        return f"{minutes}m"

def colorize(text, color):
    return f"\033[38;2;{int(color[1:3], 16)};{int(color[3:5], 16)};{int(color[5:7], 16)}m{text}\033[0m"

def pawfetch():
    config = load_config()
    settings = config['settings']
    
    ascii_art = r"""⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣄⢀⡀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢿⣿⣿⡿⠀⠀⠀⠀
⠀⠀⠀⠀⣀⣀⣤⠖⠛⠉⠉⠉⠉⠉⠙⠒⠦⣿⣏⣀⠀⠀⠀⠀
⠀⠀⣠⠞⠁⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢵⡄⠀⠀
⠀⢰⣯⠀⠀⢀⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⠀⠀⣿⠀⠀
⠀⠈⣇⢀⢠⠇⠀⣶⡶⠄⠀⠀⠀⢠⣶⡶⠀⠀⣸⣀⣼⠟⠀⠀
⠀⠀⠙⠛⠾⡆⠀⠙⠛⠃⠀⠀⠀⠀⠙⠋⠀⠀⣹⠟⠁⠀⠀⠀
⢀⡴⠚⠉⠛⢿⠀⠀⠀⠀⢿⣿⠆⠀⠀⠀⠀⢀⣿⠋⠉⠉⢳⡄
⢾⡀⡄⠀⣄⡼⠻⢧⠤⣤⠤⠤⣤⣠⣦⣾⠶⠞⢿⣤⡄⣠⣀⡷
⠈⠙⠛⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠀
    """
    colored_art = '\n'.join([
        colorize(line, settings['ascii_color1']) if idx % 3 == 0 else
        colorize(line, settings['ascii_color2']) if idx % 3 == 1 else
        colorize(line, settings['ascii_color3'])
        for idx, line in enumerate(ascii_art.splitlines())
    ])

    user = os.getlogin()
    hostname = platform.node()
    title = settings['hostname_format'].format(user=user, hostname=hostname).lower()
    cpu_info = get_cpu_info().replace("intel(r) core(tm)", "").replace("cpu @", "").strip()
    ram_info = get_ram_info()
    gpu_info = get_gpu_info().replace("nvidia", "").replace("geforce", "").strip()
    distro = get_distro()
    kernel = get_kernel()
    packages = get_packages()
    uptime = get_uptime()

    info = f"""    🐾 {colorize(title, settings['title_color'])} 🐾
    {colorize('os',  settings['info_color'])}      {colorize(distro, settings['info_sub_color'])}
    {colorize('krnl',  settings['info_color'])}    {colorize(kernel, settings['info_sub_color'])}
    {colorize('pkgs',  settings['info_color'])}    {colorize(packages, settings['info_sub_color'])}
    {colorize('cpu',  settings['info_color'])}     {colorize(cpu_info, settings['info_sub_color'])}
    {colorize('gpu',  settings['info_color'])}     {colorize(gpu_info, settings['info_sub_color'])}
    {colorize('mem',  settings['info_color'])}     {colorize(ram_info, settings['info_sub_color'])}
    {colorize('up',  settings['info_color'])}      {colorize(uptime, settings['info_sub_color'])}
    """

    lines_art = colored_art.splitlines()
    lines_info = info.splitlines()
    max_lines = max(len(lines_art), len(lines_info))
    padded_art = lines_art + [''] * (max_lines - len(lines_art))
    padded_info = lines_info + [''] * (max_lines - len(lines_info))

    for left, right in zip(padded_art, padded_info):
        print(f"{left:<45} {right}")

if __name__ == "__main__":
    pawfetch()
