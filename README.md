# Creamy Korean

An API for an aggregator of Korean cosmetic products on the Russian market. The main feature is to allow users to choose products by needed or avoidable ingredients.

This is a training project, so none of the further URLs are actually available.

## Base URL

```
https://creamykorean.ru/v1/api/
```

## Products

```
GET /products
```

Return all products that have actual ingredients lists. If a product database entry contains all data except an ingredients list (composition), this entry won't be in a response.

```
{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "A'Pieu Deep Clean Makeup Retouching Pad",
            "brand": "A'pieu",
            "volume": "10 подушечек",
            "image": "https://sifo.ru/image/cache/catalog/products/a-pieu/salfetki-dlya-korrekcii-makiyazha-a-pieu-deep-clean-makeup-retouching-pad/salfetki-dlya-korrekcii-makiyazha-a-pieu-deep-clean-makeup-retouching-pad-700x700.jpg",
            "section": "Салфетки",
            "composition": "Purified Water, Glycerin, PEG-6 Caprylic, Propanediol, Butylene Glycol, Sodium Bicarbonate, Carbonated Water, Aloe Vera Leaf Extract, Salvia Leaf Extract, Mangosteen Peel Extract, Allantoin, Green Tea Extract, Ginger Extract, Spanish Licorice Root Extract, Coptis Root Extract, Ethylhexylglycerin, Disodium EDTA, Propylene Glycol, 1,2-Hexanediol, Phenoxyethanol, Fragrance",
            "prices": [
                {
                    "highest": 190,
                    "lowest": 190
                }
            ],
            "available_in_shops": [
                {
                    "shop": "Sifo",
                    "availability": true,
                    "current_price": 190,
                    "link_to_product_page": "https://sifo.ru/salfetki-dlya-korrekcii-makiyazha-pieu-deep-clean-makeup-retouching-pad",
                    "last_updated": "2020-10-05T21:28:15.987867+03:00"
                }
            ]
        },
        {
            "id": 9,
            "name": "Shingmulnara Tea Tree Trouble Care Body Wash",
            "brand": "Shingmulnara",
            "volume": "500 мл",
            "image": "https://sifo.ru/image/cache/catalog/products/shingmulnara/gel-dlya-dusha-shingmulnara-tea-tree-trouble-care-body-wash/gel-dlya-dusha-shingmulnara-tea-tree-trouble-care-body-wash-700x700.jpg",
            "section": "Гели для душа",
            "composition": "Water, Sodium Laureth Sulfate, Sodium Chloride, Cocamide DEA, Glycerin, Cocamidopropyl Betaine, Sodium Benzoate, Salicylic Acid, Disodium Cocoamphodiacetate, Fragrance, Betaine, Butylene Glycol, Citric Acid, Rosmarinus Officinalis (Rosemary) Leaf Oil, Polyquaternium-7, 1,2-Hexanediol, Melaleuca Alternifolia (Tea Tree) Leaf Oil, Melaleuca Alternifolia (Tea Tree) Leaf Extract, Hexylene Glycol",
            "prices": [
                {
                    "highest": 1580,
                    "lowest": 1580
                }
            ],
            "available_in_shops": [
                {
                    "shop": "Sifo",
                    "availability": true,
                    "current_price": 1580,
                    "link_to_product_page": "https://sifo.ru/gel-dlya-dusha-shingmulnara-tea-tree-trouble-care-body-wash",
                    "last_updated": "2020-10-06T18:56:59.130834+03:00"
                }
            ]
        },
        ...
    ]
}
```

```
GET /products/{id}
```

Return a single product entry. If an entry with such an ID is in the database but doesn't contain an ingredients list, the response will be 404 error.

```
{
    "id": 10,
    "name": "Nollam Lab Body Wash Wild",
    "brand": "Nollam Lab",
    "volume": "300 мл",
    "image": "https://sifo.ru/image/cache/catalog/products/nollam-lab/gel-dlya-dusha-nollam-lab-body-wash-wild/gel-dlya-dusha-nollam-lab-body-wash-wild-700x700.jpg",
    "section": "Гели для душа",
    "composition": "Sodium Laureth Sulfate, Water, Disodium Cocoamphodiacetate, Lauryl Glucoside, Glycerin, Sodium Myristoyl Sarcosinate, Cocamide Methyl MEA, Juniperus Communis Fruit Extract, Lilium Candidum Flower Water, Lactobacillus/Soybean Ferment Extract, Dioscorea Japonica Root Extract, Tremella Fuciformis (Mushroom) Extract, Glycol Distearate, Citric Acid, Sodium Benzoate, Guar Hydroxypropyltrimonium Chloride, Disodium EDTA, Fragrance",
    "prices": [
        {
            "highest": 530,
            "lowest": 530
        }
    ],
    "available_in_shops": [
        {
            "shop": "Sifo",
            "availability": true,
            "current_price": 530,
            "link_to_product_page": "https://sifo.ru/gel-dlya-dusha-nollam-lab-body-wash-wild",
            "last_updated": "2020-10-06T18:57:04.812366+03:00"
        }
    ]
}
```

### Fields

For all products, it is possible to request only needed fields.

```
GET /products/?fields=id,prices,available_in_shops
```

```
{
    "count": 3,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "prices": [
                {
                    "highest": 190,
                    "lowest": 190
                }
            ],
            "available_in_shops": [
                {
                    "shop": "Sifo",
                    "availability": true,
                    "current_price": 190,
                    "link_to_product_page": "https://sifo.ru/salfetki-dlya-korrekcii-makiyazha-pieu-deep-clean-makeup-retouching-pad",
                    "last_updated": "2020-10-05T21:28:15.987867+03:00"
                }
            ]
        },
        {
            "id": 9,
            "prices": [
                {
                    "highest": 1580,
                    "lowest": 1580
                }
            ],
            "available_in_shops": [
                {
                    "shop": "Sifo",
                    "availability": true,
                    "current_price": 1580,
                    "link_to_product_page": "https://sifo.ru/gel-dlya-dusha-shingmulnara-tea-tree-trouble-care-body-wash",
                    "last_updated": "2020-10-06T18:56:59.130834+03:00"
                }
            ]
        },
        ...
    ]
}
```

### Filtering

For products next filters are available:
* section — return products by a single section (including its subsections);
* exclude — return products that don't contain one or many certain ingredients in their ingredients lists;
* include_all — return products that include all queried ingredients;
* include_any — return products that include at least one of the queried ingredients.

Parameters for all filters must be integers:

```
GET /products/?include_all=1034,3193
```

## Sections

```
GET /sections
```

Return all sections (products categories).

```
{
    "count": 5,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Лицо",
            "products_number": 1,
            "subsections": [
                {
                    "id": 4,
                    "name": "Очищение",
                    "products_number": 1,
                    "subsections": [
                        {
                            "id": 13,
                            "name": "Гидрофильное масло",
                            "products_number": 0,
                            "subsections": []
                        },
                        {
                            "id": 14,
                            "name": "Пенки",
                            "products_number": 0,
                            "subsections": []
                        },
                        {
                            "id": 15,
                            "name": "Гели",
                            "products_number": 0,
                            "subsections": []
                        }
                        ...
                    ]
                }
                ...
            ]
            ...
        }
    ]
}
```

## Users

```
POST /users
```

Create a user.

Required fields:
* username;
* email;
* password.

All data must be validated before making a request (an email seems to be an email, a password was typed twice).

```
GET /users/{id}
```

Return user data.

```
{
    "id": 3,
    "username": "testuser1",
    "email": "znegrosilva87j@amazonshopbuy.com",
    "profile": {
        "favourite_products": [
            {
                "id": 102,
                "name": "Royal Skin Cactus Soothing Gel"
            },
            {
                "id": 167,
                "name": "Ciracle Pore Control Blackhead Off Sheet"
            }
        ],
        "exclude_ingrs": [
            {
                "id": 2664,
                "name": "Sodium Laureth Sulfate"
            },
            {
                "id": 2757,
                "name": "Sodium Lauryl Sulfate"
            }
        ],
        "include_ingrs": [
            {
                "id": 3003,
                "name": "Tocopherol"
            },
            {
                "id": 2213,
                "name": "Cetearyl Alcohol"
            },
            {
                "id": 2214,
                "name": "Cetyl Alcohol"
            }
        ],
        "exclude_ingrs_groups": null,
        "include_ingrs_groups": null
    }
}
```

```
PATCH /users/{id}
```

Change user data partially.

"username", "email" and "password" have to contain new validated data.

Fields in "profile" have to look such a way:

```
{
   "profile": {
      "exclude_ingrs": {
         "action": "add",
         "values": [
             9,
             41,
             63
         ]
      },
      "include_ingrs": {
          "action": "remove",
          "values": 2214
      }
   }
}
```
Available actions:
* "add";
* "remove".

Values must be IDs as either a list of integers or a single integer.

## Pagination

Pagination style implies using limit and offset parameters. Default limit is 20.

```
GET /products/?limit=40&offset=60
```
