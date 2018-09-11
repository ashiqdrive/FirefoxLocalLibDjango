import datetime
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from catalog.models import Book, Author, BookInstance, Genre
from catalog.forms import RenewBookForm

@login_required
def index(request):
	"""View Function for home page"""

	# Number of visits to this view, as counted in the session variable.
	num_visits = request.session.get('num_visits', 0)
	request.session['num_visits'] = num_visits + 1
	
	#Generate Counts of some main objects
	num_books = Book.objects.all().count()
	num_instances = BookInstance.objects.all().count()

	# Available books (status = 'a')
	num_instances_available = BookInstance.objects.filter(status__exact='a').count()

	# The 'all()' is implied by default.
	num_authors = Author.objects.count()

	num_genre = Genre.objects.all().count()

	#context variable (a Python dictionary containing the data that will be inserted into those placeholders). 
	context = {
		'num_books': num_books,
		'num_instances': num_instances,
		'num_instances_available': num_instances_available,
		'num_authors': num_authors,
		'num_genre':num_genre,
		'num_visits': num_visits,
		}
	
	# Render the HTML template index.html with the data in the context variable
	return render(request, 'index.html', context=context)

class BookListView(LoginRequiredMixin,generic.ListView):
    model = Book
    """By default this will call the modelname_list.html from template (i.e) book_list.html because you called book as model"""
    context_object_name = 'my_book_list'
    paginate_by=5  # your own name for the list as a template variable
    #queryset = Book.objects.filter(title__icontains='aqeeda')# Get 5 books containing the title war
    #template_name = 'books/my_arbitrary_template_name_list.html'# Specify your own template name/location

    """def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(BookListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        return context"""

class BookDetailView(LoginRequiredMixin,generic.DetailView):
    model = Book

class AuthorListView(LoginRequiredMixin,generic.ListView):
	model=Author
	context_object_name='my_author_list'
	queryset=Author.objects.all()
	template_name = 'customAuthorList.html'
	
class AuthorDetailView(LoginRequiredMixin,generic.DetailView):
	model=Author
	template_name = 'customAuthorDetail.html'

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name ='catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10
    
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class SeeLoanedBooksListView(LoginRequiredMixin,PermissionRequiredMixin,generic.ListView):
	"""Generic class based listview to see all books loaned with user name"""
	permission_required='catalog.can_mark_returned'
	model=BookInstance
	template_name='catalog/see_all_loaned_books.html'
	def get_queryset(self):
		return BookInstance.objects.filter(status__exact='o').order_by('due_back')

def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        #book_renewal_form = RenewBookForm(request.POST)
        brf = RenewBookForm(request.POST)
        
        # Check if the form is valid:
        if brf.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = brf.cleaned_data['due_back']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        #book_renewal_form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})
        brf = RenewBookForm(initial={'due_back': proposed_renewal_date})

    context = {
        'form': brf,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)

#________________________________________________________________________
#_______________Author Generic View______________________________________
#________________________________________________________________________
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

class AuthorCreate(CreateView):
    model=Author
    fields='__all__'
    initial={'date_of_death':'05/01/2018'}#just for learning purpose that you can set initial values
    btValue="Create Author"
    #passing context to templete
    def get_context_data(self, **kwargs):
        ctx = super(AuthorCreate, self).get_context_data(**kwargs)
        ctx['btValue'] = self.btValue
        return ctx

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    btValue="Update !"
    #passing context to templete
    def get_context_data(self, **kwargs):
        ctx = super(AuthorUpdate,self).get_context_data(**kwargs)
        ctx['btValue'] = self.btValue
        return ctx

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')

#________________________________________________________________________
#_______________Book Generic View________________________________________
#________________________________________________________________________

class BookCreate(CreateView):
    model=Book
    fields = '__all__'

class BookUpdate(UpdateView):
    model=Book
    fields = '__all__'

class BookDelete(DeleteView):
    model=Book
    success_url = reverse_lazy('books')