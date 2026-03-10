import subprocess
import sys

def run_git_command(command):
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout.strip()

try:
    # Cek branch aktif
    branch = run_git_command(["git", "branch", "--show-current"])
    print(f"📂 Branch aktif: {branch}")

    # Cek apakah ada perubahan
    status = run_git_command(["git", "status", "--porcelain"])

    if not status:
        print("⚠️ Tidak ada perubahan untuk di-commit.")
        sys.exit()

    print("📝 Perubahan terdeteksi:")
    print(status)

    # Input pesan commit
    commit_message = input("\nMasukkan pesan commit: ")

    # Git add
    subprocess.run(["git", "add", "."], check=True)
    print("✅ File berhasil di-add")

    # Commit
    subprocess.run(["git", "commit", "-m", commit_message], check=True)
    print(f"✅ Commit berhasil: {commit_message}")

    # Konfirmasi push
    confirm = input("🚀 Push ke GitHub sekarang? (y/n): ")

    if confirm.lower() == "y":
        subprocess.run(["git", "push", "origin", branch], check=True)
        print("🎉 Push berhasil ke GitHub!")
    else:
        print("❌ Push dibatalkan")

except Exception as e:
    print("🔥 Terjadi error:", e)