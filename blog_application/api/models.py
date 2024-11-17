from django.db import models

class User(models.Model):
    person_name = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='avatars/')
    email = models.EmailField(unique=True)
    login = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)   
    favorite_users = models.ManyToManyField('self', symmetrical=False, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True) 
    location = models.CharField(max_length=255, null=True, blank=True)  
    activity = models.DateTimeField(null=True, blank=True)  

    def __str__(self):
        return self.person_name

class Topic(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    pub_date = models.DateField()
    rating = models.IntegerField(default=0)
    commentary = models.TextField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    is_liked = models.BooleanField(default=False)
    like_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.commentary} by {self.user.person_name}"
