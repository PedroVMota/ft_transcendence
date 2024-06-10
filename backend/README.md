## Api Auth Routes

Auth routes:

```python
urlpatterns = [
    path('token/login/', UserLoginView.as_view(), name='login'),
    path('token/register/', UserRegistrationView.as_view(), name='register'),
    path('token/flush/', closeSession.as_view(), name='token_flush'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('user/', UserDetailView.as_view(), name='user'),
    path('', HomeView.as_view(), name='home'),
]

#Example of a route => http://localhost:8000/token/login/

```

### Token login:

requires a json object with the following structure:

```json
{
    "username": "username",
    "password": "password"
}


// Response
{
    "access": "access",
    "refresh": "refresh"
}
```

### Token register:

requires a json object with the following structure:

```json
{
    "username": "username",
    "password": "password",
    "email": "email"
}

// Response
{
    "message": "User created successfully"
}



```


### Token refresh:

requires a json object with the following structure:

```json
{
    "refresh": "refresh
}
```

### Token flush:

requires a json object with the following structure:

```json
{
    "refresh": "refresh
}
```

