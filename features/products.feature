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

Scenario: Update a Product
    When I visit the "Home Page"
    And I set the "Search_Name" to "iPhone 12"
    And I press the "Search" button
    Then I should see "iPhone 12" in the "Name" field
    And I should see "Tech" in the "Category" field
    When I change "Name" to "iPhone X"
    And I press the "Update" button
    Then I should see the message "Product has been Updated!"
    When I copy the "ID" field
    And I press the "Clear" button
    And I paste the "ID" field
    And I press the "Retrieve" button
    Then I should see "iPhone X" in the "Name" field
    When I press the "Clear" button
    And I press the "Search" button
    Then I should see "iPhone X" in the results
    Then I should not see "iPhone 12" in the results
    
    
