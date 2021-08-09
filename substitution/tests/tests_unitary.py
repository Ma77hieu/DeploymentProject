from authentification.models import User
from django.test import TestCase
from substitution.search_engine import Substitutes
from substitution.services import Services
from substitution.models import Product, Ratings
from django.http import HttpRequest


class searchEngineTests(TestCase):
    fixtures = ['substitution.json', 'users.json', 'favs.json', 'ratings.json']
    substitute = Substitutes()
    specific_charac_string = "aaeeee  uu"
    assertion_list = ['a', 'DU', 'saucisson', 'Nutella', '42']
    assertion_trimmed_words_list = [
        'saucisson', 'Nutella']
    assertion_trimmed_words_list_2 = [
        'iubiube', 'Abricot']
    assertion_trimmed_words_list_3 = [
        'iubiube', 'iqzerubgilteub', 'haej', 'k,ufipoaqerg']

    def test_replace_spec_characs(self):
        """test the replace_spec_characs function of search_engine.py"""
        normalized_string = self.substitute.replace_spec_characs(
            "àaéeèe' ùu")
        self.assertEqual(normalized_string, self.specific_charac_string)

    def test_isolate_words(self):
        """test the isolate_words function of search_engine.py"""
        test_words_list = self.substitute.isolate_words(
            "a DU saucisson Nutella 42")
        self.assertEqual(test_words_list, self.assertion_list)

    def test_trim(self):
        """test the trim function of search_engine.py"""
        trimmed_words_list = self.substitute.trim(self.assertion_list)
        self.assertEqual(trimmed_words_list, self.assertion_trimmed_words_list)

    def test_find_prod_Nutella(self):
        """test the find_prod function of
        search_engine.py with "Nutella" input"""
        self.substitute.find_prod(self.assertion_trimmed_words_list)
        prod_id_1 = self.substitute.searched_product_id
        is_prod_found_1 = self.substitute.result_found
        self.assertEqual(prod_id_1, 127)
        self.assertEqual(is_prod_found_1, True)

    def test_find_prod_Abricot(self):
        """test the replace_spec_characs function with "Abricot" input"""
        self.substitute.find_prod(self.assertion_trimmed_words_list_2)
        prod_id_2 = self.substitute.searched_product_id
        is_prod_found_2 = self.substitute.result_found
        self.assertEqual(prod_id_2, 105)
        self.assertEqual(is_prod_found_2, True)

    def test_find_prod_FAIL(self):
        """test the 'no product found' scenario of
        the find_prod function of search_engine.py"""
        self.substitute.find_prod(self.assertion_trimmed_words_list_3)
        prod_id_3 = self.substitute.searched_product_id
        is_prod_found_3 = self.substitute.result_found
        self.assertEqual(prod_id_3, '-1')
        self.assertEqual(is_prod_found_3, False)

    def test_get_prod_infos(self):
        """test the get-prod_infos function of search_engine.py"""
        self.substitute.get_prod_infos(125)
        cat = self.substitute.cat_name
        nutri = self.substitute.nutriscore
        self.assertEqual(cat, 'Snacks')
        self.assertEqual(nutri, 'd')

    def test_get_prod_id_from_cat(self):
        """test the get_prod_id_from_cat
         function of search_engine.py"""
        self.substitute.get_prod_id_from_cat('Snacks')
        ids = self.substitute.ids_prod_from_cat
        self.assertEqual(
            ids, [125, 126, 127, 128, 129, 130, 131, 132, 133, 134])

    def test_get_alt_ids(self):
        """test the get_alt_ids function of search_engine.py"""
        self.substitute.get_alt_ids(
            'd', [125, 126, 127, 128, 129, 130, 131, 132, 133, 134])
        alts = self.substitute.ids_alts
        self.assertEqual(alts, [125, 126, 129, 130, 131, 132])

    def test_global_search_engine(self):
        """test the global 'find_alt' function of search_engine.py"""
        global_alt_ids = self.substitute.find_alt(
            "Un truc avec de l Abricot")
        print("global: {}".format(global_alt_ids))
        self.assertEqual(global_alt_ids, (
                         [105, 106, 109, 110, 112], True))

    def test_add_rating(self):
        """tests the addition of a rating to a product"""
        initial_rating = Ratings.objects.filter(
            product_id=109).values_list('rating', flat=True)[0]
        # print("initial rating: {}".format(initial_rating))
        test_request = HttpRequest()
        test_request.POST = {"rating": 4}
        test_user = User(pk=36)
        test_request.user = test_user
        test_request.method = "POST"
        test_product = Product.objects.get(pk=109)
        # print("test_request.POST: {}".format(test_request.POST))
        # print("test_request.user.id: {}".format(test_request.user.id))
        Services().get_rating(test_request, test_product)
        new_ratings = Ratings.objects.filter(
            product_id=109).values_list('rating', flat=True)
        all_ratings = []
        for rating in new_ratings:
            all_ratings.append(rating)
            # print("all ratings:{}".format(all_ratings))
        old_and_new_ratings = [initial_rating, all_ratings]
        self.assertEqual(old_and_new_ratings, (
                         [0, [0, 4]]))
