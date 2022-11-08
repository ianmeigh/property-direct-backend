# API Testing

## TOC

- [Automated Testing](#automated-testing)
- [Manual Testing](#manual-testing)
  - [Endpoint Testing](#endpoint-testing)
  - [CRUD Functionality Testing](#crud-functionality-testing)
    - [Bookmarks App](#bookmarks-app)
    - [Followers App](#followers-app)
    - [Notes App](#notes-app)
    - [Profiles App](#profiles-app)
    - [Propertys App](#propertys-app)
- [Code Validation](#code-validation)

## Automated Testing

Automated tests were created for the Propertys, Notes, Bookmarks, Followers and Profiles applications.

Property tests focused on ensuring only sellers could create, edit and delete property. This involved mocking calls to the external API used to verify and get more information about postcodes.

Other automated testing focused on the privacy aspects of the Notes, Bookmarks, Followers and Profiles applications. This focus was to minimize the risk of any future development inadvertently exposing private user information. Links to tests create can be found below:

- [Bookmarks - View Tests](https://github.com/ianmeigh/property-direct-backend/blob/main/bookmarks/tests/test_views.py)
- [Followers - View Tests](https://github.com/ianmeigh/property-direct-backend/blob/main/followers/tests/test_views.py)
- [Notes - View Tests](https://github.com/ianmeigh/property-direct-backend/blob/main/notes/tests/test_views.py)
- [Profiles - View Tests](https://github.com/ianmeigh/property-direct-backend/blob/main/profiles/tests/test_views.py)
- [Propertys - View Tests](https://github.com/ianmeigh/property-direct-backend/blob/main/propertys/tests/test_views.py)
- [Propertys - Serializer Tests](https://github.com/ianmeigh/property-direct-backend/blob/main/propertys/tests/test_serializers.py)

Please find the full coverage report [here](docs/testing_coverage_report.png).

## Manual Testing

Manual testing took place throughout development of the API to ensure features functioned. These included visiting each URL to ensure accurate results were returned depending on authorization state, the creation, update and deletion of items:

### Endpoint Testing

| URL | Passed |
|---|---|
| root | :white_check_mark: |
| /bookmarks/ | :white_check_mark: |
| /bookmarks/\<id>/ | :white_check_mark: |
| /followers/ | :white_check_mark: |
| /followers/\<id>/ | :white_check_mark: |
| /notes/ | :white_check_mark: |
| /notes/\<id>/ | :white_check_mark: |
| /profiles/ | :white_check_mark: |
| /profiles/\<id>/ | :white_check_mark: |
| /profiles/\<id>/delete/ | :white_check_mark: |
| /property/ | :white_check_mark: |
| /property/create/ | :white_check_mark: |
| /property/\<id>/ | :white_check_mark: |

### CRUD Functionality Testing

#### Bookmarks App

| App | Action | Authenticated | Anonymous | Passed |
|---|---|---|---|---|
| Bookmarks | Read (List) | Array of owned objects | 403 Response | :white_check_mark: |
| Bookmarks | Read - Valid ID and Owner | Returns Detail | 404 Response | :white_check_mark: |
| Bookmarks | Read - Valid ID and not Owner | 404 Response | 404 Response | :white_check_mark: |
| Bookmarks | Read - Invalid ID | 404 Response | 404 Response  | :white_check_mark: |
| Bookmarks | Create | 201 Response | N/A | :white_check_mark: |
| Bookmarks | Update | N/A| N/A | N/A |
| Bookmarks | Delete | 204 Response | N/A | :white_check_mark: |

#### Followers App

| App | Action | Authenticated | Anonymous | Passed |
|---|---|---|---|---|
| Followers | Read (List) | Array of owned objects | Empty Results Array | :white_check_mark: |
| Followers | Read - Valid ID and Owner | Returns Detail | 403 Response | :white_check_mark: |
| Followers | Read - Valid ID and not Owner | 404 Response | 404 Response | :white_check_mark: |
| Followers | Read - Invalid ID | 404 Response | 404 Response  | :white_check_mark: |
| Followers | Create | 201 Response | N/A | :white_check_mark: |
| Followers | Update | N/A | N/A | N/A |
| Followers | Delete | 204 Response | N/A | :white_check_mark: |

#### Notes App

| App | Action | Authenticated | Anonymous | Passed |
|---|---|---|---|---|
| Notes | Read (List) | Array of owned objects | Empty Results Array | :white_check_mark: |
| Notes | Read - Valid ID and Owner | Returns Detail | 404 Response | :white_check_mark: |
| Notes | Read - Valid ID and not Owner | 404 Response | 404 Response | :white_check_mark: |
| Notes | Read - Invalid ID | 404 Response | 404 Response  | :white_check_mark: |
| Notes | Create | 201 Response | N/A | :white_check_mark: |
| Notes | Update | 200 Response | N/A | :white_check_mark: |
| Notes | Delete | 204 Response | N/A | :white_check_mark: |

#### Profiles App

| App | Action | Authenticated | Anonymous | Passed |
|---|---|---|---|---|
| Profiles | Read (List) | Array of seller profiles | Array of seller profiles | :white_check_mark: |
| Profiles | Read | Returns Detail | Returns Detail | :white_check_mark: |
| Profiles | Create | N/A | N/A | N/A |
| Profiles | Update | 200 Response | N/A | :white_check_mark: |
| Profiles | Delete | 204 Response | N/A | :white_check_mark: |

#### Propertys App

| App | Action | Authenticated | Anonymous | Passed |
|---|---|---|---|---|
| Propertys | Read (List) | Array of all properties | Array of all properties | :white_check_mark: |
| Propertys | Read | Returns Detail | Returns Detail | :white_check_mark: |
| Propertys | Create | 201 Response | N/A | :white_check_mark: |
| Propertys | Update | 200 Response | N/A | :white_check_mark: |
| Propertys | Delete | 204 Response | N/A | :white_check_mark: |

## Code Validation

The `pycodestyle` package was used to validate the project against the PEP8 Style Convention during development. No validation errors were found in the final deployed when validating files that were **not** automatically generated (e.g. validation excludes the 'settings.py' file and migration files).
