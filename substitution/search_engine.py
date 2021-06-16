from substitution.models import Product, Categories


class Substitutes():
    def __init__(self):
        #     self.ids = find_alt(user_input)
        pass

    def find_alt(self, searched_products):
        normalized_string = self.replace_spec_characs(searched_products)
        list_searched_words = self.isolate_words(normalized_string)
        words_to_compare = self.trim(list_searched_words)
        searched_product_id = self.find_prod(words_to_compare)[0]
        if self.result_found:
            prod_infos = self.get_prod_infos(searched_product_id)
            prod_from_cat_ids = self.get_prod_id_from_cat(
                prod_infos[0])
            self.subs_id = self.get_alt_ids(
                prod_infos[1], prod_from_cat_ids)
            self.prod_found = True
            return self.subs_id, self.prod_found
        else:
            self.subs_id = []
            self.prod_found = False

    def replace_spec_characs(self, input_string):
        """make sure that specific characters
         such as 'é' 'à' are replaced with equivalents"""
        characs_and_subs = {"é": "e", "è": "e", "à": "a", "'": " ", "ù": "u"}
        count = 0
        normalized_string = input_string
        for charac in characs_and_subs:
            # print("charac evaluated: {}".format(charac))
            # print("to be replaced: {}".format(characs_and_subs[charac]))
            normalized_string = normalized_string.replace(
                charac,
                characs_and_subs[charac])
            count += 1
            # print("NORMALIZED STRING: {}".format(normalized_string))
        return normalized_string

    def isolate_words(self, input_string):
        """isolate different words from input"""
        self.all_searched_words = input_string.split()
        return self.all_searched_words

    def trim(self, input_words_list):
        """select all words >2 chars, place them in a list"""
        def to_be_trimmed(x):
            if len(x) < 3:
                return False
            else:
                return True
        self.trimmed_words_list = list(filter(to_be_trimmed, input_words_list))
        # print('the filtered words are:')
        # for word in trimmed_words_list:
        #     print(word)
        return self.trimmed_words_list

    def find_prod(self, words_list):
        """compare one by one the elements of the list of isolated
        words to each product names in DB,
        return the ID of matching product"""
        keep_search = True
        while keep_search:
            for word in words_list:
                print("word evaluated: {}".format(word))
                # self.all_products = Product.objects.all()
                # print("ALL PROD:{}".format(self.all_products))
                self.match_product = Product.objects.filter(
                    product_name__icontains=word)
                print("matching products:{}".format(self.match_product))
                self.match_ids = self.match_product.values('id')
                if self.match_ids:
                    print("IDs matching products:{}".format(
                        self.match_ids))
                    print("MATCH FOUND")
                    self.searched_product_id = (
                        self.match_ids[0]['id'])
                    print("id  product found:{}".format(
                        self.searched_product_id))
                    self.result_found = True
                    keep_search = False
                else:
                    print("MATCH NOT FOUND")
                    self.searched_product_id = '-1'
                    self.result_found = False
            keep_search = False
        return self.searched_product_id, self.result_found

    def get_prod_infos(self, found_product_id):
        """get category and nutriscore of matching product"""
        category = Categories.objects.filter(product_id=found_product_id)
        print("category:{}".format(category))
        self.cat_name = category.values('name')[0]['name']
        print("category NAME:{}".format(self.cat_name))
        self.found_prod = Product.objects.filter(
            pk=found_product_id)
        print("prod found:{}".format(self.found_prod))
        self.nutriscore = self.found_prod.values('nutrition_grade')[
            0]['nutrition_grade']
        return self.cat_name, self.nutriscore

    def get_prod_id_from_cat(self, cat_name):
        """get IDs of all products from the same category"""
        self.prod_from_cat = Categories.objects.filter(name=cat_name)
        print("prod from cat:{}".format(self.prod_from_cat))
        self.ids_prod_from_cat = []
        for prod in self.prod_from_cat.values('product_id'):
            print("PROD:{}".format(prod))
            prod_id = prod['product_id']
            self.ids_prod_from_cat.append(prod_id)
            print("ids of prod from cat:{}".format(self.ids_prod_from_cat))
        return self.ids_prod_from_cat

    def get_alt_ids(self, nutriscore, prod_id_list):
        """get IDs of all products with better nutriscore
         within product ids list received as argument"""
        regex_nutri = '[a-' + nutriscore + ']'
        print("regex_nutri:{}".format(regex_nutri))
        self.alts = Product.objects.filter(
            pk__in=prod_id_list,
            nutrition_grade__regex=regex_nutri)
        print("alts with better nutriscore:{}".format(self.alts))
        self.ids_alts = []
        for prod in self.alts.values('id'):
            print("ALT n°:{}".format(prod))
            prod_id = prod['id']
            self.ids_alts.append(prod_id)
            print("potential alts:{}".format(self.ids_alts))
        return self.ids_alts


if __name__ == "__main__":
    substitute = Substitutes()
    test_words_list = substitute.isolate_words("a DU saucisson Nutella 42")
    trimmed_words_list = substitute.trim(test_words_list)
    found_id = substitute.find_prod(trimmed_words_list).searched_product_id
