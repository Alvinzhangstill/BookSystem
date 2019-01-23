from django.shortcuts import render,redirect,HttpResponse
from app01.models import *
# Create your views here.

from app01.models import Book


def add_book(request):
    print(request.method)
    if request.method == "POST":
        title=request.POST.get("title")
        price=request.POST.get("price")
        pub_date=request.POST.get("pub_date")
        publish_id=request.POST.get("publish_id")
        authors_id_list=request.POST.getlist("authors_id_list")   # select,checkbox

        # print("title:",title,"price:",price,"pub_date",pub_date)
        book_obj=Book.objects.create(title=title,price=price,publishDate=pub_date,publish_id=publish_id)

        print(authors_id_list)  # ['1', '2', '4']
        book_obj.authors.add(*authors_id_list)

        return HttpResponse("success!")
    publish_list=Publish.objects.all()
    author_list=Author.objects.all()

    return render(request,"addbook.html",{"publish_list":publish_list,"author_list":author_list})


def books(request):

    book_list=Book.objects.all()
    return render(request,"books.html",{"book_list":book_list})


def change_book(request,book_id):

    book_obj = Book.objects.filter(nid=book_id).first()
    if request.method == "POST":
        title = request.POST.get("title")
        price = request.POST.get("price")
        pub_date = request.POST.get("pub_date")
        publish_id = request.POST.get("publish_id")
        authors_id_list = request.POST.getlist("authors_id_list")

        Book.objects.filter(nid=book_id).update(title=title,price=price,publishDate=pub_date,publish=publish_id,)
        # 先清空旧的作者数据，再添加
        # book_obj.authors.clear()
        # book_obj.authors.add(*authors_id_list)

        # 或者用django提供的set方法
        book_obj.authors.set(authors_id_list)

        return redirect("/books/")

    publish_list=Publish.objects.all()
    authors_list=Author.objects.all()

    return render(request,'change_book.html',{'book_obj':book_obj,"publish_list":publish_list,"authors_list":authors_list})


def delete_book(request,del_book_id):

    Book.objects.filter(pk=del_book_id).delete()

    return redirect("/books/")


def author_works(request,author_id):
    author_obj=Author.objects.filter(pk=author_id).first()
    book_list=author_obj.book_set.all()
    # for book in book_list:
    #     print(book.title)
    # print(book_list)
    return render(request,"books_of_author.html",{"book_list":book_list,"author_obj":author_obj})
    # return HttpResponse("OK")


# commit to repository
