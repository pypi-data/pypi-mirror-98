# ukritlib
เป็นการทดลองใช้งาน Library สำหรับ Python 

Build Package 
```
python setup.py sdist bdist_wheel  
```

Test Packeage
```
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

Push Package
```
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```