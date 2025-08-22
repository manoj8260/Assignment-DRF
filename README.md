# Recipe Platform API

![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-ff1709?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)

A comprehensive Django REST Framework API for managing recipes with user authentication, recipe creation, and rating system using JWT tokens.

## 🚀 Features

- **User Management**: User registration, login, and JWT-based authentication
- **Recipe Operations**: Create, read, update, and delete recipes
- **Recipe Ratings**: Users can rate and review recipes
- **JWT Authentication**: Secure token-based authentication with access/refresh tokens
- **Data Validation**: Robust input validation using DRF serializers
- **RESTful Design**: Clean API endpoints following REST principles
- **User Permissions**: Users can only modify their own recipes and ratings

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
| POST | `/auth/register/` | User registration | ❌ |
| POST | `/auth/login/` | User login (get JWT tokens) | ❌ |
| POST | `/auth/token/refresh/` | Refresh access token | ❌ |
| POST | `/auth/logout/` | User logout | ✅ |

### Recipe Endpoints
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/recipes/` | List all recipes | ❌ |
| POST | `/recipes/` | Create new recipe | ✅ |
| GET | `/recipes/{id}/` | Get recipe details | ❌ |
| PUT | `/recipes/{id}/` | Update recipe (owner only) | ✅ |
| PATCH | `/recipes/{id}/` | Partial update recipe | ✅ |
| DELETE | `/recipes/{id}/` | Delete recipe (owner only) | ✅ |

### Recipe Rating Endpoints
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/recipes/{recipe_id}/ratings/` | Get recipe ratings | ❌ |
| POST | `/recipes/{recipe_id}/ratings/` | Rate a recipe | ✅ |
| PUT | `/recipes/{recipe_id}/ratings/{id}/` | Update your rating | ✅ |
| DELETE | `/recipes/{recipe_id}/ratings/{id}/` | Delete your rating | ✅ |

### Query Parameters

- `?search=keyword` - Search recipes by title or ingredients
- `?ordering=created_at` - Sort by creation date
- `?ordering=-rating` - Sort by rating (descending)
- `?limit=10&offset=20` - Pagination parameters

## 🔐 Authentication

This project uses **JWT (JSON Web Token) authentication**. You'll receive two tokens:
- **Access Token**: For API requests (short-lived)
- **Refresh Token**: To get new access tokens (long-lived)

### Getting JWT Tokens

1. **Register a new user:**
   ```bash
   curl -X POST http://127.0.0.1:8000/api/auth/register/ \
     -H "Content-Type: application/json" \
     -d '{
       "username": "chef123",
       "email": "chef@example.com",
       "password": "securepassword123",
       "first_name": "John",
       "last_name": "Chef"
     }'
   ```

2. **Login to get JWT tokens:**
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
     "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
     "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
   }
   ```

3. **Use access token in requests:**
   ```bash
   curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
     http://127.0.0.1:8000/api/recipes/
   ```

4. **Refresh access token when expired:**
   ```bash
   curl -X POST http://127.0.0.1:8000/api/auth/token/refresh/ \
     -H "Content-Type: application/json" \
     -d '{"refresh": "YOUR_REFRESH_TOKEN"}'
   ```

## 💡 Usage Examples

### Create a New Recipe

```bash
curl -X POST http://127.0.0.1:8000/api/recipes/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "title": "Spaghetti Carbonara",
    "description": "Classic Italian pasta dish with eggs, cheese, and bacon",
    "ingredients": "400g spaghetti, 200g guanciale, 4 eggs, 100g pecorino cheese, black pepper",
    "instructions": "1. Cook pasta al dente. 2. Fry guanciale until crispy. 3. Mix eggs and cheese. 4. Combine all ingredients off heat.",
    "prep_time": 15,
    "cook_time": 20,
    "servings": 4,
    "difficulty": "medium"
  }'
```

### Get All Recipes

```bash
curl -X GET http://127.0.0.1:8000/api/recipes/
```

### Search Recipes

```bash
curl -X GET "http://127.0.0.1:8000/api/recipes/?search=pasta"
```

### Rate a Recipe

```bash
curl -X POST http://127.0.0.1:8000/api/recipes/1/ratings/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "rating": 5,
    "comment": "Absolutely delicious! Perfect recipe."
  }'
```

### Update Your Own Recipe

```bash
curl -X PUT http://127.0.0.1:8000/api/recipes/1/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "title": "Updated Spaghetti Carbonara",
    "description": "Updated classic Italian pasta dish",
    "ingredients": "Updated ingredients list",
    "instructions": "Updated cooking instructions"
  }'
```

## 🗄️ Models

### User Model (Extended Django User)
- `username` - Unique username
- `email` - User email
- `first_name` - User's first name
- `last_name` - User's last name
- `password` - Hashed password

### Recipe Model
- `title` - Recipe title
- `description` - Recipe description
- `ingredients` - List of ingredients
- `instructions` - Cooking instructions
- `prep_time` - Preparation time (minutes)
- `cook_time` - Cooking time (minutes)
- `servings` - Number of servings
- `difficulty` - Difficulty level (easy/medium/hard)
- `author` - Recipe creator (Foreign Key to User)
- `created_at` - Creation timestamp
- `updated_at` - Last update timestamp

### RecipeRating Model
- `recipe` - Related recipe (Foreign Key)
- `user` - Rating author (Foreign Key to User)
- `rating` - Rating score (1-5)
- `comment` - Optional rating comment
- `created_at` - Rating timestamp

## 📁 Project Structure

```
Assignment-DRF/
├── manage.py
├── requirements.txt
├── README.md
├── recipe_platform/              # Main project settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── authentication/           # User authentication app
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── recipes/                  # Recipe management app
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── permissions.py
│   └── ratings/                  # Recipe ratings app
│       ├── __init__.py
│       ├── models.py
│       ├── serializers.py
│       ├── views.py
│       └── urls.py
└── db.sqlite3                    # SQLite database
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

# Test recipes
python manage.py test apps.recipes

# Test ratings
python manage.py test apps.ratings
```

### Manual API Testing

Use tools like Postman, Insomnia, or curl to test endpoints. Import the API documentation or create requests manually using the examples above.

## 🔧 Development Features

### Admin Interface

Access the Django admin at `http://127.0.0.1:8000/admin/` to:
- Manage users
- View and edit recipes
- Monitor ratings
- Access system logs

### API Documentation

Visit `http://127.0.0.1:8000/api/` for the DRF browsable API interface.

## 🚀 Common Use Cases

### For Recipe Creators:
1. Register and login to get JWT tokens
2. Create recipes with detailed instructions
3. Edit and update your own recipes
4. Delete recipes you no longer want

### For Recipe Browsers:
1. Browse all available recipes without authentication
2. Search for specific recipes
3. View detailed recipe information
4. Register to rate and comment on recipes

### For Recipe Raters:
1. Login with JWT tokens
2. Rate recipes from 1-5 stars
3. Add comments to your ratings
4. Update or delete your own ratings

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 👨‍💻 Author

**Manoj** - [@manoj8260](https://github.com/manoj8260)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🔗 Quick Links

- **API Base URL**: `http://127.0.0.1:8000/api/`
- **Admin Panel**: `http://127.0.0.1:8000/admin/`
- **Browsable API**: `http://127.0.0.1:8000/api/`

**Happy Cooking! 👨‍🍳🍝**
