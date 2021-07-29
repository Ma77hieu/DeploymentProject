from substitution.models import Product, Favorites, Ratings
from authentification.models import User
from substitution.forms import RatingForm
from django.core.paginator import Paginator
from .constants import NBR_RESULTS_PER_PAGE as per_page
from .constants import NOT_LOGGED_IN, NO_PROD_FOUND
from substitution.search_engine import Substitutes
import logging


class Services():
    def __init__(self):
        pass

    def search_a_prod(self, request):
        """uses the search engine to find a matching product and
        the alternatives, returns paginated results"""
        fav_saved = False
        if request.user.id:
            fav_product_id = request.GET.get('fav_prod')
            if fav_product_id:
                fav = Favorites(product_id=fav_product_id,
                                user_id=request.user.id)
                fav.save()
                fav_saved = True
        # print("fav_saved: {}".format(fav_saved))
        searched_product = request.GET.get('searched_product')
        # print("SEARCHED PROD: {}".format(searched_product))
        alt = Substitutes()
        if alt.find_alt(searched_product):
            alt_products_ids = alt.find_alt(searched_product)[0]
            # print("PRODUCTS ID: {}".format(alt_products_ids))
            search_match_product_id = alt.searched_product_id
            search_match_product = Product.objects.get(
                pk=search_match_product_id)
            # print("SEARCH_MATCH_PRODUCT: {}".format(
            #     search_match_product))
            # print("SEARCH_MATCH_PRODUCT IMAGE: {}".format(
            #     search_match_product.image_front_small_url))
            products = Product.objects.filter(pk__in=alt_products_ids)
            paginator = Paginator(products, per_page)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            redirect_to = "results.html"
            context = {
                'products': products,
                'searched_product': searched_product,
                'search_match_product': search_match_product,
                'page_obj': page_obj,
                'fav_saved': fav_saved}
            self.log_search_with_results(request,True)
        else:
            redirect_to = "home.html"
            error = NO_PROD_FOUND
            context = {'error': error}
            self.log_search_with_results(request,False)
        return (redirect_to, context)

    def log_search_with_results(self,request, is_match_found):
        logger = logging.getLogger(__name__)
        if is_match_found:
            log_message="A successfull search have been made"
        else:
            log_message="A search have been made but no results have been found"
        logger.error(log_message, exc_info=True, extra={
        # Optionally pass a request and we'll grab any information we can
        'request': request,
    })



    def details(self, request, product_id):
        """access a specific product details page based on product id"""
        product = Product.objects.get(pk=product_id)
        nutriscore_list = ['a', 'b', 'c', 'd', 'e']
        redirect_to = 'detailprod.html'
        form=self.get_rating(request, product)
        context = {'form':form,'product': product, 'nutriscore_list': nutriscore_list}
        return (redirect_to, context)

    def get_rating(self, request, rated_product):
        if request.method == "POST":
            user_rating = request.POST['rating']
            user_currently_rating = User.objects.get(pk=request.user.id)
            rating_to_save=Ratings(
                product=rated_product,user=user_currently_rating,rating=user_rating)
            rating_to_save.save()
            all_ratings_of_product=Ratings.objects.filter(
                product_id=rated_product).values_list('rating', flat=True)
            print('all ratings of the product: {}'.format(all_ratings_of_product))
            avg_product_rating=sum(all_ratings_of_product)/len(all_ratings_of_product)
            print('AVERAGE rating of the product: {}'.format(avg_product_rating))
            product_to_update=Product.objects.get(pk=rated_product.id)
            product_to_update.average_rating=avg_product_rating
            product_to_update.save()
        form = RatingForm()
        return form


    def mesaliments(self, request):
        """access the saved favorites of a user based on logged user id"""
        if request.user.id:
            favorites = Favorites.objects.filter(
                user_id=request.user.id).values('product_id')
            # print("FAVORITES OF THE USER: {}".format(favorites))
            favs = []
            for favorite in favorites:
                # print("FAVORITE: {}".format(favorite))
                # print("FAVORITE PRODUCT ID: {}".format(
                #     favorite["product_id"]))
                favs.append(favorite["product_id"])

            # print("IDs FAVORITES OF THE USER: {}".format(favs))
            products = Product.objects.filter(pk__in=favs)
            paginator = Paginator(products, per_page)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            favoritepage = True
            redirect_to = 'results.html'
            context = {
                'products': products,
                'page_obj': page_obj,
                'is_favorite_page': favoritepage}
        else:
            error = NOT_LOGGED_IN
            redirect_to = 'home.html'
            context = {'error': error}
        return (redirect_to, context)
