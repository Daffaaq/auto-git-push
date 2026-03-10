import subprocess
import os
from datetime import datetime

# ======================
# Helper functions
# ======================
def run(cmd):
    """Jalankan command shell, error kalau gagal"""
    subprocess.run(cmd, check=True)

def run_output(cmd):
    """Jalankan command dan kembalikan stdout"""
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()

def check_gh():
    """Cek apakah GitHub CLI tersedia di PATH"""
    from shutil import which
    if not which("gh"):
        print("❌ GitHub CLI tidak ditemukan. Pastikan 'gh' ada di PATH")
        exit()

# ======================
# Git Init & Commit
# ======================
def check_git():
    """Inisialisasi git kalau belum ada"""
    if not os.path.exists(".git"):
        print("📦 Git belum diinisialisasi, menjalankan git init...")
        run(["git", "init"])

def initial_commit_if_needed():
    """Buat initial commit kalau belum ada commit sama sekali"""
    log = run_output(["git", "log", "--oneline"])
    if not log:
        print("📝 Membuat initial commit...")
        # Kalau folder kosong, buat README.md
        if not os.listdir("."):
            repo_name = os.path.basename(os.getcwd())
            with open("README.md", "w") as f:
                f.write(f"# {repo_name}\nAuto-generated README\n")
        # Add semua file
        run(["git", "add", "."])
        # Commit pertama
        run(["git", "commit", "-m", "Initial commit"])
        print("✅ Initial commit berhasil dibuat")

# ======================
# GitHub Repo
# ======================
def check_remote():
    """Cek remote origin, buat repo GitHub kalau belum ada"""
    remotes = run_output(["git", "remote"])
    default_repo_name = os.path.basename(os.getcwd())

    if "origin" not in remotes:
        # Input nama repo
        repo_name = input(f"Masukkan nama repository GitHub (default: {default_repo_name}): ")
        if not repo_name.strip():
            repo_name = default_repo_name

        print(f"🚀 Membuat repository GitHub: {repo_name}")
        # Pastikan ada commit pertama
        initial_commit_if_needed()
        # Create repo dan push
        run(["gh", "repo", "create", repo_name,
             "--public", "--source=.", "--remote=origin", "--push"])
        print("✅ Repository GitHub berhasil dibuat dan di-push")

# ======================
# Commit & Push
# ======================
def commit_push():
    """Commit perubahan lokal dan push ke GitHub"""
    status = run_output(["git", "status", "--porcelain"])
    if not status:
        print("⚠️ Tidak ada perubahan")
        return

    print("\n📄 Perubahan:\n")
    print(status)

    msg = input("\nMasukkan pesan commit (kosong = auto): ")
    if msg == "":
        msg = "auto commit " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    run(["git", "add", "."])
    run(["git", "commit", "-m", msg])

    branch = run_output(["git", "branch", "--show-current"])
    if branch == "":
        branch = "main"
        run(["git", "branch", "-M", branch])

    print(f"\n🚀 Push ke branch {branch}")
    run(["git", "push", "-u", "origin", branch])
    print("🎉 Push berhasil")

# ======================
# Main
# ======================
def main():
    print("\n==== AUTO GIT TOOL V5 INPUT READY ====\n")
    check_gh()
    check_git()
    check_remote()
    commit_push()

if __name__ == "__main__":
    main()