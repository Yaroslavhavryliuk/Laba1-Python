import sys

from colorama import Fore
import lxml.etree as ET
import os.path
import sys

def greenText(message):
	print(Fore.GREEN + message)

def redText(message):
	print(Fore.RED + message)

def blueText(message):
	print(Fore.BLUE + message)

def yellowText(message):
	print(Fore.YELLOW + message)


class Author:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.books = set()

class Book:
    def __init__(self, id, title, genre, pages):
        self.id = id
        self.title = title
        self.genre = genre
        self.pages = pages

class Library:
    def __init__(self):
        self.authors = dict()
        self.books = dict()

    def сlean(self):
        self.authors = dict()
        self.books = dict()

    def printData(self):
        for authorId in self.authors:
            yellowText('Author:  id: ' + str(self.authors[authorId].id) + '  name: ' + self.authors[authorId].name)
            for book in self.authors[authorId].books:
                blueText('Book:  id: ' + str(book.id) + '  title: ' + book.title +
                      '  genre: ' + book.genre + '  pages: ' + str(book.pages))

    def saveToFile(self, filename):
        root = ET.Element('Library')
        xmltree = ET.ElementTree(root)
        xmlauthors = ET.SubElement(root, 'Authors')
        for key, value in self.authors.items():
            author = ET.SubElement(xmlauthors, 'Author')
            author.set('id', str(key))
            author.set('name', str(value.name))
            xmlbooks = ET.SubElement(author, 'Books')
            for bookel in value.books:
                book = ET.SubElement(xmlbooks, 'Book')
                book.set('id', str(bookel.id))
                book.set('title', str(bookel.title))
                book.set('genre', str(bookel.genre))
                book.set('pages', str(bookel.pages))

        with open(filename, 'wb') as f:
            xmltree.write(f, encoding='utf-8')
        greenText('Saved to file')

    def loadFromFile(self, filename):
        self.сlean()
        if not os.path.isfile(filename):
            redText('Incorrect file name')
            return
        if os.stat(filename).st_size == 0:
            redText('File is empty')
            return
        try:
            xml_file = ET.parse(filename)
            xml_validator = ET.XMLSchema(file = 'schema.xsd')
            xml_validator.validate(xml_file)
        except:
            redText('File validation error')
            return
        for xml_author in xml_file.findall('Authors/Author'):
            authorId = int(xml_author.get('id'))
            authorName = xml_author.get('name')
            author = Author(authorId, authorName)
            for xml_book in xml_author.findall('Books/Book'):
                bookId = int(xml_book.get('id'))
                bookTitle = xml_book.get('title')
                bookGenre = xml_book.get('genre')
                bookPages = int(xml_book.get('pages'))
                book = Book(bookId, bookTitle, bookGenre, bookPages)
                author.books.add(book)
                self.books[bookId] = book

            self.authors[authorId] = author

        self.printData()

    def addAuthor(self, author):
        if len(self.authors) == 0:
            key = 0
        else:
            key = max(self.authors.keys()) + 1
        author.id = key
        self.authors[key] = author
        greenText('Author added')

    def addBook(self, authorId, book):
        if len(self.books) == 0:
            key = 0
        else:
            key = max(self.books.keys()) + 1
        book.id = key
        self.books[key] = book
        self.authors[authorId].books.add(book)
        greenText('Book added')

    def editAuthor(self, authorId):
        if not authorId in self.authors.keys():
            redText('Incorrect id')
            return
        greenText('Enter new author name:')
        newName = input()
        self.authors[authorId].name = newName
        greenText('Author edited')

    def editBook(self, authorId, bookId):
        if not authorId in self.authors.keys() or not bookId in self.books.keys():
            redText('Incorrect id:')
            return
        greenText('What do you want to change? \n' +
              '1. Book title \n' +
              '2. Book genre \n' +
              '3. Book pages number')
        chose = int(input())
        if chose == 1:
            greenText('Enter new title: ')
            newTitle = input()
            self.books[bookId].title = newTitle
        elif chose == 2:
            greenText('Enter new genre: ')
            newGenre = input()
            self.books[bookId].genre = newGenre
        elif chose == 3:
            greenText('Enter new number of pages: ')
            newPages = int(input())
            self.books[bookId].pages = newPages
        else:
            redText('Unknown command')
            return
        for book in self.authors[authorId].books:
            if book.id == bookId:
                book = self.books[bookId]
                return
        greenText('Book edited')

    def deleteAuthor(self, authorId):
        if not authorId in self.authors.keys():
            redText('Incorrect id')
            return
        for book in self.authors[authorId].books:
            del self.books[book.id]
        del self.authors[authorId]
        greenText('Author deleted')

    def deleteBook(self, authorId, bookId):
        if not authorId in self.authors.keys() or not bookId in self.books.keys():
            redText('Incorrect id:')
            return
        del self.books[bookId]
        for book in self.authors[authorId].books:
            if book.id == bookId:
                self.authors[authorId].books.remove(book)
                greenText('Book deleted')
                return


    def getAuthor(self, authorId):
        if not authorId in self.authors.keys():
            redText('Incorrect id')
            return
        searchedAuthor = self.authors[authorId]
        yellowText('Author:  id: ' + str(searchedAuthor.id) + '  name: ' + searchedAuthor.name)

    def getBook(self, bookId):
        if not bookId in self.books.keys():
            redText('Incorrect id')
            return
        searchedBook = self.books[bookId]
        blueText('Book:  id: ' + str(searchedBook.id) + '  title: ' + searchedBook.title +
              '  genre: ' + searchedBook.genre + '  pages: ' + str(searchedBook.pages))

    def printAllAuthors(self):
        for author in self.authors.values():
            yellowText('Author:  id: ' + str(author.id) + '  name: ' + author.name)

    def printBooks(self, authorId):
        if not authorId in self.authors.keys():
            redText('Incorrect id')
            return
        yellowText('Books of ' + self.authors[authorId].name + ':')
        for book in self.authors[authorId].books:
            blueText('Book:  id: ' + str(book.id) + '  title: ' + book.title +
                  '  genre: ' + book.genre + '  pages: ' + str(book.pages))


def parseOptions(args):
    options = dict()
    for arg in args:
        if arg.startswith('-'):
            options[arg[1]] = arg[2:]
    return options



if __name__ == '__main__':
    opts = parseOptions(sys.argv)
    xsd_file = opts.get('s', 'schema.xsd')
    data_file = opts.get('s', 'library.xml')

    library = Library()

    while True:
        greenText('Choose the command:\n' +
              '1. Load data from file\n' +
              '2. Save data to file\n' +
              '3. Add new author\n' +
              '4. Add new book\n' +
              '5. Edit author information\n' +
              '6. Edit book information\n' +
              '7. Delete author\n' +
              '8. Delete book\n' +
              '9. Find author\n' +
              '10. Find book\n' +
              '11. Print all authors\n' +
              '12. Print all books of author\n' +
              '13. Exit')
        chosen = int(input())
        if chosen == 1:
            library.loadFromFile(data_file)
        elif chosen == 2:
            library.saveToFile(data_file)
        elif chosen == 3:
            greenText('Enter author name: ')
            authorName = input()
            newAuthor = Author(0, authorName)
            library.addAuthor(newAuthor)
        elif chosen == 4:
            greenText('Enter the author id: ')
            authorId = int(input())
            greenText('Enter the book title: ')
            bookTitle = input()
            greenText('Enter the book genre: ')
            bookGenre = input()
            greenText('Enter the book pages number: ')
            bookPages = int(input())
            newBook = Book(0, bookTitle, bookGenre, bookPages)
            library.addBook(authorId, newBook)
        elif chosen == 5:
            greenText('Enter the author id: ')
            authorId = int(input())
            library.editAuthor(authorId)
        elif chosen == 6:
            greenText('Enter the author id: ')
            authorId = int(input())
            greenText('Enter the book id: ')
            bookId = int(input())
            library.editBook(authorId, bookId)
        elif chosen == 7:
            greenText('Enter the author id: ')
            authorId = int(input())
            library.deleteAuthor(authorId)
        elif chosen == 8:
            greenText('Enter the author id: ')
            authorId = int(input())
            greenText('Enter the book id: ')
            bookId = int(input())
            library.deleteBook(authorId, bookId)
        elif chosen == 9:
            greenText('Enter the author id: ')
            authorId = int(input())
            library.getAuthor(authorId)
        elif chosen == 10:
            greenText('Enter the book id: ')
            bookId = int(input())
            library.getBook(bookId)
        elif chosen == 11:
            library.printAllAuthors()
        elif chosen == 12:
            greenText('Enter the author id: ')
            authorId = int(input())
            library.printBooks(authorId)
        elif chosen == 13:
            exit()
        else:
            redText('Unknown command')










