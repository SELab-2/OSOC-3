# Module overview frontend

## components

Here are all components we need for the frontend. Components are organized into folders that group related components together. This structure helps keeping the directory clean.

## contexts

The contexts module contains our custom React context providers.

## data

This module contains our enums and interfaces.

## utils

This module has all functions that are not directly React-related, and a series of utility functions to make our code cleaner. This includes API requests, logic, and functions that interact with LocalStorage and SessionStorage.

## views

Here are all the views (pages) we have in the frontend. Every view is a very simple component, because they are split up into smaller components that can be found in the [components](#components) module.
