import tkinter as tk
from tkinter import ttk, messagebox
import ast


def is_number(value: str) -> bool:
    try:
        float(value)
        return True
    except ValueError:
        # Intentar evaluar expresiones simples (fracciones a/b, operaciones + - * / **, paréntesis)
        try:
            _ = parse_numeric(value)
            return True
        except Exception:
            return False


def _eval_ast(node):
    if isinstance(node, ast.Expression):
        return _eval_ast(node.body)
    if isinstance(node, ast.Num):  # py<3.8
        return float(node.n)
    if isinstance(node, ast.Constant):  # py>=3.8
        if isinstance(node.value, (int, float)):
            return float(node.value)
        raise ValueError("Constante no numérica")
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        val = _eval_ast(node.operand)
        return +val if isinstance(node.op, ast.UAdd) else -val
    if isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow)):
        left = _eval_ast(node.left)
        right = _eval_ast(node.right)
        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        if isinstance(node.op, ast.Div):
            return left / right
        if isinstance(node.op, ast.Pow):
            return left ** right
    if isinstance(node, ast.Paren):
        return _eval_ast(node.value)
    raise ValueError("Expresión no permitida")


def parse_numeric(value: str) -> float:
    s = (value or "").strip()
    if s == "":
        raise ValueError("Entrada vacía")
    try:
        return float(s)
    except ValueError:
        # Permitir '^' como potencia -> '**'
        expr = s.replace('^', '**')
        tree = ast.parse(expr, mode='eval')
        val = _eval_ast(tree)
        return float(val)


class MatrixInput:
    def __init__(self, parent: tk.Widget, title: str):
        self.parent = parent
        self.frame = ttk.LabelFrame(parent, text=title)
        self.rows_var = tk.IntVar(value=2)
        self.cols_var = tk.IntVar(value=2)
        self.grid_frame = ttk.Frame(self.frame)
        self.entries: list[list[tk.Entry]] = []

        dims = ttk.Frame(self.frame)
        ttk.Label(dims, text="Filas:").grid(row=0, column=0, padx=(0, 4))
        self.rows_spin = ttk.Spinbox(dims, from_=1, to=10, textvariable=self.rows_var, width=5, command=self._rebuild)
        self.rows_spin.grid(row=0, column=1, padx=(0, 10))
        ttk.Label(dims, text="Columnas:").grid(row=0, column=2, padx=(0, 4))
        self.cols_spin = ttk.Spinbox(dims, from_=1, to=10, textvariable=self.cols_var, width=5, command=self._rebuild)
        self.cols_spin.grid(row=0, column=3)
        dims.grid(row=0, column=0, sticky="w", pady=(0, 6))

        self.grid_frame.grid(row=1, column=0, sticky="nsew")
        self.frame.columnconfigure(0, weight=1)
        self._rebuild()

    def widget(self) -> tk.Widget:
        return self.frame

    def _rebuild(self):
        for child in self.grid_frame.winfo_children():
            child.destroy()
        self.entries.clear()
        r = max(1, int(self.rows_var.get()))
        c = max(1, int(self.cols_var.get()))
        for i in range(r):
            row_entries = []
            for j in range(c):
                e = ttk.Entry(self.grid_frame, width=8, justify="center")
                e.grid(row=i, column=j, padx=2, pady=2)
                e.insert(0, "0")
                row_entries.append(e)
            self.entries.append(row_entries)

    def get_dimensions(self) -> tuple[int, int]:
        return len(self.entries), len(self.entries[0]) if self.entries else 0

    def get_values(self) -> list[list[float]]:
        matrix: list[list[float]] = []
        for i, row in enumerate(self.entries):
            values_row = []
            for j, e in enumerate(row):
                val = e.get().strip()
                try:
                    num = parse_numeric(val)
                except ValueError:
                    raise ValueError(f"Entrada no numérica en ({i+1},{j+1}): '{val}'")
                values_row.append(num)
            matrix.append(values_row)
        return matrix


class ResultView:
    def __init__(self, parent: tk.Widget):
        self.frame = ttk.LabelFrame(parent, text="Resultado")
        self.text = tk.Text(self.frame, height=10, width=60, state="disabled")
        self.text.grid(row=0, column=0, sticky="nsew")
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)

    def widget(self) -> tk.Widget:
        return self.frame

    def show_matrix(self, M: list[list[float]]):
        self._set_text(matrix_to_str(M))

    def show_error(self, msg: str):
        self._set_text(f"Error: {msg}")

    def clear(self):
        self._set_text("")

    def _set_text(self, content: str):
        self.text.configure(state="normal")
        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", content)
        self.text.configure(state="disabled")


def matrix_to_str(M: list[list[float]]) -> str:
    if not M:
        return "[]"
    cols = len(M[0])
    col_widths = [0] * cols
    as_str = [[f"{v:g}" for v in row] for row in M]
    for j in range(cols):
        col_widths[j] = max(len(row[j]) for row in as_str)
    lines = []
    for row in as_str:
        parts = [row[j].rjust(col_widths[j]) for j in range(cols)]
        lines.append("[ " + "  ".join(parts) + " ]")
    return "\n".join(lines)


def matmul(A: list[list[float]], B: list[list[float]]) -> list[list[float]]:
    a_rows = len(A)
    a_cols = len(A[0]) if A else 0
    b_rows = len(B)
    b_cols = len(B[0]) if B else 0
    if a_cols != b_rows:
        raise ValueError(f"Dimensiones incompatibles: {a_rows}x{a_cols} * {b_rows}x{b_cols}")
    C = [[0.0 for _ in range(b_cols)] for _ in range(a_rows)]
    for i in range(a_rows):
        for k in range(a_cols):
            aik = A[i][k]
            for j in range(b_cols):
                C[i][j] += aik * B[k][j]
    return C


def scalar_mul(s: float, M: list[list[float]]) -> list[list[float]]:
    return [[s * v for v in row] for row in M]


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Multiplicaciones de Matrices")
        self.geometry("900x600")
        self.minsize(780, 520)

        self._build_menu()

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        calc_tab = ttk.Frame(self.notebook)
        self.docs_tab = ttk.Frame(self.notebook)
        self.notebook.add(calc_tab, text="Calculadora")
        self.notebook.add(self.docs_tab, text="Documentación")

        container = ttk.Frame(calc_tab)
        container.pack(fill="both", expand=True, padx=10, pady=10)
        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)
        container.rowconfigure(2, weight=1)

        op_frame = ttk.Frame(container)
        ttk.Label(op_frame, text="Operación:").grid(row=0, column=0, padx=(0, 6))
        self.operation_var = tk.StringVar(value="A×B")
        self.operation_cb = ttk.Combobox(op_frame, textvariable=self.operation_var, state="readonly",
                                         values=("A×B", "Escalar×A", "A×Escalar"))
        self.operation_cb.grid(row=0, column=1)
        self.operation_cb.bind("<<ComboboxSelected>>", self._on_operation_change)
        op_frame.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))

        # Matrices
        self.matrixA = MatrixInput(container, "Matriz A")
        self.matrixB = MatrixInput(container, "Matriz B")
        self.matrixA.widget().grid(row=1, column=0, sticky="nsew", padx=(0, 5))
        self.matrixB.widget().grid(row=1, column=1, sticky="nsew", padx=(5, 0))

        scalar_frame = ttk.LabelFrame(container, text="Escalar")
        self.scalar_var = tk.StringVar(value="1")
        self.scalar_entry = ttk.Entry(scalar_frame, textvariable=self.scalar_var, width=12)
        ttk.Label(scalar_frame, text="Valor:").grid(row=0, column=0, padx=(0, 6))
        self.scalar_entry.grid(row=0, column=1)
        scalar_frame.grid(row=2, column=0, sticky="w", pady=(10, 10))
        self.scalar_container = scalar_frame

        actions = ttk.Frame(container)
        self.generate_btn = ttk.Button(actions, text="Calcular", command=self._calculate)
        self.generate_btn.grid(row=0, column=0, padx=(0, 10))
        self.clear_btn = ttk.Button(actions, text="Limpiar", command=self._clear)
        self.clear_btn.grid(row=0, column=1)
        actions.grid(row=2, column=1, sticky="e")

        self.result = ResultView(container)
        self.result.widget().grid(row=3, column=0, columnspan=2, sticky="nsew", pady=(10, 0))

        self.docs_text = tk.Text(self.docs_tab, wrap="word", state="normal")
        self.docs_text.insert("1.0",
            "MÉTODO DE OPERACIONES DE MATRICES\n"
            "=====================================================\n\n"
            "ENUNCIADO DEL PROCESO:\n"
            "----------------------\n"
            "Dada una matriz A de tamaño m×n y un escalar s, o bien dos matrices A (m×n) y B (n×p),\n"
            "se desea calcular el resultado de:\n\n"
            "  1) Escalar × Matriz:  C = s · A\n"
            "  2) Matriz × Matriz:   C = A × B\n\n"
            "FUNDAMENTO TEÓRICO (RESUMIDO):\n"
            "------------------------------\n"
            "1) Multiplicación por escalar:\n"
            "   Si s es un número real y A = [a_ij], entonces (s·A) = [s·a_ij].\n"
            "   Es decir, cada elemento de A se multiplica por s.\n\n"
            "2) Multiplicación de matrices (A×B):\n"
            "   Definida solo si columnas(A) = filas(B). Si A es m×n y B es n×p, entonces C es m×p y:\n"
            "   C[i,j] = Σ_{k=1..n} A[i,k] · B[k,j].\n\n"
            "USO EN ESTA APLICACIÓN:\n"
            "-----------------------\n"
            "1) Selecciona la operación: 'A×B', 'Escalar×A' o 'A×Escalar'.\n"
            "2) Ajusta dimensiones de A y B con 'Filas' y 'Columnas'.\n"
            "   - Para A×B: asegúrate de que columnas(A) = filas(B).\n"
            "3) Ingresa valores numéricos en las celdas (acepta enteros, decimales con punto y notación científica).\n"
            "4) Si la operación usa escalar, ingresa su valor en 'Valor'.\n"
            "5) Presiona 'Calcular' para ver el resultado en el panel inferior.\n\n"
            "VALIDACIONES Y CONSEJOS:\n"
            "------------------------\n"
            "- Las entradas deben ser números válidos (por ejemplo: 3, -2.5, 1e-3).\n"
            "- Para A×B: si las dimensiones no son compatibles, se mostrará un error.\n"
            "- Puedes usar matrices hasta 10×10 con los controles de dimensiones.\n"
            "- El resultado se muestra con formato compacto (por ejemplo, 2 en lugar de 2.0 cuando aplica).\n\n"
            "EJEMPLOS RÁPIDOS:\n"
            "-----------------\n"
            "- Escalar×A: si s = 2 y A = [[1, 3], [4, -1]], entonces 2·A = [[2, 6], [8, -2]].\n"
            "- A×B: si A(2×3) × B(3×2), C(2×2) con C[1,1] = A[1,1]·B[1,1] + A[1,2]·B[2,1] + A[1,3]·B[3,1].\n"
        )
        self.docs_text.configure(state="disabled")
        self.docs_text.pack(fill="both", expand=True, padx=10, pady=10)

        self._on_operation_change()

    def _build_menu(self):
        menubar = tk.Menu(self)
        ayuda = tk.Menu(menubar, tearoff=0)
        ayuda.add_command(label="Documentación", command=self._show_docs)
        ayuda.add_separator()
        ayuda.add_command(label="Acerca de", command=self._show_about)
        menubar.add_cascade(label="Ayuda", menu=ayuda)
        self.config(menu=menubar)

    def _show_docs(self):
        
        if hasattr(self, 'notebook') and hasattr(self, 'docs_tab'):
            self.notebook.select(self.docs_tab)
        else:
            messagebox.showinfo("Documentación", "Abra la pestaña 'Documentación' en la interfaz.")

    def _show_about(self):
        messagebox.showinfo("Acerca de", "Multiplicaciones de Matrices - Tkinter\nAutor: Jesús Camilo Criado Ropero")

    def _on_operation_change(self, event=None):
        op = self.operation_var.get()
        
        if op in ("Escalar×A", "A×Escalar"):
            self.scalar_container.grid()
        else:
            self.scalar_container.grid_remove()

    def _clear(self):
        self.result.clear()

    def _calculate(self):
        op = self.operation_var.get()
        try:
            A = self.matrixA.get_values()
            B = self.matrixB.get_values()
            if op == "A×B":
                res = matmul(A, B)
            elif op == "Escalar×A":
                s_raw = self.scalar_var.get().strip()
                try:
                    s = parse_numeric(s_raw)
                except ValueError:
                    raise ValueError(f"Escalar no numérico: '{s_raw}'")
                res = scalar_mul(s, A)
            elif op == "A×Escalar":
                s_raw = self.scalar_var.get().strip()
                try:
                    s = parse_numeric(s_raw)
                except ValueError:
                    raise ValueError(f"Escalar no numérico: '{s_raw}'")
                res = scalar_mul(s, A)
            else:
                raise ValueError("Operación desconocida")
            self.result.show_matrix(res)
        except Exception as e:
            self.result.show_error(str(e))
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    App().mainloop()
