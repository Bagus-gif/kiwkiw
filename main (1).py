import itertools
import os
import pyperclip
from colorama import Fore, Style, init

init(autoreset=True)  # auto-reset warna setiap print

def insert_dot_combinations(username):
    positions = list(range(1, len(username)))  # posisi yang bisa disisipi titik
    combinations = []
    for i in range(1, len(positions) + 1):
        for combo in itertools.combinations(positions, i):
            new_username = username
            offset = 0
            for pos in combo:
                new_username = new_username[:pos + offset] + '.' + new_username[pos + offset:]
                offset += 1
            combinations.append(new_username)
    return combinations

def load_used_emails(filepath):
    if not os.path.exists(filepath):
        return set()
    with open(filepath, 'r') as f:
        return set(line.strip() for line in f if line.strip())

def save_email_to_base(email, filepath):
    with open(filepath, 'a') as f:
        f.write(email + '\n')

def main():
    ref_code = input(f"{Fore.CYAN}Disimpan sesuai kode ref: {Style.RESET_ALL}").strip()
    base_email = input(f"{Fore.CYAN}Masukkan email dasar (contoh: umartest@gmail.com): {Style.RESET_ALL}").strip()
    pswd = input(f"{Fore.CYAN}Masukkan Password default: {Style.RESET_ALL}").strip()
    jumlah = int(input(f"{Fore.CYAN}Berapa akun yang ingin dibuat?: {Style.RESET_ALL}").strip())

    os.makedirs(ref_code, exist_ok=True)

    akun_path = os.path.join(ref_code, "akun.txt")
    token_path = os.path.join(ref_code, "tokens.txt")

    username, domain = base_email.split('@')
    kombinasi = insert_dot_combinations(username)
    kombinasi = sorted(set(kombinasi))  # hilangkan duplikat jika ada

    used_emails = load_used_emails('base.txt')

    akun_file = open(akun_path, "a")
    token_file = open(token_path, "a")
    password_default = pswd

    sukses = 0
    idx = 0

    while sukses < jumlah and idx < len(kombinasi):
        email_kandidat = f"{kombinasi[idx]}@{domain}"
        idx += 1
        if email_kandidat in used_emails:
            continue

        # Step 1: Copy email
        pyperclip.copy(email_kandidat)
        input(f"\n{Fore.YELLOW}[{sukses+1}] Email: {Fore.GREEN}{email_kandidat} {Fore.YELLOW}📋 (tersalin otomatis) — tekan Enter setelah tempel...")

        # Step 2: Copy password
        pyperclip.copy(password_default)
        input(f"{Fore.YELLOW}Password: {Fore.GREEN}{password_default} {Fore.YELLOW}📋 (tersalin otomatis) — tekan Enter setelah tempel...")

        # Step 3: Copy ref code
        pyperclip.copy(ref_code)
        input(f"{Fore.YELLOW}Ref Code: {Fore.GREEN}{ref_code} {Fore.YELLOW}📋 (tersalin otomatis) — tekan Enter setelah tempel...")

        # Step 4: Masukkan token dari hasil registrasi
        token = input(f"{Fore.CYAN}🔑 Masukkan token (hasil dari website): {Style.RESET_ALL}").strip()

        akun_file.write(f"{email_kandidat}:{password_default}\n")
        token_file.write(f"{token}\n")
        save_email_to_base(email_kandidat, 'base.txt')
        akun_file.flush()
        token_file.flush()

        sukses += 1

    #akun_file.flush()
    #token_file.flush()

    if sukses < jumlah:
        print(f"\n{Fore.RED}⚠️ Hanya berhasil membuat {sukses} akun. Kombinasi titik habis.")
    else:
        print(f"\n{Fore.GREEN}✅ Selesai! Semua email dan token disimpan.")

if __name__ == "__main__":
    main()
