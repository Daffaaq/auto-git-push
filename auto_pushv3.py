import subprocess
import sys
from datetime import datetime

# warna terminal
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
CYAN = "\033[96m"
RESET = "\033[0m"


def run_git(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()


def run(cmd):
    subprocess.run(cmd, check=True)


try:

    print(CYAN + "\n=== AUTO GIT PUSH V3 ===\n" + RESET)

    # cek branch
    branch = run_git(["git", "branch", "--show-current"])

    if not branch:
        print(RED + "❌ Bukan repository git!" + RESET)
        sys.exit()

    print(GREEN + f"📂 Branch aktif: {branch}" + RESET)

    # cek perubahan
    status = run_git(["git", "status", "--porcelain"])

    if not status:
        print(YELLOW + "⚠️ Tidak ada perubahan." + RESET)
        sys.exit()

    print(CYAN + "\n📄 File yang berubah:\n" + RESET)
    print(status)

    # input commit
    msg = input("\nMasukkan pesan commit (kosong = auto): ")

    if msg.strip() == "":
        msg = "auto commit " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # git add
    print(CYAN + "\n📦 Menambahkan file..." + RESET)
    run(["git", "add", "."])

    # commit
    print(CYAN + "📝 Commit..." + RESET)
    run(["git", "commit", "-m", msg])

    print(GREEN + f"✅ Commit berhasil: {msg}" + RESET)

    # cek remote
    remotes = run_git(["git", "remote"]).splitlines()

    if not remotes:
        print(RED + "❌ Tidak ada remote repository." + RESET)
        sys.exit()

    print(CYAN + "\n🌍 Remote terdeteksi:" + RESET, ", ".join(remotes))

    confirm = input("\n🚀 Push sekarang? (y/n): ")

    if confirm.lower() != "y":
        print(YELLOW + "Push dibatalkan." + RESET)
        sys.exit()

    # push ke semua remote
    for remote in remotes:
        print(CYAN + f"\n🚀 Push ke {remote}..." + RESET)
        run(["git", "push", remote, branch])

    print(GREEN + "\n🎉 Semua push berhasil!\n" + RESET)

except subprocess.CalledProcessError as e:
    print(RED + "\n❌ Error saat menjalankan git command" + RESET)
    print(e)

except Exception as e:
    print(RED + "\n🔥 Error:" + RESET, e)