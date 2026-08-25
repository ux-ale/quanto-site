"""Resize the store screenshots for the web.

Reads the full-resolution folders ("iOS screenshots" / "Android screenshots",
numbered 1-14 in the same order as the locale chips) and writes display-sized
JPEGs to shots/<store>/<code>/NN.jpg. The originals are ~422 MB and stay out
of git; only the resized set is committed.
"""
import os, subprocess, sys

MAX_EDGE = 560
QUALITY  = 80

# folder number -> locale code, in chip order
CODES = ["EN", "DE", "FR", "ES-ES", "ES-419", "IT", "PT-BR",
         "TR", "ID", "MS", "JA", "KO", "NL", "PL"]

SOURCES = [("ios", "iOS screenshots"), ("play", "Android screenshots")]


def numbered_dirs(root):
    out = {}
    for name in os.listdir(root):
        full = os.path.join(root, name)
        if not os.path.isdir(full):
            continue
        num = name.split(" ", 1)[0]
        if num.isdigit():
            out[int(num)] = full
    return out


def main():
    total = skipped = 0
    for store, root in SOURCES:
        if not os.path.isdir(root):
            sys.exit(f"missing source folder: {root}")
        dirs = numbered_dirs(root)
        missing = [i for i in range(1, len(CODES) + 1) if i not in dirs]
        if missing:
            sys.exit(f"{root}: no folder numbered {missing}")

        for i, code in enumerate(CODES, start=1):
            src_dir = dirs[i]
            dst_dir = os.path.join("shots", store, code)
            os.makedirs(dst_dir, exist_ok=True)

            files = sorted(f for f in os.listdir(src_dir)
                           if f.lower().endswith((".jpg", ".jpeg", ".png")))
            for n, fname in enumerate(files, start=1):
                src = os.path.join(src_dir, fname)
                dst = os.path.join(dst_dir, f"{n:02d}.jpg")
                if os.path.exists(dst) and os.path.getmtime(dst) >= os.path.getmtime(src):
                    skipped += 1
                    continue
                subprocess.run(
                    ["sips", "-Z", str(MAX_EDGE), "-s", "format", "jpeg",
                     "-s", "formatOptions", str(QUALITY), src, "--out", dst],
                    check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                total += 1
            print(f"  {store}/{code}: {len(files)} images", flush=True)

    print(f"converted {total}, up to date {skipped}")


if __name__ == "__main__":
    main()
