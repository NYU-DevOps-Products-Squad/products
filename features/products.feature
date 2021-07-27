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
        | dog        | good        | 10.5   |    10     | ada   |   pet    | 
        | book       | good        | 2      |    15     | bob   |   book   | 

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Product Demo REST API Service" in the title
    And I should not see "404 Not Found"

Scenario: List all products
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see "apple" in the results
    And I should see "banana" in the results
    And I should see "peach" in the results
    And I should see "dog" in the results
    And I should see "book" in the results

Scenario: Search all products named apple
    When I visit the "Home Page"
    And I set the "Name" to "apple"
    And I press the "Search" button
    Then I should see "apple" in the results
    And I should not see "banana" in the results
    And I should not see "peach" in the results
    And I should not see "dog" in the results
    And I should not see "book" in the results

Scenario: Search all products price is 2
    When I visit the "Home Page"
    And I set the "Price" to "2"
    And I press the "Search" button
    Then I should see "banana" in the results
    And I should see "book" in the results
    And I should not see "apple" in the results
    And I should not see "peach" in the results
    And I should not see "dog" in the results

Scenario: Search all products in category fruit
    When I visit the "Home Page"
    And I set the "Category" to "fruit"
    And I press the "Search" button
    Then I should see "apple" in the results
    And I should see "banana" in the results
    And I should see "peach" in the results
    And I should not see "dog" in the results
    And I should not see "book" in the results

Scenario: Search all products owned by sun
    When I visit the "Home Page"
    And I set the "Owner" to "sun"
    And I press the "Search" button
    Then I should see "apple" in the results
    And I should see "banana" in the results
    And I should see "peach" in the results
    And I should not see "dog" in the results
    And I should not see "book" in the results

