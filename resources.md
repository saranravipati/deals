# APIs Used by Chef'd Website

This is a list of all the API calls our website utilizes along with a short description of each. If the argument listed is not part of the request, then it is part of the payload data.

**[Apps.chefd.com](#apps-chefd)**

* [Customers](#apps-customers)
* [Orders](#apps-orders)
* [Gift Cards](#apps-gift-cards)
* [Products](#apps-products)
* [Recipes](#apps-recipes)
* [CMS](#apps-cms)
* [Delivery Dates](#apps-delivery-dates)

**[Rec.chefd.com](#rec-chefd)**

* [Customers](#rec-customers)
* [Recipes](#rec-recipes)
* [Gift Cards](#rec-gift-cards)
* [Food Critic](#rec-critic)
* [API Tunneling](#rec-api-tunneling)

**[Social Annex (Annex Cloud)](#sa)**

* [Ratings & Reviews](#sa-ratings-reviews)
* [Share a Meal (Post-meal Experience Modal)](#sa-share-meal)
* [Loyalty Points](#sa-loyalty-points)
* [Question & Answer](#sa-question-answer)
* [Refer a Friend](#sa-refer-friend)

## <a id="apps-chefd"></a>Apps.chefd.com

All URLs referenced in this section of the documentation have the following base:

|            Staging             |       Production       |
| :----------------------------: | :--------------------: |
| https://apps-staging.chefd.com | https://apps.chefd.com |

### <a id="apps-customers"></a>**Customers**

* `POST /v1/customers/search`

  | Argument | Description              |   Type   | Required |
  | -------- | ------------------------ | :------: | :------: |
  | `email`  | Customer's email address | `string` |   [x]    |

  Used to search if a customer exists when purchasing a meal plan. This will force them to login so it could attach the meal plan to that customer.

* `GET /v1/customers/{customer_id}/unratedorders/`

  | Argument      | Description           |   Type   | Required |
  | ------------- | --------------------- | :------: | :------: |
  | `customer_id` | Shopify customer's ID | `number` |   [x]    |

  Used to get the unrated orders of a customer to determine whether they should be prompted to rate it.

* `POST /v1/customers/{customer_id}/favorites/`

  | Argument      | Description           |   Type   | Required |
  | ------------- | --------------------- | :------: | :------: |
  | `customer_id` | Shopify customer's ID | `number` |   [x]    |
  | `product_id`  | Shopify product ID    | `number` |   [x]    |

  Used to add a product to a customer's favorites list.

* `DELETE /v1/customers/{customer_id}/favorites/`

  | Argument      | Description           |   Type   | Required |
  | ------------- | --------------------- | :------: | :------: |
  | `customer_id` | Shopify customer's ID | `number` |   [x]    |
  | `product_id`  | Shopify product ID    | `number` |   [x]    |

  Used to remove a product from a customer's favorites list.

* `POST /v1/customers/{customer_id}/wishlist/`

  | Argument      | Description           |   Type   | Required |
  | ------------- | --------------------- | :------: | :------: |
  | `customer_id` | Shopify customer's ID | `number` |   [x]    |
  | `product_id`  | Shopify product ID    | `number` |   [x]    |

  Used to add a product to a customer's wishlist.

* `DELETE /v1/customers/{customer_id}/wishlist/`

  | Argument      | Description           |   Type   | Required |
  | ------------- | --------------------- | :------: | :------: |
  | `customer_id` | Shopify customer's ID | `number` |   [x]    |
  | `product_id`  | Shopify product ID    | `number` |   [x]    |

  Used to remove a product from a customer's wishlist.

* `POST /v1/customers/{customer_id}/likes/`

  | Argument      | Description           |   Type   | Required |
  | ------------- | --------------------- | :------: | :------: |
  | `customer_id` | Shopify customer's ID | `number` |   [x]    |
  | `product_id`  | Shopify product ID    | `number` |   [x]    |

  Used to add a product to a customer's "likes" which is consumed by the rec.chefd.com recommendation API.

* `DELETE /v1/customers/{customer_id}/likes/`

  | Argument      | Description           |   Type   | Required |
  | ------------- | --------------------- | :------: | :------: |
  | `customer_id` | Shopify customer's ID | `number` |   [x]    |
  | `product_id`  | Shopify product ID    | `number` |   [x]    |

  Used to remove a product from a customer's "likes" which is consumed by the rec.chefd.com recommendation API.

* `POST /v1/customers/{customer_id}/dislikes/`

  | Argument      | Description           |   Type   | Required |
  | ------------- | --------------------- | :------: | :------: |
  | `customer_id` | Shopify customer's ID | `number` |   [x]    |
  | `product_id`  | Shopify product ID    | `number` |   [x]    |

  Used to add a product to a customer's "dislikes" which is consumed by the rec.chefd.com recommendation API.

* `DELETE /v1/customers/{customer_id}/dislikes/`

  | Argument      | Description           |   Type   | Required |
  | ------------- | --------------------- | :------: | :------: |
  | `customer_id` | Shopify customer's ID | `number` |   [x]    |
  | `product_id`  | Shopify product ID    | `number` |   [x]    |

  Used to remove a product from a customer's "dislikes" which is consumed by the rec.chefd.com recommendation API.

* `PUT /v1/customers/{customer_id}`

  | Argument      | Description                               |   Type   | Required |
  | ------------- | ----------------------------------------- | :------: | :------: |
  | `customer_id` | Shopify customer's ID                     | `number` |   [x]    |
  | `value`       | Array of the customer's meal plan objects | `array`  |   [x]    |

  Used to update customer meal plan preferences.

  _Sample Request_

  ```javascript
  PUT https://apps-staging.chefd.com/v1/customers/127861751813

  {
    "value": [{
      "name": "ATKMP",
      "number_of_servings": "2",
      "meals_per_week": "6",
      "allergens": ["None"],
      "proteins": ["Poultry", "Fish", "Shellfish"],
      "stripe_customer_id": "cus_1111111AAAAAAA",
      "delivery_day_of_week": "5",
      "status": "Active",
      "gift_cards": [{
        "id": "39206022",
        "added_at": "2016-03-25T22:53:30+00:00",
        "date_added": "3\/25\/2016",
        "starting_balance": "15.00",
        "current_balance": "15.00",
        "last_characters": "a2f2"
      }]
    }]
  }
  ```

  _Sample Response_

  ```javascript
  {
    "status": 200,
    "data": {
      "id": 791804248069,
      "namespace": "profile",
      "key": "preferences",
      "value": "[{\"name\":\"ATKMP\",\"number_of_servings\":\"2\",\"meals_per_week\":\"6\",\"allergens\":[\"None\"],\"proteins\":[\"Poultry\",\"Fish\",\"Shellfish\"],\"stripe_customer_id\":\"cus_1111111AAAAAAA\",\"delivery_day_of_week\":\"5\",\"status\":\"Active\",\"gift_cards\":[{\"id\":\"39206022\",\"added_at\":\"2016-03-25T22:53:30+00:00\",\"date_added\":\"3\\/25\\/2016\",\"starting_balance\":\"15.00\",\"current_balance\":\"15.00\",\"last_characters\":\"a2f2\"}]}]",
      "value_type": "string",
      "description": null,
      "owner_id": 127861751813,
      "created_at": "2018-01-24T11:51:44-08:00",
      "updated_at": "2018-01-24T11:51:44-08:00",
      "owner_resource": "customer"
    }
  }
  ```

* `PUT /v1/customers/{customer_id}/balance`

  | Argument         | Description                                        |   Type   | Required |
  | ---------------- | -------------------------------------------------- | :------: | :------: |
  | `customer_id`    | Shopify customer's ID                              | `number` |   [x]    |
  | `gift_card_code` | Gift card code string that user inputs             | `string` |   [x]    |
  | `meal_plan_id`   | The SKU of the Meal Plan service Item, i.e. "WWMP" | `string` |   [x]    |

  Used to add a giftcard to a customer's meal plan account balance which is used in the billing of the recurring orders, prior to charging a customer's credit card (done via a NetSuite script).

* `GET /v1/customers/{customer_id}/balance_history?meal_plan_id={meal_plan_id}`

  | Argument       | Description                                        |   Type   | Required |
  | -------------- | -------------------------------------------------- | :------: | :------: |
  | `customer_id`  | Shopify customer's ID                              | `number` |   [x]    |
  | `meal_plan_id` | The SKU of the Meal Plan service Item, i.e. "WWMP" | `string` |   [x]    |

  Used to get a customer's account balance history of a specified meal plan.

### <a id="apps-orders"></a>**Orders**

* `PUT /v1/orders/{order_id}/rate/`

  | Argument   | Description      |   Type   | Required |
  | ---------- | ---------------- | :------: | :------: |
  | `order_id` | Shopify order ID | `number` |   [x]    |

  Used to confirm a meal has been rated a meal after it has been fulfilled and a certain time period has passed.

* `PUT /v1/orders/{order_id}/snoozeratereminder`

  | Argument   | Description      |   Type   | Required |
  | ---------- | ---------------- | :------: | :------: |
  | `order_id` | Shopify order ID | `number` |   [x]    |

  Used to snooze the post meal experience rating of a meal, possible snoozing of 2 times before it stops prompting user to rate the meal.

* `PUT /v1/orders/add_balance`

  | Argument   | Description      |   Type   | Required |
  | ---------- | ---------------- | :------: | :------: |
  | `order_id` | Shopify order ID | `number` |   [x]    |

  Used to add a gift card to a meal plan account balance if there is a remaining balance on the gift card after the purchase of a meal plan.

* `PUT /v1/orders/{order_id}/meals`

  | Argument   | Description                                                              |   Type   | Required |
  | ---------- | ------------------------------------------------------------------------ | :------: | :------: |
  | `order_id` | Shopify order ID                                                         | `number` |   [x]    |
  | `meals`    | Array of variants IDs of the meals you'd like to be on the swapped order | `array`  |   [x]    |

  Used to add a gift card to a meal plan account balance if there is a remaining balance on the gift card after the purchase of a meal plan. Sample meals data below:

  ```javascript
  {
    "meals": [{
      "variant_id": "8311103875",
      "quantity": "1"
    }, {
      "variant_id": "19328484230",
      "quantity": "1"
    }]
  }
  ```

* `PUT /v1/orders/{order_id}/skip`

  | Argument   | Description      |   Type   | Required |
  | ---------- | ---------------- | :------: | :------: |
  | `order_id` | Shopify order ID | `number` |   [x]    |

  Used to update an order with a "skipped", "skipped_status" note attribute that will be used during processing orders at cutoff (Wednesday at midnight every week).

* `PUT /v1/orders/{order_id}/unskip`

  | Argument   | Description      |   Type   | Required |
  | ---------- | ---------------- | :------: | :------: |
  | `order_id` | Shopify order ID | `number` |   [x]    |

  Used to update an order with an "unskipped", "skipped_status" note attribute that will be used during processing orders at cutoff (Wednesday at midnight every week).

### <a id="apps-gift-cards"></a>**Gift Cards**

* `POST /v1/giftcards`

  | Argument      | Description                                     |   Type   | Required |
  | ------------- | ----------------------------------------------- | :------: | :------: |
  | `card_number` | Gift card code/number that was inputted by user | `string` |   [x]    |

  Used to activate third party gift cards by first verifying it and then creating one in Shopify.

* `POST /v1/giftcards/balance`

  | Argument         | Description                                     |   Type   | Required |
  | ---------------- | ----------------------------------------------- | :------: | :------: |
  | `gift_card_code` | Gift card code/number that was inputted by user | `string` |   [x]    |

  Used to check the balance of Chef'd gift cards.

### <a id="apps-products"></a>**Products**

* `GET /v1/products/{product_id}`

  | Argument     | Description        |   Type   | Required |
  | ------------ | ------------------ | :------: | :------: |
  | `product_id` | Shopify product ID | `number` |   [x]    |

  Used to get product data for misc. thing, i.e. adding products to the cart.

### <a id="apps-recipes"></a>**Recipes**

* `POST /v1/recipes/recommended`

  Accepts new customer/sign up:

  | Argument               | Description                                                                                  |   Type   | Required |
  | ---------------------- | -------------------------------------------------------------------------------------------- | :------: | :------: |
  | `name`                 | The SKU of the Meal Plan service Item, i.e. "WWMP"                                           | `string` |   [x]    |
  | `number_of_servings`   | Number of servings, usually "2" or "4"                                                       | `number` |   [x]    |
  | `meals_per_week`       | Usually from "1" through "7", Spoon University allows a "0" if it is a Grab 'N' Go only plan | `number` |   [x]    |
  | `allergens`            | Array of allergens user has selected                                                         | `array`  |   [x]    |
  | `proteins`             | Array of proteins user has selected                                                          | `array`  |   [x]    |
  | `meal_plan_product_id` | The product ID of the Meal Plan service item                                                 | `number` |   [x]    |

  _Sample Data_

  ```javascript
  {
    "name": "ATKMP",
    "number_of_servings": 2,
    "meals_per_week": 4,
    "allergens": ["None"],
    "proteins": ["Beef", "Lamb", "Poultry", "Fish", "Pork", "Shellfish"],
    "meal_plan_product_id": 8708946060
  }
  ```

  This also accepts existing meal plan/customer:

  | Argument               | Description                                        |   Type   | Required |
  | ---------------------- | -------------------------------------------------- | :------: | :------: |
  | `email`                | Shopify product ID                                 | `string` |   [x]    |
  | `meal_plan_id`         | The SKU of the Meal Plan service Item, i.e. "WWMP" | `string` |   [x]    |
  | `meal_plan_product_id` | The product ID of the Meal Plan service item       | `number` |   [x]    |

  _Sample Data_

  ```javascript
  {
    "email": "kyle.valdillez@chefd.com",
    "meal_plan_id": "ATKMP",
    "meal_plan_product_id": 8708946060
  }
  ```

  Used for meal plan recommendations for sign up/recurring orders, etc.

### <a id="apps-cms"></a>**CMS**

* `GET /v1/cms/ios/views/all`

  Used to get collections, brands, partners, featured collections, etc. to populate website and iOS/Android apps. Controlled by Marketing via Shopify Metafields/CMS.

### <a id="apps-delivery-dates"></a>**Delivery Dates (Used via rec.chefd.com)**

* `GET /api/v1/{zip_code}/{address_type}`

  | Argument       | Description                                           |   Type   | Required |
  | -------------- | ----------------------------------------------------- | :------: | :------: |
  | `zip_code`     | User inputted ZIP code                                | `string` |   [x]    |
  | `address_type` | User selected option of "residential" or "commercial" | `string` |   [x]    |

  Used to get available delivery dates based on ZIP and whether is it "residential" or "commercial".

* `GET /api/v1/{zip_code}/{address_type}{start_date}/{end_date}`

  | Argument       | Description                                           |   Type   | Required |
  | -------------- | ----------------------------------------------------- | :------: | :------: |
  | `zip_code`     | User inputted ZIP code                                | `string` |   [x]    |
  | `address_type` | User selected option of "residential" or "commercial" | `string` |   [x]    |
  | `start_date`   | Pre-order start date                                  | `number` |   [x]    |
  | `end_date`     | Pre-order end date                                    | `number` |   [x]    |

  Used to get available delivery dates based on ZIP and whether is it "residential" or "commercial" AND passing in pre-order dates which are stored on the product in Shopify via a product tag (ex: shipdates:22/01/2018-26/01/2018). "Start_date" and "end_date" are formatted in the JavaScript getTime() value of the specified date (ex: 1516217674507).

* More information available about this endpoint under “Shipping API Endpoints” section here:
  https://bitbucket.org/chefdtech/apps.chefd.com/overview

## <a id="rec-chefd"></a>Rec.chefd.com

All URLs referenced in this section of the documentation have the following base:

|            Staging            |      Production       |
| :---------------------------: | :-------------------: |
| https://api-staging.chefd.com | https://rec.chefd.com |

### <a id="rec-customers"></a>**Customers**

* `POST /api/0.1/customers/send/sms/`

  | Argument      | Description                          |   Type   | Required |
  | ------------- | ------------------------------------ | :------: | :------: |
  | `phoneNumber` | User inputted phone number           | `string` |   [x]    |
  | `messageText` | Message you wish for user to receive | `string` |   [x]    |

  Used for sending a text to a phone that contains a link to the Chef’d app. On the homepage for non-logged in users.

* `GET /api/0.1/preference/{customer_id}/questions/`

  | Argument      | Description         |   Type   | Required |
  | ------------- | ------------------- | :------: | :------: |
  | `customer_id` | Shopify customer ID | `number` |   [x]    |

  Used to get preference questions for a specific customer when they log in. If there are any available questions, the customer will have the option to answer them for loyalty points.

* `GET /api/0.1/preference/questions/?onboard=true`

  Used to get preference questions for a first-time customer or not logged in customer. Similarly to the one above, they will receive points for answering the questions if they were to create an account.

* `POST /api/0.1/preference/{customer_id}/preferences/`

  | Argument      | Description                                                             |   Type   | Required |
  | ------------- | ----------------------------------------------------------------------- | :------: | :------: |
  | `customer_id` | Shopify customer ID                                                     | `number` |   [x]    |
  | `setId`       | The set of questions' ID as defined in the MongoDB                      | `number` |   [x]    |
  | `answers`     | Answers array of objects that contain the question ID and the answer ID | `array`  |   [x]    |

  Used to submit answers to the questions (if any) and update that customer's preferences in the MongoDB in mLab which is used to recommend better recipes in the "Just for You" section of the website.

  _Sample Request_

  ```javascript
  POST https://rec.chefd.com/api/0.1/preference/3021811270/preferences/

  {
    "setId": 1,
    "answers": [{
      "question_id": 1,
      "answers": [1]
    }, {
      "question_id": 2,
      "answers": [5]
    }, {
      "question_id": 3,
      "answers": [7]
    }, {
      "question_id": 4,
      "answers": [10]
    }]
  }
  ```

  _Sample Response_

  ```javascript
  {
    "detail": "Customer preferences saved successfully"
  }
  ```

* `POST /api/0.1/preference/preferences/`

  | Argument  | Description                                                             |   Type   | Required |
  | --------- | ----------------------------------------------------------------------- | :------: | :------: |
  | `setId`   | The set of questions' ID as defined in the MongoDB                      | `number` |   [x]    |
  | `answers` | Answers array of objects that contain the question ID and the answer ID | `array`  |   [x]    |

  Similar to the one above but for customers that don't have an account set up or aren't logged in.

* `POST /api/0.1/actions/`

  | Argument         | Description                                          |   Type   | Required |
  | ---------------- | ---------------------------------------------------- | :------: | :------: |
  | `customerId`     | Shopify customer ID                                  | `number` |   [x]    |
  | `actionTypeId`   | Type of action ID as defined by the MongoDB          | `number` |   [x]    |
  | `actionSourceId` | ID of the action source as definedy by the MongoDB   | `number` |   [x]    |
  | `actionData`     | Data representing the action taken, i.e. product IDs | `array`  |   [x]    |

  Used to send customer events MongoDB such as search, filter, product add to carts, etc. to help aid in the recommendations via the "recommendation engine".

  _Sample Request_

  ```javascript
  POST https://rec.chefd.com/api/0.1/actions/

  {
    "customerId": 601822979,
    "actionTypeId": 3,
    "actionSourceId": 1,
    "actionData": [458004911]
  }
  ```

  _Sample Response_

  ```javascript
  {
    "detail": "The customer action has been saved"
  }
  ```

* `POST /api/0.1/actions/justforyou/feedback/`

  | Argument     | Description                                                         |   Type    | Required |
  | ------------ | ------------------------------------------------------------------- | :-------: | :------: |
  | `customerId` | Shopify customer ID                                                 | `number`  |   [x]    |
  | `productId`  | Shopify product ID                                                  | `number`  |   [x]    |
  | `liked`      | Whether the user liked the suggestion in the "Just For You" section | `boolean` |   [x]    |

  **On the website but not in use/hidden.** Would be used to send feedback to the MongoDB whether or not the user had liked the recipes they were being suggested.

* `GET /api/0.1/customers/{customer_id}/justforyou/`

  | Argument     | Description         |   Type   | Required |
  | ------------ | ------------------- | :------: | :------: |
  | `customerId` | Shopify customer ID | `number` |   [x]    |

  Used to get recommendations for the "Just for You" section when the customer is logged in. This is NOT the recommendations that are used for the meal plan. These are only for the customer based on preference questions and other actions they have taken.

### <a id="rec-recipes"></a>**Recipes**

* `GET /api/0.1/recipes/{product_id}/similarity/`

  | Argument     | Description        |   Type   | Required |
  | ------------ | ------------------ | :------: | :------: |
  | `product_id` | Shopify product ID | `number` |   [x]    |

  Used to get recipes similar to the product you are passing in. Currently being used on the Product detail pages.

* `POST /api/0.1/recipes/discount/`

  | Argument         | Description         |  Type   | Required |
  | ---------------- | ------------------- | :-----: | :------: |
  | `productsInCart` | List of product IDs | `array` |   [x]    |

  Used to get discounts based on the products in the cart so that it could be displayed in the custom slide out cart on the website. This was primarily used for a promotion back last year. Technically still fires since those products are still available but hasn't been used in any other promotions since.

  _Sample Request_

  ```javascript
  POST https://www.rec.chefd.com/api/0.1/recipes/discount

  {
    "productsInCart": [10716376524, 10716139404, 8704574092]
  }
  ```

  _Sample Response_

  ```javascript
  {
    "discount": {
      "productsApplicable": [10716139404, 10716376524],
      "discountCode": "grilling5",
      "discountPercentage": 5
    }
  }
  ```

* `POST /api/0.1/recipes/delivery/dates/`

  | Argument      | Description                                                       |   Type   | Required |
  | ------------- | ----------------------------------------------------------------- | :------: | :------: |
  | `zipcode`     | User inputted ZIP code                                            | `string` |   [x]    |
  | `recipes`     | List of recipe objects containing Shopify product and variant IDs | `array`  |   [x]    |
  | `addressType` | User selected option of "residential" or "commercial"             | `string` |   [x]    |

  Used to get delivery dates for the ZIP and address type inputted. This acts as proxy for the "Delivery Dates" API in the apps.chefd.com section above.

  _Sample Request_

  ```javascript
  POST https://rec.chefd.com/api/0.1/recipes/delivery/dates/

  {
    "zipcode": "90245",
    "recipes": [{
      "recipeId": 458004911,
      "variantId": 1187574767
    }, {
      "recipeId": 8704574092,
      "variantId": 29951848524
    }],
    "addressType": "residential"
  }
  ```

  _Sample Response_

  ```javascript
  {
    "failsafe": false,
    "shipdates": [null, null],
    "url": "https://apps.chefd.com/api/v1/dates/90245/residential/?locations=[elsegundo]",
    "recipe_data": [{
      "shipdates": [null, null],
      "id": 8704574092,
      "location_inventory": [{
        "ondemand_available": true,
        "location": "elsegundo"
      }]
    }, {
      "shipdates": [null, null],
      "id": 458004911,
      "location_inventory": [{
        "ondemand_available": true,
        "location": "elsegundo"
      }]
    }],
    "is_meal_plan": false,
    "location_inventory": ["elsegundo"],
    "response": [{
      "date": "2018-01-26T09:00:00.000Z",
      "transitTime": 1,
      "remaining": 5000,
      "location": "elsegundo"
    }, {
      "date": "2018-01-27T09:00:00.000Z",
      "transitTime": 1,
      "remaining": 5000,
      "location": "elsegundo"
    }, {
      "date": "2018-01-30T09:00:00.000Z",
      "transitTime": 1,
      "remaining": 5000,
      "location": "elsegundo"
    }, {
      "date": "2018-01-31T09:00:00.000Z",
      "transitTime": 1,
      "remaining": 5000,
      "location": "elsegundo"
    }, {
      "date": "2018-02-01T09:00:00.000Z",
      "transitTime": 1,
      "remaining": 5000,
      "location": "elsegundo"
    }, {
      "date": "2018-02-02T09:00:00.000Z",
      "transitTime": 1,
      "remaining": 5000,
      "location": "elsegundo"
    }, {
      "date": "2018-02-03T09:00:00.000Z",
      "transitTime": 1,
      "remaining": 5000,
      "location": "elsegundo"
    }, {
      "date": "2018-02-06T09:00:00.000Z",
      "transitTime": 1,
      "remaining": 5000,
      "location": "elsegundo"
    }, {
      "date": "2018-02-07T09:00:00.000Z",
      "transitTime": 1,
      "remaining": 5000,
      "location": "elsegundo"
    }, {
      "date": "2018-02-08T09:00:00.000Z",
      "transitTime": 1,
      "remaining": 5000,
      "location": "elsegundo"
    }]
  }
  ```

### <a id="rec-gift-cards"></a>**Gift Cards**

* `POST /api/0.1/redeem-gift-card/`

  | Argument    | Description                     |   Type   | Required |
  | ----------- | ------------------------------- | :------: | :------: |
  | `cardValue` | Value that user wants to redeem | `number` |   [x]    |
  | `email`     | Customer email address          | `string` |   [x]    |

  Used to redeem loyalty points for a Chef'd e-gift card.

  _Sample Request_

  ```javascript
  POST https://api-staging.chefd.com/api/0.1/redeem-gift-card/

  {
    "cardValue":10,
    "email":"kyle.valdillez@chefd.com"
  }
  ```

### <a id="rec-food-critic"></a>**Food Critic**

* `POST /api/0.1/foodcritic/signup/`

  | Argument         | Description                                                             |   Type   | Required |
  | ---------------- | ----------------------------------------------------------------------- | :------: | :------: |
  | `first_name`     | User's first name                                                       | `string` |   [x]    |
  | `last_name`      | User's last name                                                        | `string` |   [x]    |
  | `email`          | User's email address                                                    | `string` |   [x]    |
  | `contact_number` | User's contact number                                                   | `string` |   [x]    |
  | `reason`         | Reason they want to be food critic                                      | `string` |   [x]    |
  | `social_media`   | List of social media links they want to use as proof of their followers | `array`  |   [x]    |

  Used to redeem loyalty points for a Chef'd e-gift card.

  _Sample Request_

  ```javascript
  POST https://api-staging.chefd.com/api/0.1/foodcritic/signup/

  {
    "first_name": "John",
    "last_name": "Smith",
    "email": "john.smith@chefd.com",
    "contact_number": "(818) 111-2222",
    "reason": "I want free food",
    "social_media": ["https://www.facebook.com/test", "https://www.instagram.com/test"]
  }
  ```

  _Sample Response_

  ```javascript
  {
    "detail": "Email has been sent"
  }
  ```

### <a id="rec-api-tunneling"></a>**API Tunneling**

* `POST /api/0.1/tunnel/auth/login/`

  | Argument     | Description         |   Type   | Required |
  | ------------ | ------------------- | :------: | :------: |
  | `customerId` | Shopify customer ID | `number` |   [x]    |

  Used to log into a Shopify customer via checkout. I believe this corresponds to this in the [repo](https://bitbucket.org/chefdtech/rec.chefd.com/src/9bb4bb37f835582bd93d8c1f4c53a98ee261303a/api_tunnel/api_views.py?at=master&fileviewer=file-view-default#api_views.py-214).

* `[ANY VALUE] /api/0.1/tunnel/auth/login/?endpoint={params_url}`

  | Argument     | Description     |   Type   | Required |
  | ------------ | --------------- | :------: | :------: |
  | `params_url` | Shopify API URL | `string` |   [x]    |

  Used to supplement updates via the Shopify API. Here is the corresponding code in the [repo](https://bitbucket.org/chefdtech/rec.chefd.com/src/9bb4bb37f835582bd93d8c1f4c53a98ee261303a/api_tunnel/api_views.py?at=master&fileviewer=file-view-default#api_views.py-350).

  For `POST` requests, here is a _Sample Header_

  ```javascript
  {
    "Content-Type": "application/json",
    "token": "5sr12wp28fOC97pLwsMmwvvJLm5Rulws",
    "customerid": 4811484101
  }
  ```

  See below for some `params_url` examples:

  * `POST /admin/customers/{customer_id}/addresses.json` -- [Shopify Address Documentation](https://help.shopify.com/api/reference/customeraddress)
  * `PUT /admin/customers/{customer_id}.json` -- [Shopify Customer Documentation](https://help.shopify.com/api/reference/customer)
  * `POST /admin/orders.json` -- [Shopify Order Documentation](https://help.shopify.com/api/reference/order)
  * `GET /admin/customers/{customer_id}/metafields.json` -- [Shopify Metafield Documentation](https://help.shopify.com/api/reference/metafield)
  * `PUT /admin/customers/{customer_id}/metafields/{metafield_id}.json` -- [Shopify Metafield Documentation](https://help.shopify.com/api/reference/metafield)
  * `PUT /admin/customers/{customer_id}/addresses/{address_id}.json` -- [Shopify Address Documentation](https://help.shopify.com/api/reference/customeraddress)
  * `GET /admin/orders.json?customer_id={customer_id}&status=any` -- [Shopify Order Documentation](https://help.shopify.com/api/reference/order)
  * `GET /admin/orders.json?ids={order_ids}` -- [Shopify Order Documentation](https://help.shopify.com/api/reference/order)
  * `PUT /admin/orders/{order_id}.json` -- [Shopify Order Documentation](https://help.shopify.com/api/reference/order)
  * `GET /admin/products.json?ids={product_ids}` -- [Shopify Product Documentation](https://help.shopify.com/api/reference/product)

* `POST /api/0.1/stripe/customer/sources/add/`

  | Argument        | Description                                      |   Type    | Required |
  | --------------- | ------------------------------------------------ | :-------: | :------: |
  | `customerId`    | Shopify customer ID                              | `number`  |   [x]    |
  | `stripeToken`   | Stripe generated token                           | `string`  |   [x]    |
  | `defaultSource` | Whether or not to set this source as the default | `boolean` |   [x]    |

  Used to add a new card to a customer via the Stripe API. Here is the corresponding code in the [repo](https://bitbucket.org/chefdtech/rec.chefd.com/src/9bb4bb37f835582bd93d8c1f4c53a98ee261303a/stripe_payment/api_views.py?at=master&fileviewer=file-view-default#api_views.py-163).

  _Sample Data_

  ```javascript
  {
    "customerId": 4811484101,
    "stripeToken": "tok_19xykpFwwFlRyjYNqzxsCKZB",
    "defaultSource": true
  }
  ```

* `POST /api/0.1/stripe/customer/sources/setdefault/`

  | Argument        | Description    |   Type   | Required |
  | --------------- | -------------- | :------: | :------: |
  | `defaultSource` | Stripe card ID | `string` |   [x]    |

  Used to set a card as the default source of a customer via the Stripe API. Here is the corresponding code in the [repo](https://bitbucket.org/chefdtech/rec.chefd.com/src/9bb4bb37f835582bd93d8c1f4c53a98ee261303a/stripe_payment/api_views.py?at=master&fileviewer=file-view-default#api_views.py-266).

  _Sample Header_

  ```javascript
  {
    "Content-Type": "application/json",
    "token": "5sr12wp28fOC97pLwsMmwvvJLm5Rulws",
    "customerid": 4811484101
  }
  ```

  _Sample Data_

  ```javascript
  {
    "defaultSource": "card_19zmj6FwwFlRyjYNL8GCzWLD"
  }
  ```

* `DELETE /api/0.1/stripe/customer/sources/all/`

  | Argument       | Description    |   Type   | Required |
  | -------------- | -------------- | :------: | :------: |
  | `removeSource` | Stripe card ID | `string` |   [x]    |

  Used to remove a card source from a customer via the Stripe API. Here is the corresponding code in the [repo](https://bitbucket.org/chefdtech/rec.chefd.com/src/9bb4bb37f835582bd93d8c1f4c53a98ee261303a/stripe_payment/api_views.py?at=master&fileviewer=file-view-default#api_views.py-92).

  _Sample Header_

  ```javascript
  {
    "Content-Type": "application/json",
    "token": "5sr12wp28fOC97pLwsMmwvvJLm5Rulws",
    "customerid": 4811484101
  }
  ```

  _Sample Data_

  ```javascript
  {
    "removeSource": "card_19zmj6FwwFlRyjYNL8GCzWLD"
  }
  ```

* `GET /api/0.1/stripe/customer/sources/all/`

  Used to get the card sources from a customer via the Stripe API. Here is the corresponding code in the [repo](https://bitbucket.org/chefdtech/rec.chefd.com/src/9bb4bb37f835582bd93d8c1f4c53a98ee261303a/stripe_payment/api_views.py?at=master&fileviewer=file-view-default#api_views.py-52).

  _Sample Header_

  ```javascript
  {
    "Content-Type": "application/json",
    "token": "5sr12wp28fOC97pLwsMmwvvJLm5Rulws",
    "customerid": 4811484101
  }
  ```

* `GET /api/0.1/tunnel/open/?endpoint=/admin/products.json?ids={product_id,product_id}`

  | Argument     | Description        |   Type   | Required |
  | ------------ | ------------------ | :------: | :------: |
  | `product_id` | Shopify product ID | `number` |   [x]    |

  Used to get data via opening a connection for non-threatening Shopify APIs. Here is the corresponding code in the [repo](https://bitbucket.org/chefdtech/rec.chefd.com/src/9bb4bb37f835582bd93d8c1f4c53a98ee261303a/api_tunnel/api_views.py?at=master&fileviewer=file-view-default#api_views.py-515).

* `POST /api/0.1/social-annex/`

  | Argument     | Description                                                   |   Type   | Required |
  | ------------ | ------------------------------------------------------------- | :------: | :------: |
  | `page`       | Which page of the reviews one would like to access            | `number` |   [x]    |
  | `limit`      | How many reviews per page                                     | `number` |   [x]    |
  | `sortOption` | Option by which one would like to get the reviews             | `string` |   [x]    |
  | `data`       | Parameters to specify which product and status of the reviews | `object` |   [x]    |

  Used to get reviews from the Social Annex API.

  _Sample Request_

  ```javascript
  {
    "page": 1,
    "limit": 5,
    "sortOption": "newest",
    "data": {
      "ProductID": ["458004911"],
      "status": "Approved"
    }
  }
  ```

  _Sample Response_

  ```javascript
  {
    "errorcode": "0",
    "data": {
      "product": [{
        "pages": {
          "totalpages": 10,
          "currentpage": "1"
        },
        "product": "458004911",
        "review": [{
          "status": "Approved",
          "lastname:": "P",
          "whoareyoucookingformostnights": "Me plus one",
          "usertype": "Internal",
          "submissiondate": "2018-01-24 08:42:43",
          "reviewid": "15168265633554",
          "helpfulcount": {
            "nocount": 0,
            "yescount": 0
          },
          "publishdate": "2018-01-24 15:53:18",
          "overallrating:": "4",
          "adminreply": "",
          "whattypeofcookdoyouconsideryourself": "Intermediate",
          "location": "CT",
          "reviewmessage:": "I was skeptical of using \"cooking wine\" but the sauce came out great - this was really delicious. Great quality meat, very tender even though it was a shorter cook time that I expected. Would definitely repeat. ",
          "uploadimages:": [],
          "title:": "Very good",
          "firstname:": "Tara",
          "wouldyourecommendthisproduct?:": "Yes",
          "emailaddress:": null
        }, {
          "status": "Approved",
          "lastname:": "M",
          "whoareyoucookingformostnights": "",
          "usertype": "Internal",
          "submissiondate": "2018-01-22 12:36:18",
          "reviewid": "15165813766577",
          "helpfulcount": {
            "nocount": 0,
            "yescount": 0
          },
          "publishdate": "2018-01-22 18:02:58",
          "overallrating:": "5",
          "adminreply": "",
          "whattypeofcookdoyouconsideryourself": "",
          "location": "",
          "reviewmessage:": "This was an easy to make\nMeal...plenty of food for the two\nOf us. I would definitly buy this one again. ",
          "uploadimages:": [],
          "title:": "",
          "firstname:": "Christine",
          "wouldyourecommendthisproduct?:": "",
          "emailaddress:": null
        }, {
          "status": "Approved",
          "lastname:": "J",
          "whoareyoucookingformostnights": "",
          "usertype": "Internal",
          "submissiondate": "2018-01-18 04:42:37",
          "reviewid": "15162505572722",
          "helpfulcount": {
            "nocount": 0,
            "yescount": 0
          },
          "publishdate": "2018-01-22 18:11:54",
          "overallrating:": "5",
          "adminreply": "",
          "whattypeofcookdoyouconsideryourself": "",
          "location": "",
          "reviewmessage:": "Nice hearty meal, Very good flavor.",
          "uploadimages:": [],
          "title:": "",
          "firstname:": "M",
          "wouldyourecommendthisproduct?:": "",
          "emailaddress:": null
        }, {
          "status": "Approved",
          "lastname:": "J",
          "whoareyoucookingformostnights": "Me plus one",
          "usertype": "Internal",
          "submissiondate": "2018-01-17 05:10:40",
          "reviewid": "15161658402099",
          "helpfulcount": {
            "nocount": 0,
            "yescount": 0
          },
          "publishdate": "2018-01-17 12:30:54",
          "overallrating:": "4",
          "adminreply": "",
          "whattypeofcookdoyouconsideryourself": "Beginner",
          "location": "",
          "reviewmessage:": "First Chef'd meal - It was impressive how amazing this tasted!  Definitely on the tougher side to make.   Really enjoyed there were mashed potatoes and green beans.  Made for an impressive plate presentation.  Will try something a little easier next time. A lot of the prep time on this one is cutting veggies.  Recommend cutting the veggies earlier in the day so it's not so much at dinner time.",
          "uploadimages:": [],
          "title:": "Great meal for family dinner ",
          "firstname:": "Janelle",
          "wouldyourecommendthisproduct?:": "Yes",
          "emailaddress:": null
        }, {
          "status": "Approved",
          "lastname:": "L",
          "whoareyoucookingformostnights": "Me plus one",
          "usertype": "Internal",
          "submissiondate": "2018-01-15 12:55:38",
          "reviewid": "15159777380184",
          "helpfulcount": {
            "nocount": 0,
            "yescount": 0
          },
          "publishdate": "2018-01-17 13:02:36",
          "overallrating:": "4",
          "adminreply": "",
          "whattypeofcookdoyouconsideryourself": "",
          "location": "",
          "reviewmessage:": "The beef was tender and the flavor was good. The green beans were bland.",
          "uploadimages:": [],
          "title:": "Nice Meal",
          "firstname:": "T",
          "wouldyourecommendthisproduct?:": "Yes",
          "emailaddress:": null
        }],
        "totalreview": 100
      }]
    }
  }
  ```

## <a id="sa"></a>Social Annex (Annex Cloud)

### <a id="sa-ratings-reviews"></a>**Ratings & Reviews**

All URLs referenced in this section of the documentation have the following base:

|    Staging & Production     | Staging Site ID | Production Site ID |
| :-------------------------: | :-------------: | :----------------: |
| https://s28.socialannex.com |     9775370     |      9775371       |

* `PUT /api/reviewhelpful`

  | Argument       | Description                                       |   Type   | Required |
  | -------------- | ------------------------------------------------- | :------: | :------: |
  | `productId`    | Shopify product ID                                | `string` |   [x]    |
  | `reviewId`     | Annex Cloud review ID                             | `string` |   [x]    |
  | `siteId`       | Annex Cloud site ID                               | `string` |   [x]    |
  | `helpfulValue` | Either a "0" for not helpful or a "1" for helpful | `string` |   [x]    |

  Used to mark a review on a product helpful or not.

  _Sample Request_

  ```javascript
  PUT https://s28.socialannex.com/api/reviewhelpful

  {
    productId: "458004911",
    reviewId: "1515500462993",
    siteId: "9775371",
    helpfulValue: "1"
  }
  ```

  _Sample Response_

  ```javascript
  {
    "Status": "200",
    "Message": "Thanks for your vote."
  }
  ```

* `POST /api/avgreview/{site_id}?format=json`

  | Argument     | Description                       |   Type   | Required |
  | ------------ | --------------------------------- | :------: | :------: |
  | `site_id`    | Annex Cloud site ID               | `string` |   [x]    |
  | `id`         | Key of the Form Data being POSTed | `string` |   [x]    |
  | `product_id` | Shopify product ID                | `string` |   [x]    |

  Used to get the average rating of a product based on its reviews.

  _Sample Request_

  ```javascript
  POST https://s28.socialannex.com/api/avgreview/9775371?format=json

  FORM DATA:
  Key = 'id'
  Value = '{"ProductID":["458004911"]}'
  ```

  _Sample Response_

  ```javascript
  {
    "errorcode": "0",
    "data": [{
      "productid": "458004911",
      "avgrating": {
        "totalreview": 100,
        "avgrage": 5
      }
    }]
  }
  ```

* `POST /api/reviewstatistics/{site_id}/{template_id}?format=json`

  | Argument      | Description                                 |   Type   | Required |
  | ------------- | ------------------------------------------- | :------: | :------: |
  | `site_id`     | Annex Cloud site ID                         | `string` |   [x]    |
  | `template_id` | Annex Cloud defined template ID for display | `string` |   [x]    |
  | `id`          | Key of the Form Data being POSTed           | `string` |   [x]    |
  | `product_id`  | Shopify product ID                          | `string` |   [x]    |

  Used to get the number of "X" star reviews a product has.

  _Sample Request_

  ```javascript
  POST https://s28.socialannex.com/api/reviewstatistics/9775371/157?format=json

  FORM DATA:
  Key = 'id'
  Value = '{"ProductID":["458004911"]}'
  ```

  _Sample Response_

  ```javascript
  {
    "errorcode": "0",
    "product": [{
      "ProductID1": {
        "458004911": {
          "reviewstatics": {
            "5.0": "84",
            "4.0": "15",
            "3.0": "0",
            "2.0": "1",
            "1.0": "0"
          }
        }
      }
    }]
  }
  ```

* `POST /api/generatewritereviewform`

  | Argument     | Description                                 |   Type   | Required |
  | ------------ | ------------------------------------------- | :------: | :------: |
  | `siteId`     | Annex Cloud site ID                         | `string` |   [x]    |
  | `templateId` | Annex Cloud defined template ID for display | `string` |   [x]    |
  | `product_id` | Shopify product ID                          | `string` |   [x]    |

  Used to generate the write a review content.

  _Sample Request_

  ```javascript
  POST https://s28.socialannex.com/api/generatewritereviewform

  FORM DATA:
  Key = 'siteId'
  Value = '9775371'

  Key = 'templateId'
  Value = '157'

  Key = 'product_id'
  Value = '458004911'
  ```

  _Sample Response_

  ```javascript
  {
    "status": "success",
    "data": [{
      "type": "TextBox",
      "fieldid": "1593",
      "lablel": "Review Message:",
      "placeholder": "",
      "sequence": "0",
      "reviewcoloumn": "comment",
      "hashtag": "#comments#",
      "fieldtoptext": "",
      "fieldbottomtext": "",
      "validations": {
        "mandatory": "1",
        "email": "No",
        "activateminlength": "0",
        "minimumlength": "0",
        "activatemaxlenth": "0",
        "maximumlength": "0",
        "blankerrormessage": "Please enter your review.",
        "regularexpression": "",
        "errormessage": "Please enter valid character",
        "minimumlines": "3"
      }
    }, {
      "type": "TextBox",
      "fieldid": "1594",
      "lablel": "Location",
      "placeholder": "",
      "sequence": "0",
      "reviewcoloumn": "location",
      "hashtag": "#location#",
      "fieldtoptext": "",
      "fieldbottomtext": "",
      "validations": {
        "mandatory": "0",
        "email": "No",
        "activateminlength": "0",
        "minimumlength": "0",
        "activatemaxlenth": "0",
        "maximumlength": "0",
        "blankerrormessage": "0",
        "regularexpression": "0",
        "errormessage": "0",
        "minimumlines": "1"
      }
    }, {
      "type": "Uplode",
      "fieldid": "1595",
      "sequence": "0",
      "images": {
        "uplode_limit": "1",
        "advice_message": ""
      },
      "videos": {},
      "placeholder": "",
      "reviewcoloumn": "upload_image",
      "hashtag": "#image#",
      "validations": {
        "mandatory": "0",
        "email": "No",
        "blankerrormessage": "0"
      }
    }, {
      "type": "overallrating",
      "fieldid": "1596",
      "sequence": "0",
      "totalrating": "5",
      "rating_steps": "0",
      "shape": "0",
      "placeholder": "",
      "reviewcoloumn": "overall_rating",
      "hashtag": "#rating#",
      "fieldtoptext": "",
      "fieldbottomtext": "",
      "validations": {
        "mandatory": "1",
        "blankerrormessage": "Please rate this product.",
        "regularexpression": "0",
        "errormessage": "0"
      },
      "ratingmessage": ["Poor", "Fair", "Average", "Good", "Excellent"]
    }, {
      "type": "TextBox",
      "fieldid": "1597",
      "lablel": "Title:",
      "placeholder": "",
      "sequence": "0",
      "reviewcoloumn": "comment_title",
      "hashtag": "#title#",
      "fieldtoptext": "",
      "fieldbottomtext": "",
      "validations": {
        "mandatory": "1",
        "email": "No",
        "activateminlength": "0",
        "minimumlength": "0",
        "activatemaxlenth": "0",
        "maximumlength": "0",
        "blankerrormessage": "Please enter review title.",
        "regularexpression": "",
        "errormessage": "",
        "minimumlines": "1"
      }
    }, {
      "type": "TextBox",
      "fieldid": "1598",
      "lablel": "First Name:",
      "placeholder": "",
      "sequence": "0",
      "reviewcoloumn": "first_name",
      "hashtag": "#firstname#",
      "fieldtoptext": "",
      "fieldbottomtext": "",
      "validations": {
        "mandatory": "1",
        "email": "No",
        "activateminlength": "0",
        "minimumlength": "0",
        "activatemaxlenth": "0",
        "maximumlength": "0",
        "blankerrormessage": "Please enter first name.",
        "regularexpression": "^\\d*[a-zA-Z][a-zA-Z\\d]*$",
        "errormessage": "Please enter alphanumeric characters.",
        "minimumlines": "1"
      }
    }, {
      "type": "TextBox",
      "fieldid": "1599",
      "lablel": "Last Name:",
      "placeholder": "",
      "sequence": "0",
      "reviewcoloumn": "last_name",
      "hashtag": "#lastname#",
      "fieldtoptext": "",
      "fieldbottomtext": "",
      "validations": {
        "mandatory": "1",
        "email": "No",
        "activateminlength": "0",
        "minimumlength": "0",
        "activatemaxlenth": "0",
        "maximumlength": "0",
        "blankerrormessage": "Please enter last name.",
        "regularexpression": "^\\d*[a-zA-Z][a-zA-Z\\d]*$",
        "errormessage": "Please enter alphanumeric characters.",
        "minimumlines": "1"
      }
    }, {
      "type": "TextBox",
      "fieldid": "1600",
      "lablel": "Email address:",
      "placeholder": "",
      "sequence": "0",
      "reviewcoloumn": "email",
      "hashtag": "#email#",
      "fieldtoptext": "",
      "fieldbottomtext": "",
      "validations": {
        "mandatory": "1",
        "email": "Yes",
        "activateminlength": "0",
        "minimumlength": "0",
        "activatemaxlenth": "0",
        "maximumlength": "0",
        "blankerrormessage": "Please enter email address.",
        "regularexpression": "^([a-zA-Z0-9_\\.\\-])+\\@(([a-zA-Z0-9\\-])+\\.)+([a-zA-Z0-9]{2,4})+$",
        "errormessage": "Please enter the valid email address.",
        "minimumlines": "1"
      }
    }, {
      "type": "DropDown",
      "fieldid": "1601",
      "sequence": "0",
      "placeholder": "",
      "reviewcoloumn": "extra_selectbox1",
      "hashtag": "#mostnightt#",
      "fieldtoptext": "",
      "fieldbottomtext": "",
      "selected": "1",
      "defaulttext": "Select",
      "add_values": "No",
      "value": [{
        "optionid": "20975",
        "optionvalue": "Myself",
        "optionname": "Myself"
      }, {
        "optionid": "20976",
        "optionvalue": "Me plus one",
        "optionname": "Me plus one"
      }, {
        "optionid": "20977",
        "optionvalue": "My friends",
        "optionname": "My friends"
      }, {
        "optionid": "20978",
        "optionvalue": "My family",
        "optionname": "My family"
      }, {
        "optionid": "20979",
        "optionvalue": "Anyone who\\'s hungry!",
        "optionname": "Anyone who\\'s hungry!"
      }],
      "validations": {
        "mandatory": "0",
        "blankerrormessage": "Please select cooking for most nights.",
        "regularexpression": "0",
        "errormessage": "0"
      }
    }, {
      "type": "DropDown",
      "fieldid": "1602",
      "sequence": "0",
      "placeholder": "",
      "reviewcoloumn": "extra_selectbox2",
      "hashtag": "#yourself#",
      "fieldtoptext": "",
      "fieldbottomtext": "",
      "selected": "1",
      "defaulttext": "Select",
      "add_values": "No",
      "value": [{
        "optionid": "20980",
        "optionvalue": "Beginner",
        "optionname": "Beginner"
      }, {
        "optionid": "20981",
        "optionvalue": "Intermediate",
        "optionname": "Intermediate"
      }, {
        "optionid": "20982",
        "optionvalue": "Expert",
        "optionname": "Expert"
      }],
      "validations": {
        "mandatory": "0",
        "blankerrormessage": "Please select type of cook do you consider yourself.",
        "regularexpression": "0",
        "errormessage": "0"
      }
    }, {
      "type": "RadioButtons",
      "fieldid": "1603",
      "sequence": "0",
      "placeholder": "",
      "reviewcoloumn": "product_recormmend",
      "hashtag": "#recommend#",
      "fieldtoptext": "",
      "fieldbottomtext": "",
      "selected": "0",
      "add_values": "No",
      "value": [{
        "optionid": "20983",
        "optionvalue": "Yes, I recommend this meal.",
        "optionname": "Yes"
      }, {
        "optionid": "20984",
        "optionvalue": "Yes, I recommend this meal.",
        "optionname": "No"
      }],
      "validations": {
        "mandatory": "0",
        "blankerrormessage": "0",
        "regularexpression": "0",
        "errormessage": "0"
      }
    }]
  }
  ```

* `PUT /api/storewriteareviewformdata`

  | Argument         | Description                                                                       |   Type   | Required |
  | ---------------- | --------------------------------------------------------------------------------- | :------: | :------: |
  | `siteId`         | Annex Cloud site ID                                                               | `string` |   [x]    |
  | `templateId`     | Annex Cloud defined template ID for display                                       | `string` |   [x]    |
  | `formData`       | User inputted review data                                                         | `string` |   [x]    |
  | `productDetails` | Product details grabbed from the page                                             | `string` |   [x]    |
  | `reviewType`     | Annex Cloud generated review ID, depends where the review is being submitted from | `string` |   [x]    |

  Used to generate the write a review content.

  _Sample Request_

  ```javascript
  PUT https://s28.socialannex.com/api/generatewritereviewform

  {
    "siteId": "9775371",
    "templateId": "157",
    "formData": "[{\"key\":\"1593\",\"keyData\":\"DO NOT PUBLISH THIS, IT IS A TEST REVIEW.\"},{\"key\":\"1596\",\"keyData\":\"5\"},{\"key\":\"1597\",\"keyData\":\"TEST REVIEW\"},{\"key\":\"1598\",\"keyData\":\"Kyle\"},{\"key\":\"1599\",\"keyData\":\"Valdillez\"},{\"key\":\"1600\",\"keyData\":\"kyle.valdillez@chefd.com\"},{\"key\":\"1601\",\"keyData\":\"20976\"},{\"key\":\"1602\",\"keyData\":\"20980\"},{\"key\":\"1603\",\"keyData\":\"20983\"}]",
    "productDetails": "{\"product_id\":\"458004911\",\"product_name\":\"Beef Bourguignon\",\"product_image\":\"//cdn.shopify.com/s/files/1/0658/0121/t/10/assets/placeholder.jpeg?1153665772700376160\",\"product_url\":\"https://www.chefd.com/products/beef-bourguignon\"}",
    "reviewType": "0"
  }
  ```

  _Sample Response_

  ```javascript
  {
    "productinfo": {
      "productname": "Beef Bourguignon",
      "productimageurl": "\/\/cdn.shopify.com\/s\/files\/1\/0658\/0121\/t\/10\/assets\/placeholder.jpeg?1153665772700376160",
      "producturl": "https:\/\/www.chefd.com\/products\/beef-bourguignon"
    },
    "thankyoumessage": "<div class=\"sa_container\">\r\n<div class=\"sa-r-and-r-outer\">\r\n<div class=\"clearfix\">&nbsp;<\/div>\r\n&nbsp;\r\n\r\n<div class=\"clearfix\">&nbsp;<\/div>\r\n\r\n<div class=\"col-md-12 thank-you-margin\">\r\n<div align=\"center\" class=\"col-md-4 sa-tickmark\"><img alt=\"\" class=\"img-responsive\" src=\"\/\/cdn.socialannex.com\/custom_images\/9775371\/S13MUU_right.png\" \/><\/div>\r\n\r\n<div class=\"col-md-6 sa-thank-you\">Thank You<br \/>\r\n<span>Thank you for your review. Please allow up to 48 hours for us to publish your review.<br \/>\r\nYou will be notified once this has been posted!<\/span><\/div>\r\n<\/div>\r\n\r\n<div class=\"clearfix\">&nbsp;<\/div>\r\n&nbsp;\r\n\r\n<div class=\"clearfix\">&nbsp;<\/div>\r\n<!-- form finish here--><\/div>\r\n<\/div>",
    "username": "",
    "reviewid": "15169206906116",
    "trackId": 6973
  }
  ```

### <a id="sa-share-meal"></a>**Sharing a Meal (Post-meal Experience Modal)**

All URLs referenced in this section of the documentation have the following base:

|     Staging & Production      | Staging Site ID | Production Site ID |
| :---------------------------: | :-------------: | :----------------: |
| https://track.socialannex.net |     9775370     |      9775371       |

* `POST /api/SetConnectUserdetails/{site_id}?access_token={access_token}`

  | Argument       | Description                           |   Type   | Required |
  | -------------- | ------------------------------------- | :------: | :------: |
  | `site_id`      | Annex Cloud site ID                   | `string` |   [x]    |
  | `access_token` | Annex Cloud access token              | `string` |   [x]    |
  | `service`      | The service ID it needs to connect to | `string` |   [x]    |
  | `user_name`    | User's name                           | `string` |   [x]    |
  | `user_email`   | User's email address                  | `string` |   [x]    |

  Used to connect Facebook and Twitter when sharing a meal via post-meal experience. Service 1 is Facebook and 2 is Twitter.

  _Sample Request_

  ```javascript
  POST https://s28.socialannex.com/api/SetConnectUserdetails/9775371?access_token=4c1b19e6fa91623bf185fa7746870271

  FORM DATA:
  Key = 'service'
  Value = '2'

  Key = 'user_name'
  Value = 'Kyle Valdillez'

  Key = 'user_email'
  Value = 'kyle.valdillez@chefd.com'  
  ```

  _Sample Response_

  ```javascript
  {
    "Status": "success",
    "data": {
      "popup_header_background_color": "",
      "popup_body_background_color": "",
      "logo_image_url": "",
      "heading_text": "",
      "heading_text_color": "",
      "thanks_sorry_flag": "0",
      "thank_you_message_heading_text": "",
      "thank_you_message_heading_text_color": "",
      "thank_you_message_description_text": "",
      "thank_you_message_description_text_color": "",
      "sorry_message_heading_text": "",
      "sorry_message_heading_text_color": "",
      "sorry_message_description_text": "",
      "sorry_message_description_text_color": "",
      "thankyou_image_url": "",
      "sorry_image_url": ""
    }
  }
  ```

* `POST/api/SetShareUserdetails/{site_id}?access_token={access_token}`

  | Argument              | Description                         |   Type   | Required |
  | --------------------- | ----------------------------------- | :------: | :------: |
  | `site_id`             | Annex Cloud site ID                 | `string` |   [x]    |
  | `access_token`        | Annex Cloud access token            | `string` |   [x]    |
  | `service`             | The service ID it needs to share to | `string` |   [x]    |
  | `share_page_flag`     | Annex Cloud defined ID              | `string` |   [x]    |
  | `user_name`           | User's name                         | `string` |   [x]    |
  | `user_email`          | User's email address                | `string` |   [x]    |
  | `product_id`          | Shopify product ID                  | `string` |   [x]    |
  | `product_name`        | Shopify product name                | `string` |   [x]    |
  | `product_description` | Shopify product description         | `string` |   [x]    |
  | `product_image`       | Shopify product image URL           | `string` |   [x]    |
  | `product_url`         | Shopify product URL                 | `string` |   [x]    |
  | `product_price`       | Shopify product price               | `string` |   [x]    |
  | `caption`             | Caption of post via social media    | `string` |   [x]    |

  Used to create bitly links for the customer to share via Facebook and Twitter.

  _Sample Request_

  ```javascript
  POST https://s28.socialannex.com/api/SetConnectUserdetails/9775371?access_token=4c1b19e6fa91623bf185fa7746870271

  FORM DATA:
  Key = 'service'
  Value = '8'

  Key = 'share_page_flag'
  Value = '2'

  Key = 'user_name'
  Value = 'Kyle Valdillez'

  Key = 'user_email'
  Value = 'kyle.valdillez@chefd.com'

  Key = 'product_id'
  Value = '10818328012'

  Key = 'product_name'
  Value = 'Steak Sandwiches'

  Key = 'product_description'
  Value = 'Best steak sandwiches meal you can get.'

  Key = 'product_image'
  Value = 'https://cdn.shopify.com/s/files/1/0658/0121/products/MUN.BEEF1.2_20Hero_52530a5b-d9c5-4205-8264-e962f57620a5.jpg?v=1507868990'

  Key = 'product_url'
  Value = '/products/steak-sandwiches-with-kale-chimichurri-and-heirloom-tomato-salad'

  Key = 'product_price'
  Value = '$30.00'

  Key = 'caption'
  Value = 'https://www.chefd.com/'
  ```

  _Sample Response_

  ```javascript
  {
    "Status": "success",
    "data": {
      "bitly_url": "https:\/\/chefd.app.link\/6ZAB6Iot0J"
    }
  }
  ```

### <a id="sa-loyalty-points"></a>**Loyalty Points**

All URLs referenced in this section of the documentation have the following base:

|    Staging & Production     | Staging Site ID | Production Site ID |
| :-------------------------: | :-------------: | :----------------: |
| https://s15.socialannex.net |     9775370     |      9775371       |

* `POST /apiv2/userpoints/{site_id}/{customer_email}?access_token={access_token}`

  | Argument         | Description                       |   Type   | Required |
  | ---------------- | --------------------------------- | :------: | :------: |
  | `site_id`        | Annex Cloud site ID               | `string` |   [x]    |
  | `customer_email` | Shopify customer email            | `string` |   [x]    |
  | `access_token`   | Annex Cloud access token          | `string` |   [x]    |
  | `action_id`      | Annex Cloud defined action ID     | `string` |   [x]    |
  | `action_use`     | Annex Cloud defined action use ID | `string` |   [x]    |

  Used to allocate points for subscribing to the newsletter.

  _Sample Request_

  ```javascript
  POST https://s15.socialannex.net/apiv2/userpoints/9775371/kyle.valdillez@chefd.com?access_token=fd6wHXXKtgj0TG0B83AU

  FORM DATA:
  Key = 'action_id'
  Value = '122'

  Key = 'action_use'
  Value = '4'
  ```

  _Sample Response_

  ```javascript
  {
    "error_code": "0",
    "description": "...",
    "status_code": 123
  }
  ```

* `POST /apiv2/userpoints/{site_id}/{customer_email}?access_token={access_token}`

  | Argument         | Description                       |   Type   | Required |
  | ---------------- | --------------------------------- | :------: | :------: |
  | `site_id`        | Annex Cloud site ID               | `string` |   [x]    |
  | `customer_email` | Shopify customer email            | `string` |   [x]    |
  | `access_token`   | Annex Cloud access token          | `string` |   [x]    |
  | `action_id`      | Annex Cloud defined action ID     | `string` |   [x]    |
  | `action_use`     | Annex Cloud defined action use ID | `string` |   [x]    |

  Used to allocate points for answering personalization questions.

  _Sample Request_

  ```javascript
  POST https://s15.socialannex.net/apiv2/userpoints/9775371/kyle.valdillez@chefd.com?access_token=fd6wHXXKtgj0TG0B83AU

  FORM DATA:
  Key = 'action_id'
  Value = '124'

  Key = 'action_use'
  Value = '4'
  ```

  _Sample Response_

  ```javascript
  {
    "error_code": "0",
    "description": "...",
    "status_code": 123
  }
  ```

* `GET /apiv2/user/{site_id}/{customer_email}?access_token={access_token}`

  | Argument         | Description              |   Type   | Required |
  | ---------------- | ------------------------ | :------: | :------: |
  | `site_id`        | Annex Cloud site ID      | `string` |   [x]    |
  | `customer_email` | Shopify customer email   | `string` |   [x]    |
  | `access_token`   | Annex Cloud access token | `string` |   [x]    |

  Used to get a users currently available points and other info.

  _Sample Request_

  ```javascript
  GET https://s15.socialannex.net/apiv2/user/9775371/kyle.valdillez@chefd.com?access_token=fd6wHXXKtgj0TG0B83AU
  ```

  _Sample Response_

  ```javascript
  {
    "error_code": "0",
    "data": {
      "site_id": "9775371",
      "user_email": "",
      "first_name": "Kyle",
      "last_name": "Valdillez",
      "user_status": "1",
      "phone": "",
      "phone1": "",
      "user_date_of_birth": "0000-00-00",
      "loyalty_id": "kyle.valdillez@chefd.com",
      "user_created_date": "2017-07-30 20:19:52",
      "user_update_date": "2017-07-30 20:19:52",
      "home_yard": "",
      "user_name": "",
      "active": "",
      "available_points": "444.00",
      "lifetime_points": "3444.00",
      "used_points": "3000.00",
      "hold_points": "0.00",
      "points_to_currency": "",
      "tiers": [],
      "segment_details": [],
      "reward_details": []
    }
  }
  ```

* `POST /apiv2/user/{site_id}/{customer_email}?access_token={access_token}`

  | Argument         | Description                      |   Type   | Required |
  | ---------------- | -------------------------------- | :------: | :------: |
  | `site_id`        | Annex Cloud site ID              | `string` |   [x]    |
  | `customer_email` | Shopify customer email           | `string` |   [x]    |
  | `access_token`   | Annex Cloud access token         | `string` |   [x]    |
  | `email`          | User's email address             | `string` |   [x]    |
  | `incentive_id`   | Annex Cloud defined incentive ID | `string` |   [x]    |

  Used to sign up a user for the loyalty program.

  _Sample Request_

  ```javascript
  POST https://s15.socialannex.net/apiv2/user/9775371/kyle.valdillez@chefd.com?access_token=fd6wHXXKtgj0TG0B83AU

  FORM DATA:
  Key = 'email'
  Value = 'kyle.valdillez@chefd.com'

  Key = 'incentive_id'
  Value = '2826'
  ```

  _Sample Response_

  ```javascript
  {
    "error_code": "0",
    "id": "24018023"
  }
  ```

* `GET /apiv2/rewardlist/{site_id}/{customer_email}?access_token={access_token}&filter=0`

  | Argument         | Description              |   Type   | Required |
  | ---------------- | ------------------------ | :------: | :------: |
  | `site_id`        | Annex Cloud site ID      | `string` |   [x]    |
  | `customer_email` | Shopify customer email   | `string` |   [x]    |
  | `access_token`   | Annex Cloud access token | `string` |   [x]    |

  Used to get a list of the customer’s redeemed rewards.

  _Sample Request_

  ```javascript
  GET https://s15.socialannex.net/apiv2/rewardlist/9775371/kyle.valdillez@chefd.com?access_token=fd6wHXXKtgj0TG0B83AU&filter=0
  ```

  _Sample Response_

  ```javascript
  {
    "error_code": "0",
    "data": [
      {
        "reward_id": "102027",
        "reward_name": "$20",
        "reward_code": "23647b75acab8fg7",
        "points_used": "2000",
        "is_used_in_purchase": "0",
        "db_add_date": "2017-09-14 15:45:16"
      },
      {
        "reward_id": "102026",
        "reward_name": "$10",
        "reward_code": "h44c8ha3g2346832",
        "points_used": "1000",
        "is_used_in_purchase": "0",
        "db_add_date": "2017-09-07 14:20:31"
      }
    ]
  }
  ```

* `GET /apiv2/reward/{site_id}/{customer_email}?access_token={access_token}`

  | Argument         | Description              |   Type   | Required |
  | ---------------- | ------------------------ | :------: | :------: |
  | `site_id`        | Annex Cloud site ID      | `string` |   [x]    |
  | `customer_email` | Shopify customer email   | `string` |   [x]    |
  | `access_token`   | Annex Cloud access token | `string` |   [x]    |

  Used to get a list of eligible awards from the redeemed rewards.

  _Sample Request_

  ```javascript
  GET https://s15.socialannex.net/apiv2/reward/9775371/kyle.valdillez@chefd.com?access_token=fd6wHXXKtgj0TG0B83AU
  ```

  _Sample Response_

  ```javascript
  // Since I have no eligible awards, I get this response below:

  {
    "error_code": "1",
    "description": "Rewards not eligible",
    "status_code": 1000035
  }
  ```

* `GET /apiv2/actions/{site_id}?access_token={access_token}`

  | Argument         | Description              |   Type   | Required |
  | ---------------- | ------------------------ | :------: | :------: |
  | `site_id`        | Annex Cloud site ID      | `string` |   [x]    |
  | `customer_email` | Shopify customer email   | `string` |   [x]    |
  | `access_token`   | Annex Cloud access token | `string` |   [x]    |

  Used to get a list of all the actions a user can take to earn points.

  _Sample Request_

  ```javascript
  GET https://s15.socialannex.net/apiv2/actions/9775371?access_token=fd6wHXXKtgj0TG0B83AU
  ```

  _Sample Response_

  ```javascript
  {
    "error_code": "0",
    "data": [{
        "id": "6075",
        "site_id": "9775371",
        "action_id": "515",
        "action_type": "1",
        "action_name": "First Time Purchaser Bonus",
        "action_points": "100",
        "maximum_points": "100",
        "period": "0",
        "ratio": "0",
        "active": "1",
        "refferal_back_points": "0",
        "refferal_back_max_points": "0",
        "refferal_back_max_period": "0",
        "refferal_order_points": "0",
        "refferal_order_max_points": "0",
        "refferal_order_max_period": "0",
        "action_name_display": "First Purchase Bonus",
        "action_point_display": "+100 pts",
        "action_limit_display": "1 time",
        "action_link_url": "",
        "period_limit": "0",
        "points_expire_duration": "365",
        "period_limit_refer_back": "0",
        "display_action_sequence": "0",
        "is_badges_active": "0",
        "action_image_url": "",
        "is_campaign": "0",
        "skip_from_leaderboard": "0",
        "is_action_series": "0",
        "is_action_series_in_order": "0",
        "no_time_performed": "0",
        "time_period_performed": "0",
        "action_ratio": "0",
        "action_description_display": "New to Chef’d? On your first purchase, you’ll get an additional 100 points on top of your purchase points!",
        "action_category_id": "43",
        "action_discount": "",
        "refferal_back_display_name": "",
        "refferal_order_display_name": "",
        "action_activity_display_name": "First Time Purchaser Bonus",
        "action_token": "0",
        "segment_id": "0",
        "tier_id": "0",
        "hold_points_days": "0",
        "db_add_date": "2017-07-14 05:46:37",
        "db_update_date": "2017-09-12 08:47:50",
        "action_category_name": "Shop"
      },
      {
        "id": "5328",
        "site_id": "9775371",
        "action_id": "121",
        "action_type": "2",
        "action_name": "Create an Account",
        "action_points": "250",
        "maximum_points": "250",
        "period": "0",
        "ratio": "0",
        "active": "1",
        "refferal_back_points": "0",
        "refferal_back_max_points": "0",
        "refferal_back_max_period": "0",
        "refferal_order_points": "0",
        "refferal_order_max_points": "0",
        "refferal_order_max_period": "0",
        "action_name_display": "Create an Account",
        "action_point_display": "+250 pts",
        "action_limit_display": "1 time",
        "action_link_url": "",
        "period_limit": "0",
        "points_expire_duration": "0",
        "period_limit_refer_back": "0",
        "display_action_sequence": "0",
        "is_badges_active": "0",
        "action_image_url": "",
        "is_campaign": "0",
        "skip_from_leaderboard": "0",
        "is_action_series": "0",
        "is_action_series_in_order": "0",
        "no_time_performed": "0",
        "time_period_performed": "0",
        "action_ratio": "0",
        "action_description_display": "Getting started with Chef’d is easy—and rewarding! Set up your Chef’d account and instantly receive 250 points!",
        "action_category_id": "45",
        "action_discount": "",
        "refferal_back_display_name": "",
        "refferal_order_display_name": "",
        "action_activity_display_name": "Create an Account",
        "action_token": "0",
        "segment_id": "0",
        "tier_id": "0",
        "hold_points_days": "0",
        "db_add_date": "2016-12-29 01:45:45",
        "db_update_date": "2017-09-12 08:51:09",
        "action_category_name": "Set Up"
      },
      {
        "id": "5329",
        "site_id": "9775371",
        "action_id": "109",
        "action_type": "2",
        "action_name": "Refer a Friend to purchase",
        "action_points": "1000",
        "maximum_points": "100000000",
        "period": "0",
        "ratio": "0",
        "active": "1",
        "refferal_back_points": "0",
        "refferal_back_max_points": "0",
        "refferal_back_max_period": "0",
        "refferal_order_points": "0",
        "refferal_order_max_points": "0",
        "refferal_order_max_period": "0",
        "action_name_display": "Refer a Friend to purchase",
        "action_point_display": "+1,000 pts",
        "action_limit_display": "Unlimited",
        "action_link_url": "",
        "period_limit": "0",
        "points_expire_duration": "0",
        "period_limit_refer_back": "0",
        "display_action_sequence": "0",
        "is_badges_active": "0",
        "action_image_url": "",
        "is_campaign": "0",
        "skip_from_leaderboard": "0",
        "is_action_series": "0",
        "is_action_series_in_order": "0",
        "no_time_performed": "0",
        "time_period_performed": "0",
        "action_ratio": "0",
        "action_description_display": "Earn 1,000 points when you refer friend! Once your friend places their order using your referral link, you’ll get your points.",
        "action_category_id": "42",
        "action_discount": "",
        "refferal_back_display_name": "",
        "refferal_order_display_name": "",
        "action_activity_display_name": "Refer a Friend to purchase",
        "action_token": "0",
        "segment_id": "0",
        "tier_id": "0",
        "hold_points_days": "0",
        "db_add_date": "2016-12-29 01:46:56",
        "db_update_date": "2017-09-12 08:51:52",
        "action_category_name": "Share"
      }
      ...
    ]
  }
  ```

* `GET /apiv2/useractivity/{site_id}/{customer_email}?access_token={access_token}`

  | Argument         | Description              |   Type   | Required |
  | ---------------- | ------------------------ | :------: | :------: |
  | `site_id`        | Annex Cloud site ID      | `string` |   [x]    |
  | `customer_email` | Shopify customer email   | `string` |   [x]    |
  | `access_token`   | Annex Cloud access token | `string` |   [x]    |

  Used to get a list of actions taken by the customer to receive loyalty points for point history, available actions left, etc.

  _Sample Request_

  ```javascript
  GET https://s15.socialannex.net/apiv2/useractivity/9775371/kyle.valdillez@chefd.com?access_token=fd6wHXXKtgj0TG0B83AU
  ```

  _Sample Response_

  ```javascript
  {
    "error_code": "0",
    "activity_data": [{
        "id": "44913976",
        "site_id": "9775371",
        "service_id": "0",
        "user_id": "16884640",
        "action_id": "121",
        "earned_points": "250",
        "used_points": "0",
        "available_points": "250",
        "stat_id": "0",
        "term_status": "0",
        "term_date": "0000-00-00 00:00:00",
        "action_use": "4",
        "reason": "",
        "rec_ip_address": "0",
        "order_id": "",
        "api_post_status": "0",
        "api_call": "0",
        "fromemail": "",
        "new_user_id": "0",
        "expire_date": "2018-09-06 17:47:06",
        "expire_points_status": "0",
        "counter": "0",
        "is_test_data": "0",
        "random_id": "0",
        "db_add_date": "2017-09-06 17:47:06",
        "db_update_date": "0000-00-00",
        "api_time": "0000-00-00 00:00:00",
        "api_feed_done": "0",
        "allow_points": "0",
        "expired_by_cron": "0",
        "expired_by_cron_date": "0000-00-00 00:00:00",
        "re_update": "0",
        "old_user_id": "0",
        "display_xp": "1",
        "campaign": "0",
        "internal_reason": "",
        "event_description": "",
        "store_id": "",
        "is_instore_activity": "0",
        "customer_type": "0",
        "purchase_type": "0",
        "reservation_id": "0",
        "action_name": "Create an Account",
        "action_activity_display_name": "Create an Account",
        "refferal_back_display_name": "",
        "refferal_order_display_name": ""
      },
      {
        "id": "45217954",
        "site_id": "9775371",
        "service_id": "0",
        "user_id": "16884640",
        "action_id": "600",
        "earned_points": "43",
        "used_points": "0",
        "available_points": "0",
        "stat_id": "0",
        "term_status": "0",
        "term_date": "0000-00-00 00:00:00",
        "action_use": "4",
        "reason": "",
        "rec_ip_address": "0",
        "order_id": "6206026316",
        "api_post_status": "0",
        "api_call": "0",
        "fromemail": "",
        "new_user_id": "0",
        "expire_date": "2018-09-07 18:47:48",
        "expire_points_status": "0",
        "counter": "0",
        "is_test_data": "0",
        "random_id": "0",
        "db_add_date": "2017-09-07 18:47:48",
        "db_update_date": "2017-09-07",
        "api_time": "0000-00-00 00:00:00",
        "api_feed_done": "0",
        "allow_points": "0",
        "expired_by_cron": "0",
        "expired_by_cron_date": "0000-00-00 00:00:00",
        "re_update": "0",
        "old_user_id": "0",
        "display_xp": "1",
        "campaign": "0",
        "internal_reason": "",
        "event_description": "",
        "store_id": "",
        "is_instore_activity": "0",
        "customer_type": "0",
        "purchase_type": "0",
        "reservation_id": "0",
        "action_name": "Purchase",
        "action_activity_display_name": "Purchase",
        "refferal_back_display_name": "",
        "refferal_order_display_name": ""
      },
      {
        "id": "45217955",
        "site_id": "9775371",
        "service_id": "0",
        "user_id": "16884640",
        "action_id": "515",
        "earned_points": "100",
        "used_points": "0",
        "available_points": "100",
        "stat_id": "0",
        "term_status": "0",
        "term_date": "0000-00-00 00:00:00",
        "action_use": "4",
        "reason": "0",
        "rec_ip_address": "0",
        "order_id": "0",
        "api_post_status": "0",
        "api_call": "0",
        "fromemail": "",
        "new_user_id": "0",
        "expire_date": "2018-09-07 18:47:48",
        "expire_points_status": "0",
        "counter": "0",
        "is_test_data": "0",
        "random_id": "0",
        "db_add_date": "2017-09-07 18:47:49",
        "db_update_date": "0000-00-00",
        "api_time": "0000-00-00 00:00:00",
        "api_feed_done": "0",
        "allow_points": "0",
        "expired_by_cron": "0",
        "expired_by_cron_date": "0000-00-00 00:00:00",
        "re_update": "0",
        "old_user_id": "0",
        "display_xp": "1",
        "campaign": "0",
        "internal_reason": "",
        "event_description": "",
        "store_id": "",
        "is_instore_activity": "0",
        "customer_type": "0",
        "purchase_type": "0",
        "reservation_id": "0",
        "action_name": "First Time Purchaser Bonus",
        "action_activity_display_name": "First Time Purchaser Bonus",
        "refferal_back_display_name": "",
        "refferal_order_display_name": ""
      }
      ...
    ]
  }
  ```

* `GET /apiv2/noneligieblereward/{site_id}/{customer_email}?access_token={access_token}`

  | Argument         | Description              |   Type   | Required |
  | ---------------- | ------------------------ | :------: | :------: |
  | `site_id`        | Annex Cloud site ID      | `string` |   [x]    |
  | `customer_email` | Shopify customer email   | `string` |   [x]    |
  | `access_token`   | Annex Cloud access token | `string` |   [x]    |

  Used to get a list of the locked/non eligible rewards for a customer so they can see what they could possibly get with enough points.

  _Sample Request_

  ```javascript
  GET https://s15.socialannex.net/apiv2/noneligieblereward/9775371/kyle.valdillez@chefd.com?access_token=fd6wHXXKtgj0TG0B83AU
  ```

  _Sample Response_

  ```javascript
  {
    "error_code": "0",
    "data": [
      {
        "reward_id": "102026",
        "reward_name": "$10",
        "reward_desc": "",
        "earned_points_required": "1000",
        "deduct_amount": "0.00",
        "is_campaign": "0"
      },
      {
        "reward_id": "102027",
        "reward_name": "$20",
        "reward_desc": "",
        "earned_points_required": "2000",
        "deduct_amount": "0.00",
        "is_campaign": "0"
      },
      {
        "reward_id": "102028",
        "reward_name": "$30",
        "reward_desc": "",
        "earned_points_required": "3000",
        "deduct_amount": "0.00",
        "is_campaign": "0"
      },
      {
        "reward_id": "102029",
        "reward_name": "$40",
        "reward_desc": "",
        "earned_points_required": "4000",
        "deduct_amount": "0.00",
        "is_campaign": "0"
      }
    ]
  }
  ```

### <a id="sa-question-answer"></a>**Question & Answer**

All URLs referenced in this section of the documentation have the following base:

|    Staging & Production     | Staging Site ID | Production Site ID |
| :-------------------------: | :-------------: | :----------------: |
| https://s23.socialannex.com |     9775370     |      9775371       |

* `GET /api/product/quscount/{site_id}/{product_id}/2`

  | Argument     | Description         |   Type   | Required |
  | ------------ | ------------------- | :------: | :------: |
  | `site_id`    | Annex Cloud site ID | `string` |   [x]    |
  | `product_id` | Shopify product ID  | `string` |   [x]    |

  Used to get the number of questions about a product.

  _Sample Request_

  ```javascript
  GET https://s23.socialannex.com/api/product/quscount/9775371/458004911/2
  ```

  _Sample Response_

  ```javascript
  {
    "status_code": "200",
    "message": "OK",
    "errorno": "0",
    "error_message": "",
    "question_count": "3"
  }
  ```

* `GET /api/product/qa/{site_id}/{product_id}/1/1`

  | Argument     | Description         |   Type   | Required |
  | ------------ | ------------------- | :------: | :------: |
  | `site_id`    | Annex Cloud site ID | `string` |   [x]    |
  | `product_id` | Shopify product ID  | `string` |   [x]    |

  Used to get the number of questions about a product.

  _Sample Request_

  ```javascript
  GET https://s23.socialannex.com/api/product/qa/9775371/458004911/1/1
  ```

  _Sample Response_

  ```javascript
  {
    "status_code": "200",
    "message": "OK",
    "errorno": "0",
    "error_message": "",
    "question_answers": [
      {
        "anscnt": "1",
        "question_id": "46690",
        "question": "How long does the dish take to prepare and cook?",
        "product_id": "53942048",
        "like_count": "0",
        "unlike_count": "0",
        "more_details": "",
        "question_add_time": "2017-01-20 13:48:48",
        "user_id": "22159",
        "user_email": "mloebker@gmail.com",
        "city": "Kentucky",
        "state": "",
        "country": "",
        "gender": "",
        "age": "",
        "display_name": "Mo",
        "answers": [
          {
            "answer_id": "230178",
            "question_id": "46690",
            "answer": "I made this recipe 2 weeks ago and it took me about 45 of prep time and cooking and it was delicious!",
            "like_count": "0",
            "unlike_count": "0",
            "is_helpful_yes": "8",
            "is_helpful_no": "4",
            "answer_add_time": "2017-01-20 16:12:48",
            "user_id": "22165",
            "user_email": "bencariou@gmail.com",
            "city": "United States",
            "state": "",
            "country": "",
            "gender": "",
            "age": "",
            "display_name": "Olympique51"
          }
        ]
      }
    ]
  }
  ```

* `POST /api/question/qussave/{site_id}/{product_id}`

  | Argument     | Description            |   Type   | Required |
  | ------------ | ---------------------- | :------: | :------: |
  | `site_id`    | Annex Cloud site ID    | `string` |   [x]    |
  | `product_id` | Shopify product ID     | `string` |   [x]    |
  | `question`   | User inputted question | `string` |   [x]    |
  | `user_email` | User email address     | `string` |   [x]    |
  | `nick_name`  | User display name      | `string` |   [x]    |
  | `location`   | User display location  | `string` |   [x]    |

  Used to ask a question about a product (curated by Customer Care).

  _Sample Request_

  ```javascript
  POST https://s23.socialannex.com/api/question/qussave/9775371/458004911

  FORM DATA:
  Key = 'question'
  Value = 'How long does it take to cook this?'

  Key = 'user_email'
  Value = 'kyle.valdillez@chefd.com'

  Key = 'nick_name'
  Value = 'Kyle V'

  Key = 'location'
  Value = 'Los Angeles, CA'
  ```

  _Sample Response_

  ```javascript
  {
    "status_code": "200",
    "message": "OK",
    "errorno": "0",
    "error_message": "",
    "description": "Question submited successfully"
  }
  ```

* `POST /api/answer/anssave/{site_id}/{product_id}`

  | Argument      | Description                             |   Type   | Required |
  | ------------- | --------------------------------------- | :------: | :------: |
  | `site_id`     | Annex Cloud site ID                     | `string` |   [x]    |
  | `product_id`  | Shopify product ID                      | `string` |   [x]    |
  | `answer`      | User inputted answer                    | `string` |   [x]    |
  | `question_id` | Annex Cloud question ID                 | `string` |   [x]    |
  | `user_email`  | User email address                      | `string` |   [x]    |
  | `nick_name`   | User display name                       | `string` |   [x]    |
  | `location`    | Hard-coded location, not used/displayed | `string` |   [x]    |

  Used to ask a question about a product (curated by Customer Care).

  _Sample Request_

  ```javascript
  POST https://s23.socialannex.com/api/answer/anssave/9775371/458004911

  FORM DATA:
  Key = 'answer'
  Value = 'It takes 45mins to cook.'

  Key = 'question_id'
  Value = '46690'

  Key = 'user_email'
  Value = 'kyle.valdillez@chefd.com'

  Key = 'nick_name'
  Value = 'Kyle V'

  Key = 'location'
  Value = 'India'
  ```

  _Sample Response_

  ```javascript
  {
    "status_code": "200",
    "message": "OK",
    "errorno": "0",
    "error_message": "",
    "description": "Answer submited successfully"
  }
  ```

* `PUT /api/answer/ishelpfull/{site_id}/{review_id}/1/{customer_email}`

  | Argument         | Description           |   Type   | Required |
  | ---------------- | --------------------- | :------: | :------: |
  | `site_id`        | Annex Cloud site ID   | `string` |   [x]    |
  | `review_id`      | Annex Cloud review ID | `string` |   [x]    |
  | `customer_email` | User email address    | `string` |   [x]    |

  Used to mark an answer as helpful.

  _Sample Request_

  ```javascript
  PUT https://s23.socialannex.com/api/answer/ishelpfull/9775371/230178/1/kyle.valdillez@chefd.com
  ```

  _Sample Response_

  ```javascript
  {
    "status_code": "200",
    "message": "OK",
    "errorno": "0",
    "error_message": "",
    "description": "'Helpful' count updated successfully."
  }
  ```

* `PUT /api/answer/ishelpfull/{site_id}/{review_id}/2/{customer_email}`

  | Argument         | Description           |   Type   | Required |
  | ---------------- | --------------------- | :------: | :------: |
  | `site_id`        | Annex Cloud site ID   | `string` |   [x]    |
  | `review_id`      | Annex Cloud review ID | `string` |   [x]    |
  | `customer_email` | User email address    | `string` |   [x]    |

  Used to mark an answer as helpful.

  _Sample Request_

  ```javascript
  PUT https://s23.socialannex.com/api/answer/ishelpfull/9775371/230178/2/kyle.valdillez@chefd.com
  ```

  _Sample Response_

  ```javascript
  {
    "status_code": "200",
    "message": "OK",
    "errorno": "0",
    "error_message": "",
    "description": "'Not helpful' count updated successfully."
  }
  ```

### <a id="sa-refer-friend"></a>**Refer a Friend**

All URLs referenced in this section of the documentation have the following base:

|    Staging & Production    | Staging Site ID | Production Site ID |
| :------------------------: | :-------------: | :----------------: |
| https://s2.socialannex.net |     9775370     |      9775371       |

* `POST /api/createuser/{site_id}?access_token={access_token}`

  | Argument       | Description              |   Type   | Required |
  | -------------- | ------------------------ | :------: | :------: |
  | `site_id`      | Annex Cloud site ID      | `string` |   [x]    |
  | `access_token` | Annex Cloud access token | `string` |   [x]    |
  | `email`        | User email address       | `string` |   [x]    |
  | `incentive_id` | Annex Cloud incentive ID | `string` |   [x]    |
  | `sa_stat_id`   | Annex Cloud referral ID  | `string` |          |

  Used to create a user, if there is a referral ID will pass through to checkout so the referrer will get credited.

  _Sample Request_

  ```javascript
  POST https://s2.socialannex.net/api/createuser/9775371?access_token=4c1b19e6fa91623bf185fa7746870271`

  FORM DATA:
  Key = 'email'
  Value = 'kyle.valdillez@chefd.com'

  Key = 'incentive_id'
  Value = '2826'
  ```

  _Sample Response_

  ```javascript
  {
    "Status": "success",
    "data": {
      "user_id": "4560360",
      "user_name": " ",
      "personal_data": "https:\/\/chefd.app.link\/vFmflNUDpJ",
      "sharer_stat_id": "0",
      "invite_code": "D63EZc",
      "messages": "User Login successfully"
    }
  }
  ```

* `POST /api/createbitly/{site_id}?access_token={access_token}`

  | Argument       | Description              |   Type   | Required |
  | -------------- | ------------------------ | :------: | :------: |
  | `site_id`      | Annex Cloud site ID      | `string` |   [x]    |
  | `access_token` | Annex Cloud access token | `string` |   [x]    |
  | `user_id`      | Annex Cloud user ID      | `string` |   [x]    |
  | `socialType`   | Annex Cloud social ID    | `string` |   [x]    |
  | `incentive_id` | Annex Cloud incentive ID | `string` |   [x]    |

  Used to create bit.ly link to share with friends to refer them.

  _Sample Request_

  ```javascript
  POST https://s2.socialannex.net/api/createbitly/9775371?access_token=4c1b19e6fa91623bf185fa7746870271`

  FORM DATA:
  Key = 'user_id'
  Value = '4560360'

  Key = 'socialType'
  Value = '2'

  Key = 'incentive_id'
  Value = '2827'
  ```

  _Sample Response_

  ```javascript
  {
    "Status": "success",
    "data": {
      "bitly": "https:\/\/chefd.app.link\/gfycbvV81J",
      "Loyalty points": {
        "errorcode": "1",
        "shared_details": {
          "user_id": "4560360",
          "status": 1,
          "points_given": "Input params are not valid"
        },
        "Action performed": "Action ID Found"
      }
    }
  }
  ```

  * `POST /api/sendemail/{site_id}?access_token={access_token}`

  | Argument       | Description                   |   Type   | Required |
  | -------------- | ----------------------------- | :------: | :------: |
  | `site_id`      | Annex Cloud site ID           | `string` |   [x]    |
  | `access_token` | Annex Cloud access token      | `string` |   [x]    |
  | `user_id`      | Annex Cloud user ID           | `string` |   [x]    |
  | `toemail`      | User's friend's email address | `string` |   [x]    |
  | `incentive_id` | Annex Cloud incentive ID      | `string` |   [x]    |

  Used to send an email to a friend with a specific URL that will allow the user to receive points for the friend they referred if they purchase for the first time.

  _Sample Request_

  ```javascript
  POST https://s2.socialannex.net/api/sendemail/9775371?access_token=4c1b19e6fa91623bf185fa7746870271`

  FORM DATA:
  Key = 'user_id'
  Value = '4560360'

  Key = 'toemail'
  Value = 'kyleraf@mailinator.com'

  Key = 'incentive_id'
  Value = '2827'
  ```

  _Sample Response_

  ```javascript
  {
    "Status": "success",
    "data": ["kyleraf@mailinator.com send mail successfully"],
    "loyalty points": {
      "errorcode": "1",
      "shared_details": {
        "user_id": "4560360",
        "status": 1,
        "points_given": "Input params are not valid"
      },
      "Action performed": "Action ID Found"
    }
  }
  ```
