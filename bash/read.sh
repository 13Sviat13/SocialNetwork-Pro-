#1/bin/bash

echo "Enter the name of file"
read filename

if [ ! -f "$filename" ]; then
  echo "File is no found"
  exit 1
fi

echo "Inside $filename:"
cat "$filename"