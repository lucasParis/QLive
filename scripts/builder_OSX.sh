mkdir Resources
cp *.py Resources/
rm Resources/main.py
cp main.py QLive.py

rm -rf build dist
py2applet --make-setup QLive.py Resources/*
python setup.py py2app --plist=info.plist
rm -f setup.py
rm -rf build
mv dist QLive_OSX

if cd QLive_OSX;
then
    find . -name .git -depth -exec rm -rf {} \
    find . -name *.pyc -depth -exec rm -f {} \
    find . -name .* -depth -exec rm -f {} \;
else
    echo "Something wrong. QLive_OSX not created"
    exit;
fi

# keep only 64-bit arch
ditto --rsrc --arch x86_64 QLive.app QLive-x86_64.app
rm -rf QLive.app
mv QLive-x86_64.app QLive.app

cd ..
cp -R QLive_OSX/QLive.app .

rm -rf QLive_OSX
rm -rf Resources
rm QLive.py
