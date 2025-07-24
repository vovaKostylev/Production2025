from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from ADAR import solve_ADAR

def render_latex_steps(steps):
    app = QApplication([])

    # Генерация HTML с MathJax (используем raw-строки)
    html_parts = []
    for title, equations in steps:
        html_parts.append(f"<h2>{title}</h2>")
        html_parts.append("<div style='margin-left: 20px;'>")
        for eq in equations:
            html_parts.append(rf"<p>\[ {eq} \]</p>")  # Используем rf-строку
        html_parts.append("</div>")

    html_content = r"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
        <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
        <style>
            body { font-family: Arial; padding: 20px; }
            h2 { color: #2c3e50; border-bottom: 1px solid #eee; padding-bottom: 5px; }
            p { margin: 10px 0; }
        </style>
    </head>
    <body>
        <h1>Решение методом АКАР</h1>
    """ + "\n".join(html_parts) + r"""
    </body>
    </html>
    """

    # Настройка окна просмотра
    web_view = QWebEngineView()
    web_view.setHtml(html_content)

    window = QWidget()
    layout = QVBoxLayout()
    layout.addWidget(web_view)
    window.setLayout(layout)
    window.resize(1000, 800)
    window.setWindowTitle("Аналитическое конструирование агрегированных регуляторов")
    window.show()
    app.exec_()

# Запуск решения и отображения
if __name__ == "__main__":
    steps = solve_ADAR()
    render_latex_steps(steps)