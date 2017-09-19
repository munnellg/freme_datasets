#!/usr/bin/env python3
import sys
from itertools import islice
from urllib.parse import urljoin, urlencode
from urllib.request import Request, urlopen
from optparse import OptionParser
from docs.config import freme_url, auth_token, chunk_size

# Build this program's option parser
def build_opt_parser():
    usage = "usage: %prog filename"
    parser = OptionParser(usage=usage)

    parser.add_option ( "-n",
                        "--dataset-name",
                        action="store",
                        dest="dataset_name",
                        default=None,
                        metavar="string",
                        help="The name of the dataset we're targeting" )

    parser.add_option ( "-c",
                        "--create",
                        dest="create",
                        action="store_true",
                        default=False,
                        metavar="boolean",
                        help="Script should create the dataset specified" )

    parser.add_option ( "-l",
                        "--load",
                        dest="load",
                        action="store_true",
                        default=False,
                        metavar="boolean",
                        help="Script should load specified dataset with information" )

    parser.add_option ( "-d",
                        "--delete",
                        dest="delete",
                        action="store_true",
                        default=False,
                        metavar="boolean",
                        help="Script should delete the dataset specified" )

    return parser

# Parse commandline arguments using OptionParser given
def parse_arguments( parser ):
    (options, args) = parser.parse_args()

    return options, args

def send_request( dataset="", headers=dict(), query_string=None, method="GET", body="" ):
    target = urljoin(freme_url, dataset)

    headers["User-Agent"]     = "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)"
    headers["Accept-Charset"] = "utf-8"
    headers["X-Auth-Token"]   =  auth_token
    headers["Content-Type"]   =  "application/n-triples"
    headers["Language"]       =  "en"

    
    if query_string != None:
        query_string = urlencode(query_string)
    
        if target[-1] == "/":
            target = target[:-1]

        target += "?{}".format(query_string)

    request = Request(
        url=target,
        method=method,
        headers=headers
    )

    return urlopen(request, body.encode("utf-8")).read().decode('utf-8')

def dataset_list_all():
    try:
        return send_request()
    except Exception as error:
        print(error)
        exit()

def dataset_exists( name ):

    try:
        send_request( name )
    except Exception as error:
        if error.code == 404:
            return False
        else:
            print(error)
            exit()

    return True

def dataset_examine( name ):
    try:
        return send_request( name )
    except Exception as error:
        print(error)
        exit()

def dataset_create( name, vis, description ):

    data = {
        "name"        : name,
        "description" : description,
        "visibility"  : vis
    }

    print(data)

    try:
        return send_request( method="POST", query_string=data )
    except Exception as error:
        # Print error message in the event of an exception and return
        # an empty string
        print(error)
        exit()

def dataset_delete( name ):
    try:
        return send_request( name, method="DELETE" )
    except Exception as error:
        # Print error message in the event of an exception and return
        # an empty string
        print(error)
        exit()

def dataset_load( name, data, lang ):
    qs = {        
        "language"    : lang,        
    }
    with open(data, "r") as f:
        count = 1
        while True:
            lines = list(islice(f, chunk_size))
            if not lines:
                break
            data = "".join(lines)
            try:
                send_request( name, method="PUT", body=data, query_string=qs )
                count += len(lines)
                print("Loaded {} entities so far".format(count))
                
            except Exception as error:
                # Print error message in the event of an exception and return
                # an empty string
                print(error)
                exit()

def main():
    parser = build_opt_parser()

    (options, args) = parse_arguments(parser)

    if options.dataset_name != None:
        if options.create:
            print("Creating new dataset: {}".format(options.dataset_name))                        
            vis = input("Visibility [private]: ")
            vis = vis if vis != "" else "private"   
            desc = input("Description: ")            
            print(dataset_create(options.dataset_name, vis, desc))

        if options.load:
            print("Loading dataset {}".format(options.dataset_name))
            lang = input("Language [en]: ")
            lang = lang if lang != "" else "en"
            for filename in args:
                dataset_load(options.dataset_name, filename, lang)

        if options.delete:
            print("Are you sure you want to delete this dataset?")
            print("Once it's gone, it's gone forever...")
            to_delete = input("Please type its name again to confirm you know what you're doing: ")

            if to_delete == options.dataset_name:
                print("Deleting!!!")
                print(dataset_delete(options.dataset_name))
            else:
                print("Not deleting")

        if not options.create and not options.load and not options.delete:
            print("Displaying dataset: {}".format(options.dataset_name))
            print( dataset_examine( options.dataset_name ))
    else:
        print("Displaying all datasets")
        print( dataset_list_all() )

if __name__=="__main__":
    main()
