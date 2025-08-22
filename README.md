# Recipe Platform API

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-ff1709?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)

A comprehensive Django REST Framework API for managing recipes with user authentication, recipe creation by sellers, and rating system using JWT tokens. Supports both seller and customer user types.

## 🚀 Features

- **User Management**: User registration with seller/customer types and JWT-based authentication
- **Recipe Management**: Sellers can create, read, update, and delete recipes with images
- **Recipe Ratings**: Customers can rate recipes (1-5 stars) with unique rating per user per recipe
- **JWT Authentication**: Secure token-based authentication with access/refresh tokens
- **User Types**: Separate roles for sellers (create recipes) and customers (rate recipes)
- **Image Upload**: Recipe images with file upload support
- **Pagination**: Paginated API responses for better performance
- **Data Validation**: Robust input validation using DRF serializers with custom validators

## 📋 Table of Contents

- [Installation](#installation)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Usage Examples](#usage-examples)
- [Models](#models)
- [Project Structure](#project-structure)
- [Testing](#testing)

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/manoj8260/Assignment-DRF.git
   cd Assignment-DRF
   ```

2. **Create a virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Create a .env file in the root directory (optional)
   cp .env.example .env
   # Add your SECRET_KEY and other settings
   ```

5. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Start the development server**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://127.0.0.1:8000/`

## 📚 API Endpoints

### Base URL: `http://127.0.0.1:8000/api/`

### Authentication Endpoints
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/auth/register/` | User registration (seller/customer) | ❌ |
| POST | `/auth/login/` | User login (get JWT tokens) | ❌ |
| POST | `/auth/token/refresh/` | Refresh access token | ❌ |
| POST | `/auth/logout/` | User logout | ✅ |

### Recipe Endpoints
| Method | Endpoint | Description | Auth Required | User Type |
|--------|----------|-------------|---------------|-----------|
| GET | `/recipes/` | List all recipes (paginated) | ❌ | Any |
| POST | `/recipes/` | Create new recipe | ✅ | Seller only |
| GET | `/recipes/{id}/` | Get recipe details | ❌ | Any |
| PUT | `/recipes/{id}/` | Update recipe (owner only) | ✅ | Seller (owner) |
| PATCH | `/recipes/{id}/` | Partial update recipe | ✅ | Seller (owner) |
| DELETE | `/recipes/{id}/` | Delete recipe (owner only) | ✅ | Seller (owner) |

### Recipe Rating Endpoints
| Method | Endpoint | Description | Auth Required | User Type |
|--------|----------|-------------|---------------|-----------|
| GET | `/recipes/{recipe_id}/ratings/` | Get recipe ratings (paginated) | ❌ | Any |
| POST | `/recipes/{recipe_id}/ratings/` | Rate a recipe | ✅ | Customer |
| PUT | `/recipes/{recipe_id}/ratings/{id}/` | Update your rating | ✅ | Customer (owner) |
| DELETE | `/recipes/{recipe_id}/ratings/{id}/` | Delete your rating | ✅ | Customer (owner) |

### Pagination Parameters

All list endpoints support pagination:
- `?page=1` - Page number (default: 1)
- `?page_size=10` - Number of items per page (default: varies by endpoint)

Example: `GET /api/recipes/?page=2&page_size=5`

## 🔐 Authentication

This project uses **JWT (JSON Web Token) authentication** with user types (seller/customer). You'll receive:
- **Access Token**: For API requests (short-lived)
- **Refresh Token**: To get new access tokens (long-lived)
- **User Details**: Including user type, email, and full name

### Getting JWT Tokens

1. **Register a new seller:**
   ```bash
   curl -X POST http://127.0.0.1:8000/api/auth/register/ \
     -H "Content-Type: application/json" \
     -d '{
       "username": "chef123",
       "email": "chef@example.com",
       "password": "securepassword123",
       "first_name": "John",
       "last_name": "Chef",
       "user_type": "seller"
     }'
   ```

2. **Register a new customer:**
   ```bash
   curl -X POST http://127.0.0.1:8000/api/auth/register/ \
     -H "Content-Type: application/json" \
     -d '{
       "username": "foodie456",
       "email": "foodie@example.com",
       "password": "securepassword123",
       "first_name": "Jane",
       "last_name": "Foodie",
       "user_type": "customer"
     }'
   ```

3. **Login to get JWT tokens:**
   ```bash
   curl -X POST http://127.0.0.1:8000/api/auth/login/ \
     -H "Content-Type: application/json" \
     -d '{
       "username": "chef123",
       "password": "securepassword123"
     }'
   ```

   **Response:**
   ```json
   {
     "message": "Login successfully",
     "user_details": {
       "email": "chef@example.com",
       "full_name": "John Chef",
       "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
       "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
     }
   }
   ```

4. **Use access token in requests:**
   ```bash
   curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     http://127.0.0.1:8000/api/recipes/
   ```

5. **Refresh access token when expired:**
   ```bash
   curl -X POST http://127.0.0.1:8000/api/auth/token/refresh/ \
     -H "Content-Type: application/json" \
     -d '{"refresh": "YOUR_REFRESH_TOKEN"}'
   ```

## 💡 Usage Examples

### Create a New Recipe (Seller Only)

```bash
curl -X POST http://127.0.0.1:8000/api/recipes/ \
  -H "Content-Type: multipart/form-data" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F 'name=Spaghetti Carbonara' \
  -F 'description=Classic Italian pasta dish with eggs, cheese, and guanciale. Creamy texture without cream!' \
  -F 'recipe_image=@/path/to/carbonara.jpg'
```

**Or with JSON (without image):**
```bash
curl -X POST http://127.0.0.1:8000/api/recipes/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "name": "Spaghetti Carbonara",
    "description": "Classic Italian pasta dish with eggs, cheese, and guanciale. Creamy texture without cream!"
  }'
```

### Get All Recipes (Paginated)

```bash
# First page (default)
curl -X GET http://127.0.0.1:8000/api/recipes/

# Second page with 5 items per page
curl -X GET "http://127.0.0.1:8000/api/recipes/?page=2&page_size=5"
```

**Response:**
```json
{
  "count": 25,
  "next": "http://127.0.0.1:8000/api/recipes/?page=3&page_size=5",
  "previous": "http://127.0.0.1:8000/api/recipes/?page=1&page_size=5",
  "results": [
    {
      "id": 1,
      "name": "Spaghetti Carbonara",
      "description": "Classic Italian pasta dish...",
      "recipe_image": "http://127.0.0.1:8000/media/recipes/carbonara.jpg",
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z",
      "created_by": {
        "id": 1,
        "first_name": "John",
        "last_name": "Chef"
      }
    }
  ]
}
```

### Rate a Recipe (Customer Only)

```bash
curl -X POST http://127.0.0.1:8000/api/recipes/1/ratings/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "rating": 5
  }'
```

### Update Your Own Recipe (Seller Only)

```bash
curl -X PATCH http://127.0.0.1:8000/api/recipes/1/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "name": "Perfect Spaghetti Carbonara",
    "description": "Updated: The most authentic Italian pasta dish with step-by-step instructions"
  }'
```

### Get Recipe Ratings (Paginated)

```bash
curl -X GET http://127.0.0.1:8000/api/recipes/1/ratings/
```

## 🗄️ Models

### User Model (Extended Django User)
- `username` - Unique username
- `email` - User email address
- `first_name` - User's first name
- `last_name` - User's last name
- `password` - Hashed password
- `user_type` - Either "seller" or "customer"

**User Types:**
- **Seller**: Can create, update, and delete recipes
- **Customer**: Can rate and review recipes

### Recipes Model
```python
class Recipes(models.Model):
    name = models.CharField(max_length=255)           # Recipe name
    description = models.TextField()                   # Recipe description
    recipe_image = models.ImageField()                # Recipe image (optional)
    created_at = models.DateTimeField()               # Creation timestamp
    updated_at = models.DateTimeField()               # Last update timestamp
    created_by = models.ForeignKey(User)              # Recipe creator (seller only)
```

**Business Rules:**
- Only sellers can create recipes
- Recipe creators can update/delete their own recipes
- Recipe images are stored in `media/recipes/` folder
- Recipes display as: "Recipe Name by Creator's First Name"

### RecipeRatings Model
```python
class RecipeRatings(models.Model):
    recipe = models.ForeignKey(Recipes)               # Related recipe
    user = models.ForeignKey(User)                    # Rating author
    rating = models.IntegerField()                    # Rating (1-5 stars)
    created_at = models.DateTimeField()               # Rating timestamp
    updated_at = models.DateTimeField()               # Last update timestamp
```

**Business Rules:**
- Rating must be between 1-5 stars (validated)
- One rating per user per recipe (unique constraint)
- Any authenticated user can rate any recipe
- Users can update/delete their own ratings only
- Ratings display as: "user@email.com rated Recipe Name → 5*"

## 📁 Project Structure

```
Assignment-DRF/
├── manage.py
├── requirements.txt
├── README.md
├── recipe_platform/ # Main project settings
│ ├── init.py
│ ├── settings.py
│ ├── urls.py
│ ├── wsgi.py
│ └── asgi.py
├── apps/
│ ├── authentication/ # User authentication app
│ │ ├── init.py
│ │ ├── models.py
│ │ ├── serializers.py
│ │ ├── views.py
│ │ └── urls.py
│ ├── recipes/ # Recipe management app
│ │ ├── init.py
│ │ ├── models.py
│ │ ├── serializers.py
│ │ ├── views.py
│ │ ├── urls.py
│ │ └── permissions.py
│ └── utils/
│ ├── init.py
│ └── pagination.py
├── media/
| └── recipes/ # Recipe images storage
|__ backups/  
```

## 🧪 Testing

### Run All Tests

```bash
python manage.py test
```

### Test Specific Apps

```bash
# Test authentication
python manage.py test apps.authentication

# Test recipes and ratings
python manage.py test apps.recipes
```

### Manual API Testing

Use tools like Postman, Insomnia, or curl to test endpoints. Test different user types:

1. **As a Seller:**
   - Register with `user_type: "seller"`
   - Create, update, delete recipes
   - Cannot rate recipes (if restricted)

2. **As a Customer:**
   - Register with `user_type: "customer"`
   - Rate recipes (1-5 stars)
   - Cannot create recipes

## 🔧 Key Features Explained

### Pagination
- All list endpoints return paginated results
- Includes `count`, `next`, `previous`, and `results`
- Customizable page size via query parameters

### User Type Permissions
- **Sellers** can only create recipes (enforced by model constraint)
- **Customers** can rate any recipe
- Users can only modify their own content

### Image Handling
- Recipe images are optional
- Uploaded to `media/recipes/` folder
- Use multipart/form-data for file uploads

### Unique Rating Constraint
- One rating per user per recipe
- Prevents duplicate ratings
- Updates existing rating if user rates again

## 🚀 Common Workflows

### For Sellers:
1. Register with `user_type: "seller"`
2. Login to get JWT tokens
3. Create recipes with descriptions and images
4. Update your own recipes
5. View ratings on your recipes

### For Customers:
1. Register with `user_type: "customer"`
2. Browse recipes (no auth needed)
3. Login to rate recipes
4. Give 1-5 star ratings
5. Update your own ratings

### For Everyone:
1. Browse paginated recipe lists
2. View individual recipe details
3. See all ratings for any recipe

## 👨‍💻 Author

**Manoj** - [@manoj8260](https://github.com/manoj8260)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🔗 Quick Links

- **API Base URL**: `http://127.0.0.1:8000/api/`
- **Admin Panel**: `http://127.0.0.1:8000/admin/`
- **Browsable API**: `http://127.0.0.1:8000/api/`
- **Media Files**: `http://127.0.0.1:8000/media/`

**Happy Cooking! 👨‍🍳🍝**
