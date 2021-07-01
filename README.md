# products
Repo for the products team or NYU DevOps 2021 summer

### Database  Fields
| Fields | Type | Description
| :--- | :--- | :--- |
| id | String | ID 
| name | String | Product Name
| description | String | Product Description
| price | Float | Product Price
| inventory | Int | Product Amount
| Owner | String | OwnerID
| Category | String | Product Category|

## API Documentation
### URLS

 |                 URL                 | HTTP Method |                         Description                          |
| :---------------------------------: | :---------: | :----------------------------------------------------------: |
|              /api/products              |   **GET**   |              Returns a list all of the products              |
|           /api/products/{id}            |   **GET**   |             Returns the product with a given id              |
|       /api/products/{id}/purchase       |  **POST**   | purchases the product with the corresponding id by adding it to user's shopping cart |
