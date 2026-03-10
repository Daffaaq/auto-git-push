import subprocess
import os
from datetime import datetime
from shutil import which

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
    if not which("gh"):
        print("❌ GitHub CLI tidak ditemukan. Pastikan 'gh' ada di PATH")
        exit()

# ======================
# Git Init & Initial Commit
# ======================
def check_git():
    """Inisialisasi git kalau belum ada"""
    if not os.path.exists(".git"):
        print("📦 Git belum diinisialisasi, menjalankan git init...")
        run(["git", "init"])

def initial_commit_if_needed():
    """Buat initial commit kalau belum ada commit sama sekali"""
    try:
        log = run_output(["git", "log", "--oneline"])
    except:
        log = ""
    if not log:
        print("📝 Membuat initial commit...")
        if not os.listdir("."):
            repo_name = os.path.basename(os.getcwd())
            with open("README.md", "w") as f:
                f.write(f"# {repo_name}\nAuto-generated README\n")
        if not os.path.exists(".gitignore"):
            with open(".gitignore", "w") as f:
                f.write("vendor/\n.env\n*.log\n")
        run(["git", "add", "."])
        msg = input("Masukkan pesan untuk initial commit (kosong = auto): ").strip()
        if not msg:
            msg = "Initial commit " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        run(["git", "commit", "-m", msg])
        print("✅ Initial commit berhasil dibuat")
        with open("git_auto.log", "a") as log_file:
            log_file.write(f"{datetime.now()} | Initial commit: {msg}\n")

# ======================
# GitHub Repo
# ======================
def check_remote():
    """Cek remote origin, buat repo GitHub kalau belum ada"""
    remotes = run_output(["git", "remote"])
    default_repo_name = os.path.basename(os.getcwd())

    if "origin" not in remotes:
        repo_name = input(f"Masukkan nama repository GitHub (default: {default_repo_name}): ").strip()
        if not repo_name:
            repo_name = default_repo_name

        visibility = input("Visibility repo? [public/private] (default: public): ").strip().lower()
        if visibility not in ["public", "private"]:
            visibility = "public"

        branch = input("Nama branch default (kosong = main): ").strip()
        if not branch:
            branch = "main"

        print(f"🚀 Membuat repository GitHub: {repo_name}")
        initial_commit_if_needed()
        run(["gh", "repo", "create", repo_name,
             f"--{visibility}", "--source=.", "--remote=origin", "--push", "--confirm"])
        run(["git", "branch", "-M", branch])
        print(f"✅ Repository GitHub '{repo_name}' berhasil dibuat dan branch '{branch}' siap push")
        return branch
    else:
        branch = run_output(["git", "branch", "--show-current"])
        if not branch:
            branch = "main"
        return branch

# ======================
# Git Tools Menu
# ======================
def git_tools_menu():
    while True:
        print("\n=== Git Tools Menu ===")
        print("1. Lihat semua branch")
        print("2. Buat branch baru")
        print("3. Checkout ke branch")
        print("4. Lihat log commit")
        print("5. Kembali ke menu utama")
        choice = input("Pilih opsi: ").strip()

        if choice == "1":
            branches = run_output(["git", "branch", "-a"])
            print("\n📂 Semua branch:\n", branches)
        elif choice == "2":
            new_branch = input("Nama branch baru: ").strip()
            if not new_branch:
                print("⏩ Membuat branch dibatalkan")
            else:
                run(["git", "checkout", "-b", new_branch])
                print(f"✅ Branch '{new_branch}' dibuat dan dicheckout")
        elif choice == "3":
            checkout_branch = input("Nama branch untuk checkout: ").strip()
            if not checkout_branch:
                print("⏩ Checkout branch dibatalkan")
            else:
                run(["git", "checkout", checkout_branch])
                print(f"✅ Berhasil checkout ke branch '{checkout_branch}'")
        elif choice == "4":
            logs = run_output(["git", "log", "--oneline", "--graph", "--pretty=format:%h %ad %s", "--all"])
            print("\n📝 Log commit:\n", logs)
        elif choice == "5":
            break
        else:
            print("⚠️ Pilihan tidak valid")

# ======================
# Commit & Push
# ======================
def commit_push_loop(branch):
    while True:
        status = run_output(["git", "status", "--porcelain"])
        if not status:
            print("⚠️ Tidak ada perubahan untuk di-commit.")
        else:
            print("\n📄 Perubahan terdeteksi:\n", status)
            msg = input("\nMasukkan pesan commit (kosong = auto, 'skip' = lewati commit): ").strip()
            if msg.lower() == "skip":
                print("⏩ Commit dilewati")
            else:
                if not msg:
                    msg = "auto commit " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                run(["git", "add", "."])
                run(["git", "commit", "-m", msg])
                do_push = input("Push sekarang ke GitHub? (y/n, default y): ").strip().lower()
                if do_push != "n":
                    print(f"\n🚀 Push ke branch {branch}")
                    run(["git", "push", "-u", "origin", branch])
                    print("🎉 Push berhasil")
                with open("git_auto.log", "a") as log_file:
                    log_file.write(f"{datetime.now()} | Commit: {msg} | Branch: {branch}\n")
        # Menu tambahan
        print("\n💡 Opsi tambahan:")
        print("   [tools] buka menu Git tools, [exit] keluar")
        action = input("Pilihan: ").strip().lower()
        if action == "tools":
            git_tools_menu()
        elif action == "exit":
            print("👋 Keluar dari Auto Git Tool")
            break

# ======================
# Main
# ======================
def main():
    print("\n==== AUTO GIT TOOL V10 ====\n")
    check_gh()
    check_git()
    branch = check_remote()
    commit_push_loop(branch)

if __name__ == "__main__":
    main()