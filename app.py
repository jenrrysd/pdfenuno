from flask import Flask, render_template, request, redirect, url_for, send_from_directory, after_this_request
from werkzeug.utils import secure_filename
from PyPDF2 import PdfMerger
import os
import time

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['OUTPUT_FOLDER'] = 'static/outputs'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Obtener archivos subidos
        pdf_files = request.files.getlist('pdf_files')
        output_name = request.form.get(
            'output_name', 'merged').strip() or 'merged'

        # Guardar archivos temporalmente
        filenames = []
        for file in pdf_files:
            if file.filename.endswith('.pdf'):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                filenames.append(filename)

        # Combinar PDFs
        merger = PdfMerger()
        for filename in filenames:
            merger.append(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        output_path = os.path.join(
            app.config['OUTPUT_FOLDER'], f"{output_name}.pdf")
        merger.write(output_path)
        merger.close()

        # Limpiar archivos temporales
        for filename in filenames:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        return redirect(url_for('download', filename=f"{output_name}.pdf"))

    return render_template('index.html')


@app.route('/download/<filename>')
def download(filename):
    path = os.path.join(app.config['OUTPUT_FOLDER'], filename)

    @after_this_request
    def remove_file(response):
        try:
            time.sleep(1)  # Espera 1 segundo antes de eliminar (opcional)
            os.remove(path)
        except Exception as e:
            app.logger.error(f"Error al eliminar {path}: {e}")
        return response

    return send_from_directory(app.config['OUTPUT_FOLDER'], filename, as_attachment=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='2020', debug=True)
