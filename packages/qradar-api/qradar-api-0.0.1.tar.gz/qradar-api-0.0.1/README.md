# qradar-api

This package contains an object oriented approach to the QRadar API. The idea is to keep the logic simple, structure and allow for an easy way to integrate with the QRadar API.

This package was inspired by: https://github.com/ryukisec/qradar4py who already put in some ground work when it came to an object oriented approach.
This package goes further and adds models for the different object you can retrieve and post.

It is a work in progress though :)

## Structure

the package contains 
* Endpoints
    * Inherit from base class `QRadarAPIClient`
    * Use decorators to define which headers and parameters are allowed for each endpoint
    * located in src\qradar\api\endpoints
* Models
    * Inherit from base class `QRadarModel`, which provides them with a custom `__repr__` and `from_json()` factory
    * Located in src\qradar\models

## Installation
```bash
sudo pip3 install qradar-api
```

## Roadmap

- [ ] Set up decent packaging :package:
- [ ] Implement all models &  GET endpoints :rocket:
- [ ] Implement all post endpoints :pencil:
- [ ] Convince IBM to contribute when creating a new API version :pray:
- [ ] Write a nice set of unit tests :clown_face:

