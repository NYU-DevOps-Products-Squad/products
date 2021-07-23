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

Scenario: Create a Product
    When I visit the "Home Page"
    And I set the "Name" to "mango"
    And I set the "Description" to "good"
    And I set the "Price" to "3.5"
    And I set the "Inventory" to "10"
    And I set the "Owner" to "sun"
    And I set the "Category" to "fruit"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "Category" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "mango" in the "Name" field
    And I should see "good" in the "Description" field
    And I should see "3.5" in the "Price" field
    And I should see "10" in the "Inventory" field
    And I should see "sun" in the "Owner" field
    And I should see "fruit" in the "Category" field



Scenario: Read a Product
    When I visit the "Home Page" 
    And I set the "Name" to "apple"
    And I press the "Read" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "Category" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "apple" in the "Name" field
    And I should see "good" in the "Description" field
    And I should see "2.1" in the "Price" field
    And I should see "10" in the "Inventory" field
    And I should see "sun" in the "Owner" field
    And I should see "fruit" in the "Category" field



