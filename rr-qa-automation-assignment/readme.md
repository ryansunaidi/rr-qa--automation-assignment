# QA Automation Assignment

## Overview
This project contains automated tests for the TMDB Discover demo website (https://tmdb-discover.surge.sh/). The test suite validates filtering options, navigation, pagination, and content display functionality.

## Testing Strategy

### 1. Test Categories
- **Smoke Tests**: Basic functionality verification
- **Regression Tests**: Comprehensive feature testing
- **Negative Tests**: Error handling and edge cases
- **Content Validation**: UI element verification

### 2. Test Design Techniques
- **Equivalence Partitioning**: Year ranges, rating values
- **Boundary Value Analysis**: Pagination limits, year boundaries
- **Positive/Negative Testing**: Valid and invalid inputs
- **State Transition**: Navigation between pages/sections

### 3. Test Cases Generated

#### Filtering Tests
1. Navigation between categories (Popular, Trend, New, Top Rated)
2. Search functionality with valid/invalid terms
3. Type filter (Movie/TV Show)
4. Year range filtering
5. Rating filter validation
6. Genre selection (if implemented)

#### Pagination Tests
1. Basic next/previous navigation
2. Page number selection
3. Button state verification (disabled/enabled)
4. Last page handling (known issue)

#### Navigation Tests
1. Direct URL access (negative case)
2. Browser back/forward navigation
3. URL slug validation

### 4. Framework Details

#### Libraries Used
- **Selenium WebDriver**: Browser automation
- **Pytest**: Test framework and runner
- **Pytest-html**: HTML reporting
- **WebDriver Manager**: Automatic driver management
- **Logging**: Comprehensive test logging

#### Patterns Implemented
1. **Page Object Model (POM)**: Separates page logic from tests
2. **Singleton Logger**: Centralized logging
3. **Factory Pattern**: Browser instantiation
4. **Fixture Pattern**: Test setup/teardown

## How to Run Tests

### Prerequisites
- Python 3.8+
- Google Chrome browser

### Installation

# Install dependencies
pip install -r requirements.txt