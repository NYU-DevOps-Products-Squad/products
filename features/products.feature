Feature: The product store service back-end
    As a Product Store Owner
    I need a RESTful catalog service
    So that I can keep track of all my products

Background:
    Given the following products
        | name       | description |  price | inventory | owner | category |
        | apple      | good        | 2.1    |    10     | sun   |   fruit  |
        | banana     | good        | 2      |    10     | sun   |   fruit  | 
        | peach      | good        | 5.5    |    10     | sun   |   fruit  | 

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Product Demo REST API Service" in the title
    And I should not see "404 Not Found"

Scenario: Update a Product
    When I visit the "Home Page"
    And I set the "Name" to "peach"
    And I press the "Search" button
    Then I should see "peach" in the "Name" field
    And I should see "fruit" in the "Category" field
    When I change "Name" to "pear"
    And I press the "Update" button
    Then I should see the message "Success"
    When I copy the "ID" field
    And I press the "Clear" button
    And I paste the "ID" field
    And I press the "Retrieve" button
    Then I should see "pear" in the "Name" field











