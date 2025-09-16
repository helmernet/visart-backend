import sys

def show_invisible(file_path):
    with open(file_path, "rb") as f:
        lines = f.readlines()
    for i, line in enumerate(lines, 1):
        decoded = line.decode("utf-8", errors="replace")
        visible = (
            decoded
            .replace(" ", "·")        # espacio simple
            .replace("\t", "<TAB>")   # tabulador
            .replace("\r", "<CR>")    # retorno de carro
            .replace("\n", "<LF>")    # salto de línea
        )
        print(f"Línea {i:3}: {visible} ({len(decoded)} caracteres)")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python tools/show_invisible.py <archivo>")
        sys.exit(1)
    show_invisible(sys.argv[1])