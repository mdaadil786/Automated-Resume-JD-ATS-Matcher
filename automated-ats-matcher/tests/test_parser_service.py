import io
from zipfile import ZipFile
from werkzeug.datastructures import FileStorage
from app.services.parser_service import parse_uploaded_files

def test_txt():
    f = FileStorage(stream=io.BytesIO(b"Python SQL Docker"),
                    filename="resume.txt", content_type="text/plain")
    x = parse_uploaded_files([f])
    assert len(x) == 1 and "Python" in x[0]["text"]

def test_nested_zip():
    inner=io.BytesIO()
    with ZipFile(inner,"w") as z: z.writestr("candidate.txt","Java Spring Boot SQL")
    outer=io.BytesIO()
    with ZipFile(outer,"w") as z: z.writestr("nested.zip",inner.getvalue())
    outer.seek(0)
    f=FileStorage(stream=outer,filename="resumes.zip",content_type="application/zip")
    x=parse_uploaded_files([f])
    assert len(x)==1 and "Spring Boot" in x[0]["text"]
