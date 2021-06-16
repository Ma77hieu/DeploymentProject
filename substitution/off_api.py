"""
Extraction of the data from the Open food fact (OFF) API
"""

import json
import requests
from .constants import NBR_CAT, NBR_PROD
from .models import Product
from .models import Categories
# from category import Category
# from product import Product


class OffApiData():

    """
    This class represents the data extracted from the OFF API
    """

    def __init__(self):
        self.data_loaded = False
        self.cat_list = None
        self.categories = None
        self.product_name = None
        self.nutriscore = None
        self.image = None
        self.url = None
        self.image = None
        self.energy_kj = None
        self.energy_kcal = None
        self.fat = None
        self.fiber = None
        self.proteins = None
        self.salt = None

    def get_info(self):
        """
        Get the information we need from the OFF API
        """
        self.get_categories()
        self.get_products()

    def get_categories(self):
        """
        Sends a request to the OFF API to receive a list of categories
        """
        self.cat_list = []
        url_req_categories = (
            'https://fr.openfoodfacts.org/categories.json&limit='
            + str(NBR_CAT+1)
        )
        print("categories request: {}\n".format(url_req_categories))
        self.categories = requests.get(url_req_categories)
        categories_json = json.loads(
            self.categories.content.decode('utf-8'))
        for each_cat in range(0, NBR_CAT):
            print("loading CATEGORY {} ".format(each_cat+1))
            cat_name = categories_json["tags"][each_cat]["name"]
            self.cat_list.append(cat_name)
            # self.category.insert_cat(cat_name)

    def get_products(self):
        """
        Sends a request to the OFF API to receive a list of products
        within a specific category
        """
        # elem = str
        for cat_name in self.cat_list:
            for prod in range(0, NBR_PROD):
                print("loading PRODUCT {} from CAT {} "
                      .format(prod+1, cat_name))
                products_url = (
                    "https://fr.openfoodfacts.org/cgi/search.pl"
                    "?action=process&tagtype_0=categories"
                    "&tag_contains_0"
                    "=contains&tag_0="
                    + cat_name
                    + '&json=true&page_size='
                    + str(NBR_PROD)
                    + '&page=1'
                )
                print("products request: {}\n".format(products_url))
                products = requests.get(products_url)
                p_json = json.loads(products.content.decode('utf-8'))
                self.product_name = (
                    p_json["products"][prod]["product_name_fr"])
                if "nutriscore_grade" in p_json["products"][prod]:
                    self.nutriscore = (
                        p_json["products"][prod]["nutriscore_grade"])
                self.url = p_json["products"][prod]["url"]
                self.image = (
                    p_json["products"][prod]["image_front_small_url"])
                self.energy_kj = (
                    p_json["products"][prod]["nutriments"]["energy_100g"])
                if "energy-kcal_100g" in p_json(
                        ["products"][prod]["nutriments"]):
                    self.energy_kcal = p_json(
                        ["products"][prod]["nutriments"]["energy-kcal_100g"])
                if "fat_100g" in p_json(
                        ["products"][prod]["nutriments"]):
                    self.fat = p_json(
                        ["products"][prod]["nutriments"]["fat_100g"])
                if "fiber_100g" in p_json["products"][prod]["nutriments"]:
                    self.fiber = p_json(
                        ["products"][prod]["nutriments"]["fiber_100g"])
                if "proteins_100g" in p_json["products"][prod]["nutriments"]:
                    self.proteins = p_json(
                        ["products"][prod]["nutriments"]["proteins_100g"])
                if "salt_100g" in p_json["products"][prod]["nutriments"]:
                    self.salt = p_json(
                        ["products"][prod]["nutriments"]["salt_100g"])
                extracted_product = Product(product_name=self.product_name,
                                            nutrition_grade=self.nutriscore,
                                            url=self.url,
                                            image_front_small_url=self.image,
                                            energy_kj=self.energy_kj,
                                            energy_kcal=self.energy_kcal,
                                            fat=self.fat,
                                            fiber=self.fiber,
                                            proteins=self.proteins,
                                            salt=self.salt)
                extracted_product.save()
                cat_saved_DB = Categories(
                    name=cat_name, product=extracted_product)
                cat_saved_DB.save()
        self.data_loaded = True


if __name__ == "__main__":
    data = OffApiData()
    data.get_info()

# def check_value(value):
#     if (value == "" OR value is None):
#         return False
#     return True

# save = True
# json = p_json["products"][prod]

# datas = {}

# TO_CHECK = {
#     "base" : {
#         "product_name": "product_name_fr",
#         "nutriscore": "nutriscore_grade",
#         "url": "url",
#         "image": "image_front_small_url"
#     },
#     "nutriments" : {
#         "energy_kj": "energy_100g",
#         "energy_kcal": "energy-kcal_100g",
#         "fat": "fat_100g",
#         "fiber": "fiber_100g",
#         "proteins": "proteins_100g",
#         "salt": "salt_100g"
#     }
# }

# while save:
#     for tata in ["base", "nutriments"]:
#         for key, value in TO_CHECK[tata].items():
#             if( datas["key"] and check_value(value) ):
#                 datas["key"] = value
#             else:
#                 save = False
#                 break
#     extracted_product = Product(**datas)
#     extracted_product.save()
#     save = False

    # to_be_extracted = {"product_name": "product_name_fr",
    #                    "nutriscore": "nutriscore_grade",
    #                    "url": "url",
    #                    "image": "image_front_small_url"}
    # nutriments = {"energy_kj": "energy_100g",
    #               "energy_kcal": "energy-kcal_100g",
    #               "fat": "fat_100g",
    #               "fiber": "fiber_100g",
    #               "proteins": "proteins_100g",
    #               "salt": "salt_100g"}
    # for key, value in to_be_extracted.items():
    #     if value in p_json["products"][prod]:
    #         self.key = p_json["products"][prod][value]
    #     else:
    #         self.key = "no_name_in_database"
    #     print("{} a pour valeur {}".format(key, self.key))
    # for key, value in nutriments.items():
    #     if value in p_json["products"][prod]["nutriments"]:
    #         self.key = p_json["products"][prod]["nutriments"][value]
    #     else:
    #         self.key = "0"
    #     print("{} a pour valeur {}".format(key, self.key))
