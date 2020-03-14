from firebase_admin import credentials, firestore, initialize_app
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import os
from datetime import datetime
from http import HTTPStatus
from django.views.decorators.csrf import csrf_exempt



DIR_PATH = os.path.dirname(os.path.realpath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# firestore import

cred = credentials.Certificate(DIR_PATH + "\serviceAccountKey.json")
default_app = initialize_app(cred)
db = firestore.client()

# get Collection from Firestore


def getListCollections(collection_name):
    collection_object = db.collection(collection_name).order_by(
        "created", direction=firestore.Query.DESCENDING).stream()
    collections = []
    for collection in collection_object:
        book_data = {
            "_id": collection.id,
            "collects": collection.to_dict()
        }
        collections.append(book_data)
    return collections

# get One Collection with ID


def getCollection(collect_name, doc_id):
    collection_object = db.collection(collect_name).document(doc_id).get()
    collectiion = {
        "_id": collection_object.id,
        "collect": collection_object.to_dict()
    }
    return collectiion

# get collections ID


def getCollects_ID(collect_name):
    collection_object = db.collection(collect_name).stream()
    collections = []
    for collection in collection_object:
        book_data = {
            "_id": collection.id,
        }
        collections.append(book_data)
    return collections

# create document


def createDocument(collect_name, collect_data):
    try:
         db.collection(collect_name).add(collect_data)
         added_data = queryCollectionLatesAdded(collect_name)
         return added_data
    except Exception as e:
        return e
    return []

# query collection
def queryCollectionLatesAdded(collect_name):
     collection_lastest = db.collection(collect_name).order_by(
         "created", direction=firestore.Query.DESCENDING).limit(1).stream()
     collection_once = []
     for collection in collection_lastest:
        book_data = {
            "_id": collection.id,
            "collect": collection.to_dict()
        }
        collection_once.append(book_data)
     return collection_once
 
def updateDocument(collect_name, doc_id, data):
     collection_object = db.collection(collect_name).document(doc_id)
     try:
         collection_object.update(data)
         updated = getCollection(collect_name, doc_id)
         return updated
     except Exception as e:
         return e
     
def deleteDocument(collect_name, doc_id):
    
     try:
         collection_object = db.collection(collect_name).document(doc_id).delete()
         deleted = getCollection(collect_name, doc_id)
         return deleted
     except Exception as e:
         return e
 
# home
def home(request):
    books = getListCollections("books")
    return JsonResponse(books, safe=False)
    return render(request, "home.html")

# list all books
def books(request):
    # return render(request, "register.html")
    books = getListCollections("books")
    return JsonResponse(books, safe=False)

def createBook(request):
    if request.method == "POST":
        
        book = {
            "id": int(datetime.now().timestamp()),
            "name": request.POST.get("name"),
            "desc": request.POST.get("desc"),
            "num": int(request.POST.get("num")),
            "price": float(request.POST.get("price")),
            "created": datetime.now(),
            "deleted": "",
            "updated": ""
        }
        try:
            added = createDocument("books", book)
            return JsonResponse(added, safe=False, status=200)
        except Exception as e:
            return JsonResponse(e, safe=False)
    else:
        return JsonResponse({"message": "Method {} not Allowed".format(request.method)}, safe=False, status=405)
    
def updateBook(request, doc_id):
    if request.method == "PUT":
        if doc_id:
            try:
                book_update = request.PUT
                book_update.updated = datetime.now()
                
                updated = updateDocument("books", doc_id, book_update)
                return JsonResponse(updated, safe=False, status=200)
            
            except Exception as e:
                return JsonResponse(e, safe=False, status=500)
        else:
            return JsonResponse({"messag": "id invalid"}, safe=False, sttaus=406)
    else:
        return JsonResponse({"messag": "Method {} not Allowed".format(request.method)}, safe=False, status=405)
            
    return JsonResponse([], safe=False, status=204)

def deleteBook(request, doc_id):
    if request.method == "DELETE":
        if doc_id:
            try:
                deleted = deleteDocument("books", doc_id)
                return JsonResponse(deleted, safe=False, status=200)
            except Exception as e:
                return JsonResponse(e, safe=False, sttaus=500)
        else:
            return JsonResponse({"messag": "id invalid"}, safe=False, status=405)
    else:
        return JsonResponse({"messag": "Method {} not Allowed".format(request.method)}, safe=False, status=500)
            
    return JsonResponse([], safe=False, status=404)
    
        
