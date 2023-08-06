from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter
import click
from pathlib import Path
from tqdm import tqdm
import os


@click.group()
def pdfmagic():
    pass


@pdfmagic.command()
@click.argument("inputdir")
@click.option("--outpath", default=None, type=str, help="Path to the output file.")
def mergedir(inputdir, outpath):
    """Merge all pdf files in the INPUTDIR, files will be ordered alphabetically."""
    inputdir = Path(inputdir)
    if outpath is None:
        outpath = str(inputdir) + "_merged.pdf"

    output = PdfFileMerger()
    pdfs_paths = sorted(list(inputdir.glob("*.pdf")))
    for pdfpath in tqdm(pdfs_paths):
        output.append(PdfFileReader(str(pdfpath)))

    output.write(str(outpath))


@pdfmagic.command()
@click.argument("file")
@click.argument("pages", type=int, nargs=-1)
@click.option("--outpath", default=None, type=str, help="Path to the output file.")
def extpages(file, pages, outpath):
    """Extract input page numbers from .pdf (page numbers start on 1)."""
    pdf = PdfFileReader(file)
    if max(pages) > pdf.getNumPages():
        raise ValueError(f"File {file} has only {pdf.getNumPages()} pages.")

    output = PdfFileWriter()

    for page in pages:
        output.addPage(pdf.getPage(page - 1))

    if outpath is None:
        outpath = (
            os.path.splitext(file)[0] + "_" + ",".join([str(p) for p in pages]) + ".pdf"
        )
    print(outpath)
    with open(outpath, "wb") as f:
        output.write(f)
