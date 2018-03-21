# Import Libraries
import sys
version = (3, 0)
cur_version = sys.version_info
if cur_version >= version:  # If the Current Version of Python is 3.0 or above
    import urllib.request
    from urllib.request import Request, urlopen
    from urllib.request import URLError, HTTPError
    from urllib.parse import quote
    import html
else:  # If the Current Version of Python is 2.x
    import urllib2
    from urllib2 import Request, urlopen
    from urllib2 import URLError, HTTPError
    from urllib import quote
import time  # Importing the time library to check the time of code execution
import os
import argparse
import ssl
import datetime
import json
import re
import codecs

possible_language = ['Arabic','Chinese (Simplified)','Chinese (Traditional)',
                    'Czech','Danish','Dutch','English','Estonian','Finnish',
                    'French','German','Greek','Hebrew','Hungarian','Icelandic',
                    'Italian','Japanese','Korean','Latvian','Lithuanian',
                    'Norwegian','Portuguese','Polish','Romanian','Russian',
                    'Spanish','Swedish','Turkish'
                    ]
img_language = ""

possible_color = ['red', 'orange', 'yellow', 'green', 'teal', 'blue', 'purple',
                 'pink', 'white', 'gray', 'black', 'brown']
img_color = ""

if not img_color:
	img_color = None

popssible_color_type = ['full-color', 'black-and-white', 'transparent']
img_color_type = ''

if not img_color_type:
	img_color_type = None

possible_size = ['large','medium','icon','>400*300','>640*480','>800*600',
                '>1024*768','>2MP','>4MP','>6MP','>8MP','>10MP','>12MP',
                '>15MP','>20MP','>40MP','>70MP'
                ]
img_size = ""

if not img_size:
	img_size = None

possible_type = ['face','photo','clip-art','line-drawing','animated']
img_type = "photo"

if not img_type:
	img_type = None

possible_aspect_ratio = ['tall', 'square', 'wide', 'panoramic']
img_aspect_ratio = ""

if not img_aspect_ratio:
	img_aspect_ratio = None

possible_img_format = ['jpg', 'gif', 'png', 'bmp', 'svg', 'webp', 'ico']
img_format = ""

if not img_format:
	img_format = None

img_similar_images = ''

if img_similar_images:
    current_time = str(datetime.datetime.now()).split('.')[0]
    search_keyword = [current_time.replace(":", "_")]

img_output_directory = "./download"

# If this argument is present, set the custom output directory
if img_output_directory:
    main_directory = img_output_directory
else:
    main_directory = "downloads"

img_delay = '2'

# Set the delay parameter if this argument is present
if img_delay:
    try:
        delay_time = int(img_delay)
    except ValueError:
        print('Delay parameter should be an integer!')
else:
    delay_time = 2


img_limit = 200

# Setting limit on number of images to be downloaded
if img_limit:
    limit = int(img_limit)
    if int(img_limit) >= 200:
        limit = 200
else:
    limit = 200


img_suffix_keywords = ""

#Additional words added to keywords
if img_suffix_keywords:
    suffix_keywords = [" " + str(sk) for sk in img_suffix_keywords.split(',')]
else:
    suffix_keywords = []

img_keywords = "car"

#Initialization and Validation of user arguments
if img_keywords:
    search_keyword = [str(item) for item in img_keywords.split(',')]

img_url = ""

if not img_url :
	img_url = None

img_specific_site = ""

if not img_specific_site:
	img_specific_site = None

img_socket_timeout = None
img_prefix = None
img_print_size = None

img_extract_metadata = None




# make directories
def create_directories(main_directory, dir_name):
    dir_name_thumbnail = dir_name + " - thumbnail"
    # make a search keyword  directory
    try:
        if not os.path.exists(main_directory):
            os.makedirs(main_directory)
            time.sleep(0.2)
            path = str(dir_name)
            sub_directory = os.path.join(main_directory, path)
            if not os.path.exists(sub_directory):
                os.makedirs(sub_directory)
            '''
            if args.thumbnail:
                sub_directory_thumbnail = os.path.join(main_directory, dir_name_thumbnail)
                if not os.path.exists(sub_directory_thumbnail):
                    os.makedirs(sub_directory_thumbnail)
            '''
        else:
            path = str(dir_name)
            sub_directory = os.path.join(main_directory, path)
            if not os.path.exists(sub_directory):
                os.makedirs(sub_directory)
            '''
            if args.thumbnail:
                sub_directory_thumbnail = os.path.join(main_directory, dir_name_thumbnail)
                if not os.path.exists(sub_directory_thumbnail):
                    os.makedirs(sub_directory_thumbnail)
            '''
    except OSError as e:
        if e.errno != 17:
            raise
            # time.sleep might help here
        pass
    return


#Building URL parameters
def build_url_parameters():
    if img_language:
        lang = "&lr="
        lang_param = {
                     "Arabic":"lang_ar","Chinese (Simplified)":"lang_zh-CN",
                     "Chinese (Traditional)":"lang_zh-TW","Czech":"lang_cs",
                     "Danish":"lang_da","Dutch":"lang_nl","English":"lang_en",
                     "Estonian":"lang_et","Finnish":"lang_fi",
                     "French":"lang_fr","German":"lang_de","Greek":"lang_el",
                     "Hebrew":"lang_iw ","Hungarian":"lang_hu",
                     "Icelandic":"lang_is","Italian":"lang_it",
                     "Japanese":"lang_ja","Korean":"lang_ko",
                     "Latvian":"lang_lv","Lithuanian":"lang_lt",
                     "Norwegian":"lang_no","Portuguese":"lang_pt",
                     "Polish":"lang_pl","Romanian":"lang_ro",
                     "Russian":"lang_ru","Spanish":"lang_es",
                     "Swedish":"lang_sv","Turkish":"lang_tr"
                     }
        lang_url = lang+lang_param[language]
    else:
        lang_url = ''

    time_range = ''

    built_url = "&tbs="
    counter = 0
    params = {'color':[img_color,{'red':'ic:specific,isc:red',
                              'orange':'ic:specific,isc:orange',
                              'yellow':'ic:specific,isc:yellow',
                              'green':'ic:specific,isc:green',
                              'teal':'ic:specific,isc:teel',
                              'blue':'ic:specific,isc:blue',
                              'purple':'ic:specific,isc:purple',
                              'pink':'ic:specific,isc:pink',
                              'white':'ic:specific,isc:white',
                              'gray':'ic:specific,isc:gray',
                              'black':'ic:specific,isc:black',
                              'brown':'ic:specific,isc:brown'}],
              'color_type':[img_color_type,{'full-color':'ic:color',
                                        'black-and-white':'ic:gray',
                                        'transparent':'ic:trans'}],
              'size':[img_size,{'large':'isz:l','medium':'isz:m','icon':'isz:i',
                            '>400*300':'isz:lt,islt:qsvga',
                            '>640*480':'isz:lt,islt:vga',
                            '>800*600':'isz:lt,islt:svga',
                            '>1024*768':'visz:lt,islt:xga',
                            '>2MP':'isz:lt,islt:2mp',
                            '>4MP':'isz:lt,islt:4mp',
                            '>6MP':'isz:lt,islt:6mp',
                            '>8MP':'isz:lt,islt:8mp',
                            '>10MP':'isz:lt,islt:10mp',
                            '>12MP':'isz:lt,islt:12mp',
                            '>15MP':'isz:lt,islt:15mp',
                            '>20MP':'isz:lt,islt:20mp',
                            '>40MP':'isz:lt,islt:40mp',
                            '>70MP':'isz:lt,islt:70mp'}],
              'type':[img_type,{'face':'itp:face','photo':'itp:photo',
                                'clip-art':'itp:clip-art',
                                'line-drawing':'itp:lineart',
                                'animated':'itp:animated'}],
              'aspect_ratio':[img_aspect_ratio,{'tall':'iar:t',
                                            'square':'iar:s',
                                            'wide':'iar:w',
                                            'panoramic':'iar:xw'}],
              'format':[img_format,{'jpg':'ift:jpg','gif':'ift:gif',
                                     'png':'ift:png','bmp':'ift:bmp',
                                     'svg':'ift:svg','webp':'webp',
                                     'ico':'ift:ico'}]}
    for key, value in params.items():
        
        if value[0] is not None:
            #print(value)
            ext_param = value[1][value[0]]
            # counter will tell if it is first param added or not
            if counter == 0:
                # add it to the built url
                built_url = built_url + ext_param
                counter += 1
            else:
                built_url = built_url + ',' + ext_param
                counter += 1
    built_url = lang_url+built_url+time_range
    return built_url


def build_search_url(search_term,params):
    # check the args and choose the URL
    if img_url:
        url = img_url
    elif img_similar_images:
        keywordem = similar_images()
        url = 'https://www.google.com/search?q=' + keywordem + \
              '&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch \
              &sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'
    elif img_specific_site:
        url = 'https://www.google.com/search?q=' + quote(
            search_term) + '&as_sitesearch=' + img_specific_site + \
            '&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch' + \
            params + '&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'
    else:
        url = 'https://www.google.com/search?q=' + quote(
            search_term) + \
            '&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch' + \
            params + '&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'
    #print(url)
    return url

#measures the file size
def file_size(file_path):
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        size = file_info.st_size
        for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if size < 1024.0:
                return "%3.1f %s" % (size, x)
            size /= 1024.0
        return size

def download_page(url):
    version = (3, 0)
    cur_version = sys.version_info
    if cur_version >= version:  # If the Current Version of Python is 3.0 or above
        try:
            headers = {}
            headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
            req = urllib.request.Request(url, headers=headers)
            resp = urllib.request.urlopen(req)
            respData = str(resp.read())
            return respData
        except Exception as e:
            print(str(e))
    else:  # If the Current Version of Python is 2.x
        try:
            headers = {}
            headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
            req = urllib2.Request(url, headers=headers)
            try:
                response = urllib2.urlopen(req)
            except URLError:  # Handling SSL certificate failed
                context = ssl._create_unverified_context()
                response = urlopen(req, context=context)
            page = response.read()
            return page
        except:
            return "Page Not found"



# Finding 'Next Image' from the given raw page
def _get_next_item(s):
    start_line = s.find('rg_meta notranslate')
    if start_line == -1:  # If no links are found then give an error!
        end_quote = 0
        link = "no_links"
        return link, end_quote
    else:
        start_line = s.find('class="rg_meta notranslate">')
        start_object = s.find('{', start_line + 1)
        end_object = s.find('</div>', start_object + 1)
        object_raw = str(s[start_object:end_object])
        #####print(object_raw)
        #remove escape characters based on python version
        version = (3, 0)
        cur_version = sys.version_info
        if cur_version >= version: #python3
            object_decode = bytes(object_raw, "utf-8").decode("unicode_escape")
            final_object = json.loads(object_decode)
        else:  #python2
            final_object = (json.loads(repair(object_raw)))
        return final_object, end_object



#Format the object in readable format
def format_object(object):
    formatted_object = {}
    formatted_object['image_format'] = object['ity']
    formatted_object['image_height'] = object['oh']
    formatted_object['image_width'] = object['ow']
    formatted_object['image_link'] = object['ou']
    formatted_object['image_description'] = object['pt']
    formatted_object['image_host'] = object['rh']
    formatted_object['image_source'] = object['ru']
    formatted_object['image_thumbnail_url'] = object['tu']
    return formatted_object

# Download Images
def download_image(image_url,image_format,main_directory,dir_name,count):
    '''
    if img_print_urls:
        print("Image URL: " + image_url)
    '''
    try:
        req = Request(image_url, headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"})
        try:
            # timeout time to download an image
            if img_socket_timeout:
                timeout = float(img_socket_timeout)
            else:
                timeout = 15
            response = urlopen(req, None, timeout)

            # keep everything after the last '/'
            image_name = str(image_url[(image_url.rfind('/')) + 1:])
            image_name = image_name.lower()
            # if no extension then add it
            # remove everything after the image name
            if image_format == "":
                image_name = image_name + "." + "jpg"
            elif image_format == "jpeg":
                image_name = image_name[:image_name.find(image_format) + 4]
            else:
                image_name = image_name[:image_name.find(image_format) + 3]

            # prefix name in image
            if img_prefix:
                prefix = img_prefix + " "
            else:
                prefix = ''

            path = main_directory + "/" + dir_name + "/" + prefix + str(count) + ". " + image_name
            output_file = open(path, 'wb')
            data = response.read()
            output_file.write(data)
            response.close()

            #return image name back to calling method to use it for thumbnail downloads
            return_image_name = prefix + str(count) + ". " + image_name

            download_status = 'success'
            download_message = "Completed Image ====> " + prefix +  str(count) + ". " + image_name

            # image size parameter
            if img_print_size:
                print("Image Size: " + str(file_size(path)))

        except UnicodeEncodeError as e:
            download_status = 'fail'
            download_message = "UnicodeEncodeError on an image...trying next one..." + " Error: " + str(e)
            return_image_name = ''

    except HTTPError as e:  # If there is any HTTPError
        download_status = 'fail'
        download_message = "HTTPError on an image...trying next one..." + " Error: " + str(e)
        return_image_name = ''

    except URLError as e:
        download_status = 'fail'
        download_message = "URLError on an image...trying next one..." + " Error: " + str(e)
        return_image_name = ''

    except ssl.CertificateError as e:
        download_status = 'fail'
        download_message = "CertificateError on an image...trying next one..." + " Error: " + str(e)
        return_image_name = ''

    except IOError as e:  # If there is any IOError
        download_status = 'fail'
        download_message = "IOError on an image...trying next one..." + " Error: " + str(e)
        return_image_name = ''
    return download_status,download_message,return_image_name


def _get_all_items(page,main_directory,dir_name,limit):
    items = []
    errorCount = 0
    i = 0
    count = 1
    while count < limit+1:
        object, end_content = _get_next_item(page)
        if object == "no_links":
            break
        else:
            #format the item for readability
            object = format_object(object)
            '''
            if args.metadata:
                print("\nImage Metadata" + str(object))
            '''
            items.append(object)  # Append all the links in the list named 'Links'

            #download the images
            download_status,download_message,return_image_name = download_image(object['image_link'],object['image_format'],main_directory,dir_name,count)
            print(download_message)
            if download_status == "success":

                # download image_thumbnails
                '''
                if args.thumbnail:
                    download_status, download_message_thumbnail = download_image_thumbnail(object['image_thumbnail_url'],main_directory,dir_name,return_image_name)
                    print(download_message_thumbnail)
                    '''

                count += 1
            else:
                errorCount += 1

            #delay param
            if img_delay:
                time.sleep(int(img_delay))

            page = page[end_content:]
        i += 1
    if count < limit:
        print("\n\nUnfortunately all " + str(
            limit) + " could not be downloaded because some images were not downloadable. " + str(
            count-1) + " is all we got for this search filter!")
    return items,errorCount



def bulk_download(search_keyword,suffix_keywords,limit,main_directory):
    # appending a dummy value to Suffix Keywords array if it is blank
    if len(suffix_keywords) == 0:
        suffix_keywords.append('')

    for sky in suffix_keywords:     # 1.for every suffix keywords
        i = 0
        while i < len(search_keyword):      # 2.for every main keyword
            iteration = "\n" + "Item no.: " + str(i + 1) + " -->" + " Item name = " + str(search_keyword[i] + str(sky))
            print(iteration)
            print("Evaluating...")
            search_term = search_keyword[i] + sky
            dir_name = search_term + ('-' + img_color if img_color else '')   #sub-directory

            create_directories(main_directory,dir_name)     #create directories in OS

            params = build_url_parameters()     #building URL with params

            url = build_search_url(search_term,params)      #building main search url

            raw_html = (download_page(url))     #download page

            print("Starting Download...")
            items,errorCount = _get_all_items(raw_html,main_directory,dir_name,limit)    #get all image items and download images

            #dumps into a text file
            if img_extract_metadata:
                try:
                    if not os.path.exists("logs"):
                        os.makedirs("logs")
                except OSError as e:
                    print(e)
                text_file = open("logs/"+search_keyword[i]+".txt", "w")
                text_file.write(json.dumps(items, indent=4, sort_keys=True))
                text_file.close()

            i += 1
    return errorCount

errorCount = bulk_download(search_keyword,suffix_keywords,limit,main_directory)