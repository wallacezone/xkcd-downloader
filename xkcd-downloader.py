# -------------------------------------------------------------------
#
# XKCD Downloader (v1.0)
#
# A simple xkcd downloader by Alessandro Barbieri
#
# Code available at: https://github.com/wallacezone/xkcd-downloader
#
# -------------------------------------------------------------------

import os, requests, subprocess

os.makedirs('xkcd', exist_ok=True) # store comics in ./xkcd

last_comic_url = 'http://xkcd.com/info.0.json'
comic_url = 'http://xkcd.com/NUM/info.0.json'

# ask the user for the number of comics to download
print()
print(' How many comics to do you want to download? (Last to first)')
print()

while True:
    input_number = input(' > ')
    print()

    try:
        input_number = int(input_number)
        break
    except ValuError:
        continue

# get the last comic json and get comic number
try:
    res = requests.get(last_comic_url)
    res.raise_for_status()
except Exception as err:
    print(err)
    exit(0)

try:
    last_comic_json = res.json()
except ValueError as err:
    print(err)
    exit(0)

last_comic_number = last_comic_json['num']

saved_imgs = 0

# loop through comics
for i in range(last_comic_number, last_comic_number - input_number, -1):

	# check whether loop hase reached first comic
    if i == 1:
    	break

    # download json and convert it
    try:
        res = requests.get(comic_url.replace('NUM', str(i)))
        res.raise_for_status()
    except Exception as err:
        print(err)
        exit(0)

    try:
        comic_json = res.json()
    except ValueError as err:
        print(err)
        continue

    # get img url
    img_url = comic_json['img']

    # download img
    print(' Downloading comic #' + str(i))
    try:
        res = requests.get(img_url)
        res.raise_for_status()
    except Exception as err:
        print(err)
        continue

    # save it
    img_file = open(os.path.join('xkcd', str(i) + '.png'), 'wb')
    for chunk in res.iter_content(100000):
        img_file.write(chunk)
    img_file.close()
    saved_imgs += 1

print()
print(' Successfully downloaded ' + str(saved_imgs) + ' comics')
print()

# open explorer on this directory
subprocess.Popen(r'explorer "' + os.getcwd() + r'\xkcd"')