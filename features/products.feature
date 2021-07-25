Feature: The product management service back-end
    As a Product Management Service Owner
    I need a RESTful catalog service
    So that I can keep track of all my products

Background:
    Given the following products
        | name     | description    | price   | inventory | owner | category |
        | iPhone12 | Black iPhone12 | 999.99  | 10        | Alice | Tech     |
        | iPad     | iPad Air2      | 1099.99 | 20        | Bob   | Tech     |
        | Banana   | Big banana     | 9.99    | 50        | Jay   | Fruit    |


Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Product RESTful Service" in the title
    And I should not see "404 Not Found"
