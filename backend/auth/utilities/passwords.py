def create_hashed_user(user_model, *, email, name, password):
    return user_model.objects.create_user(email=email, name=name, password=password)
