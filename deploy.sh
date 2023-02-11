source venv/bin/activate
rm -rf build dist
python3 setup.py py2app
mv dist/accord.app/Contents/Resources/lib/python38.zip dist/accord.app/Contents/Resources/lib/temp.zip
mkdir dist/accord.app/Contents/Resources/lib/python38.zip
unzip dist/accord.app/Contents/Resources/lib/temp.zip -d dist/accord.app/Contents/Resources/lib/python38.zip
rm dist/accord.app/Contents/Resources/lib/temp.zip
./dist/accord.app/Contents/MacOS/accord
